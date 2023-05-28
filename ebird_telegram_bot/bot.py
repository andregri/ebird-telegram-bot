from collections import defaultdict
import datetime
from dotenv import load_dotenv
import os
import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from textwrap import dedent

from ebird import checklist

following_cache = defaultdict(list)
checklist_cache = {}

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}')

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
        user_name = checklist.user_display_name(ebird_user_id)
        msg += f"\n\n🔭 The latest checklist of {user_name} was on {date} at {time}"
        msg += f"\n🦩 Check it at https://ebird.org/checklist/{sub_id}"
    
    return msg

def usage_msg(command, num_args) -> str:
    if command == "follow":
        if num_args == 0:
            return dedent(f"""
                You should provide a eBird user ID, You find the ID of a user in the URL bar of your browser.
                For instance, /follow MTI3NzgwMA
                """)

        if num_args > 1:
            return dedent(f"""
                You should provide only one eBird user ID, You find the ID of a user in the URL bar of your browser.
                For instance, /follow MTI3NzgwMA
                """)

async def find_checklist(context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = ""

    ebird_user_id = context.job.data
    msg += latest_checklist_message(ebird_user_id)

    await context.bot.send_message(context.job.chat_id, text=msg)

async def follow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        return await update.message.reply_text(usage_msg("follow", len(context.args)))
    
    ebird_user_id = context.args[0]
    user_name = checklist.user_display_name(ebird_user_id)

    msg = f'Following {user_name} 🦜'

    # Store the user choice
    if ebird_user_id in following_cache[update.message.from_user.id]:
        await update.message.reply_text(dedent(f"""
            You are already following {user_name} 🦉
            """))
        return
    
    following_cache[update.message.from_user.id].append(ebird_user_id)
    print(f"follower: {update.message.from_user} following: {ebird_user_id}({user_name})")

    # Show the latest checklist, if any
    msg += latest_checklist_message(ebird_user_id)

    # Find the latest checklist daily by adding a job to the queue
    chat_id = update.effective_message.chat_id
    context.job_queue.run_daily(find_checklist, time=datetime.time(13, 30, tzinfo=pytz.timezone('Europe/Rome')),chat_id=chat_id, name=str(chat_id), data=ebird_user_id)
    print(context.job_queue.jobs)

    await update.message.reply_text(msg, disable_web_page_preview=True)

async def unfollow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        return await update.message.reply_text(usage_msg("follow", len(context.args)))
    
    ebird_user_id = context.args[0]
    user_name = checklist.user_display_name(ebird_user_id)

    following_cache_key = update.message.from_user.id
    following_list = following_cache[following_cache_key]
    print(f"Before: {following_list}")

    # Check if it was really followed
    if not ebird_user_id in following_list:
        msg = dedent(f"""
            You are not following {user_name} 🦆
            🦅 To start watching, use the command /follow
            """)
        return await update.message.reply_text(msg)

    # Remove user from cache
    following_list.remove(ebird_user_id)
    following_cache[following_cache_key] = following_list
    print(f"After {following_list}")
    print(f"{following_cache_key} unfollowed {user_name}")

    # Remove jobs from JobQueue
    job_name = update.effective_message.chat_id
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    for job in current_jobs:
        job.schedule_removal()
    
    msg = f'Unfollowed {user_name} 🪶'
    return await update.message.reply_text(msg)

load_dotenv()

token = os.environ["TELEGRAM_API_KEY"]
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("follow", follow))
app.add_handler(CommandHandler("unfollow", unfollow))

app.run_polling()