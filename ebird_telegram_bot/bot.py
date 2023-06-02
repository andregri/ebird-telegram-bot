from collections import defaultdict
import datetime
from dotenv import load_dotenv
import logging
import os
import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from textwrap import dedent

from ebird import checklist

following_cache = defaultdict(list)
checklist_cache = {}


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}')

def latest_checklist_message(ebird_user_id: str) -> str:
    # Display the latest checklist if any
    msg = ""

    try:
        checklists = checklist.get_latest(ebird_user_id)
    except Exception as e:
        logger.info(e)
        return dedent(f"""
            User not found or eBird is not responding now.
            Make sure the ID is correct and try again later.
            """)


    if len(checklists) > 0:
        loc_id = checklists[0]['locId']
        sub_id = checklists[0]['subId']
        checklist_cache[ebird_user_id] = {'loc_id': loc_id, 'sub_id': sub_id}
        logger.info(f"{ebird_user_id} latest checklist id: {sub_id}")

        date = checklists[0]['obsDt']
        time = checklists[0]['obsTime']
        user_name = checklist.user_display_name(ebird_user_id)
        if user_name:
            msg += f"\n\n🔭 The latest checklist of {user_name} was on {date} at {time}"
            msg += f"\n🦩 Check it at https://ebird.org/checklist/{sub_id}"
        else:
            logger.info(f"{ebird_user_id} not found on eBird")
            return f"User {ebird_user_id} not found! Make sure the ID is correct."
    
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
    if not user_name:
        return await update.message.reply_text(f"User {ebird_user_id} not found! Make sure the ID is correct.")

    msg = f'Following {user_name} 🦜'

    cache_key = update.effective_message.chat_id

    # Store the user choice
    if ebird_user_id in following_cache[cache_key]:
        await update.message.reply_text(dedent(f"""
            You are already following {user_name} 🦉
            """))
        return
    
    following_cache[cache_key].append(ebird_user_id)
    logger.info(f"follower: {update.message.from_user} (cache key: {cache_key}) following: {ebird_user_id}({user_name})")

    # Show the latest checklist, if any
    msg += latest_checklist_message(ebird_user_id)

    # Find the latest checklist daily by adding a job to the queue
    chat_id = update.effective_message.chat_id
    job_name = f"{chat_id}{ebird_user_id}"
    context.job_queue.run_daily(find_checklist, time=datetime.time(13, 30, tzinfo=pytz.timezone('Europe/Rome')), chat_id=chat_id, name=job_name, data=ebird_user_id)
    logger.info(f"scheduled jobs: {[job.name for job in context.job_queue.jobs()]}")

    await update.message.reply_text(msg, disable_web_page_preview=True)

async def unfollow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        return await update.message.reply_text(usage_msg("follow", len(context.args)))
    
    ebird_user_id = context.args[0]
    user_name = checklist.user_display_name(ebird_user_id)
    if not user_name:
        return await update.message.reply_text(f"User {ebird_user_id} not found! Make sure the ID is correct.")

    following_cache_key = update.effective_message.chat_id
    following_list = following_cache[following_cache_key]
    logger.info(f"Before: {following_list}")

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
    logger.info(f"After {following_list}")
    logger.info(f"{following_cache_key} unfollowed {user_name}")

    # Remove jobs from JobQueue
    job_name = f"{update.effective_message.chat_id}{ebird_user_id}"
    current_jobs = context.job_queue.get_jobs_by_name(job_name)
    for job in current_jobs:
        job.schedule_removal()
        logger.info(f"Scheduled removal of job {job_name}")
    
    msg = f'Unfollowed {user_name} 🪶'
    return await update.message.reply_text(msg)

async def list_following(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id

    logger.info(f"{chat_id} /list")

    if not chat_id in following_cache:
        return await update.message.reply_text(f"You are not following anyone 🦅")
    
    msg = "You are following:\n"
    for following in following_cache[chat_id]:
        msg += f"📌 {checklist.user_display_name(following)} ({following})\n"
    return await update.message.reply_text(msg)

load_dotenv()

token = os.environ["TELEGRAM_API_KEY"]
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("follow", follow))
app.add_handler(CommandHandler("unfollow", unfollow))
app.add_handler(CommandHandler("list", list_following))

app.run_polling()