from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from controllers.db import create_profile
from controllers.rpc_calls import *

BUTTON_MARKUP = [
    [InlineKeyboardButton("About", callback_data="about")],
    [InlineKeyboardButton("Attendance", callback_data="attendance")],
    [InlineKeyboardButton("Exam Schedule", callback_data="exam")],
]


# Query Handlers
async def button_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "about" in update.callback_query.data:
        msg: str = "AmiBot is a Telegram bot that provides an easy way to access Amizone. \nIt is brought to you by ALIAS."
        await update.callback_query.message.reply_text(msg)

    if "attendance" in update.callback_query.data:
        await get_attendance_handler(update, context)

    if "exam" in update.callback_query.data:
        await update.callback_query.message.reply_text("Exam Schedule")


# Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg: str = "Welcome to AmiBot, the Amizone Telegram Bot! \n\nEnter your username and password separated by a space \nExample: /login 837283 password"
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
        str = await create_profile(user_id, username, password)
        await update.message.reply_text(
            "Successfully logged in", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP)
        )
    except Exception as e:
        print(e)
        await update.message.reply_text(
            "There was an error logging in. Please try again later."
        )


async def get_attendance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        response = await get_attendance(user_id)
        # ! Need better exception handling
        if response is None:
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login to login.",
            )
            return

        await context.bot.send_message(chat_id=user_id, text=str(response))
    except Exception as e:
        print(e)
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error fetching attendance. Please try again later.",
        )


async def get_exam_schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        response = await get_exam_schedule(user_id)
        if response is None:
            # ! Need better exception handling
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login to login.",
            )
            return

        await context.bot.send_message(chat_id=user_id, text=str(response))
    except Exception as e:
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error fetching exam schedule. Please try again later.",
        )
