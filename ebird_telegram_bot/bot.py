from collections import defaultdict
import datetime
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ebird import checklist

following_cache = defaultdict(list)
checklist_cache = {}

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}',
        disable_web_page_preview=True)

def latest_checklist_message(ebird_user_id: str) -> str:
    # Display the latest checklist if any
    msg = ""

    checklists = checklist.get_latest(ebird_user_id)
    if len(checklists) > 0:
        loc_id = checklists[0]['locId']
        sub_id = checklists[0]['subId']
        checklist_cache[ebird_user_id] = {'loc_id': loc_id, 'sub_id': sub_id}
        print(f"{ebird_user_id} latest checklist id: {sub_id}")

        date = checklists[0]['obsDt']
        time = checklists[0]['obsTime']
        msg += f"\n\n🔭 The latest checklist was on {date} at {time}"
        msg += f"\n🦩 Check it at https://ebird.org/checklist/{sub_id}"
    
    return msg

async def find_checklist(context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = ""

    ebird_user_id = context.job.data
    msg += latest_checklist_message(ebird_user_id)

    await context.bot.send_message(context.job.chat_id, text=msg)

async def follow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 0:
        await update.message.reply_text(f"""
            You should provide a eBird user ID, for instance /follow MTI3NzgwMA
            You find the ID of a user in the URL bar of your browser.
            """)
        return
    
    if len(context.args) > 1:
        await update.message.reply_text(f"""
            You should provide only one eBird user ID, for instance /follow MTI3NzgwMA
            You find the ID of a user in the URL bar of your browser.
            """)
        return
    
    ebird_user_id = context.args[0]
    user_name = checklist.user_display_name(ebird_user_id)

    msg = f'Following {user_name} 🦜'

    # Store the user choice
    if ebird_user_id in following_cache[update.message.from_user.id]:
        await update.message.reply_text(f"""
            You are already following {user_name} 🦉
            """)
        return
    
    following_cache[update.message.from_user.id].append(ebird_user_id)
    print(f"follower: {update.message.from_user} following: {ebird_user_id}({user_name})")

    # Show the latest checklist, if any
    msg += latest_checklist_message(ebird_user_id)

    # Find the latest checklist daily by adding a job to the queue
    chat_id = update.effective_message.chat_id
    context.job_queue.run_daily(find_checklist, time=datetime.time(9, 0),chat_id=chat_id, name=str(chat_id), data=ebird_user_id)
    print(context.job_queue.jobs)

    await update.message.reply_text(msg, disable_web_page_preview=True)

load_dotenv()

token = os.environ["TELEGRAM_API_KEY"]
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("follow", follow))

app.run_polling()