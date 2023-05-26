from collections import defaultdict
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ebird import checklist

following_cache = defaultdict(list)
checklist_cache = {}

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

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
    else:
        following_cache[update.message.from_user.id].append(ebird_user_id)
        print(f"follower: {update.message.from_user} following: {ebird_user_id}({user_name})")

    # Display the latest checklist if any
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

    await update.message.reply_text(msg)

load_dotenv()

token = os.environ["TELEGRAM_API_KEY"]
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("follow", follow))

app.run_polling()