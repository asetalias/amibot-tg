from telegram import Update
from telegram.ext import ContextTypes
from controllers.auth import create_profile
from controllers.rpc_calls import *


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg: str = """
    Welcome to AmiBot, the Amizone Telegram Bot!
    This bot is still in development, and many features will be added soon.
    Use /help to see the list of commands.
    """
    await update.message.reply_text(msg)


async def login_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    input_args = input_text.split(" ")

    if len(input_args) != 3:
        await update.message.reply_text(
            "Invalid login command. \nUse the command like -> /login 837283 password."
        )
        return

    username = input_args[1]
    password = input_args[2]
    user_id = update.effective_user.id

    try:
        await create_profile(user_id, username, password)
        await update.message.reply_text(f"Successfully logged in")
    except Exception as e:
        await update.message.reply_text(
            "There was an error logging in. Please try again later."
        )


async def get_attendance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        response = await get_attendance(user_id)
        if response is None:
            await update.message.reply_text(
                "There was an error, maybe you are not logged in. Use /login to login."
            )
            return

        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(
            "There was an error fetching attendance. Please try again later."
        )


async def get_exam_schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        response = await get_exam_schedule(user_id)
        if response is None:
            await update.message.reply_text(
                "There was an error, maybe you are not logged in. Use /login to login."
            )
            return

        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(
            "There was an error fetching exam schedule. Please try again later."
        )
