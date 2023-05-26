from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from ebird import checklist


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

    await update.message.reply_text(f'Following {user_name}')

load_dotenv()

token = os.environ["TELEGRAM_API_KEY"]
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("follow", follow))

app.run_polling()