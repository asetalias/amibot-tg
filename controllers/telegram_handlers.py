from formatter.response_formatters import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from controllers.db import create_profile
from controllers.rpc_calls import *
import logging

logger = logging.getLogger()

BUTTON_MARKUP = [
        [InlineKeyboardButton("About", callback_data="about")],
        [
            InlineKeyboardButton("Attendance", callback_data="attendance"),
            InlineKeyboardButton("Exam Schedule", callback_data="exam")
        ],
        [
            InlineKeyboardButton("Current Course", callback_data="current_course"),
            InlineKeyboardButton("Class Schedule", callback_data="class_schedule")
        ]
    ]

# Query Handlers
async def button_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "about" in update.callback_query.data:
        msg: str = "AmiBot is a Telegram bot that provides an easy way to access Amizone. \nIt is brought to you by ALIAS."
        await update.callback_query.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))

    if "attendance" in update.callback_query.data:
        await get_attendance_handler(update, context)

    if "exam" in update.callback_query.data:
        await get_exam_schedule_handler(update, context)

    if "current_course" in update.callback_query.data:
        await get_current_course_handler(update, context)

    if "class_schedule" in update.callback_query.data:
        await get_class_schedule_handler(update, context)


# Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg: str = """\
        Welcome to AmiBot, the Amizone Telegram Bot!
        
        Enter your username and password separated by a space 
        Example: /login 837283 password

        If you have already logged in before, you can use /continue.

        To update your login credentials, use /login again.
        
    """
    await update.message.reply_text(msg)

async def continue_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome back!", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))

async def get_class_schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        await context.bot.send_message(chat_id=user_id, text="Fetching class schedule...")
        response = await get_class_schedule(user_id)
        if response is None:
            # ! Need better exception handling
            logger.debug(msg="Error fetching class schedule")
            await context.bot.send_message(chat_id=user_id, text="There was an error, maybe you are not logged in. Use /login to login.", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))
            return

        msg = get_class_schedule_formatter(response)

        await context.bot.send_message(chat_id=user_id, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP), text=msg)
    except Exception as e:
        print(e)
        await context.bot.send_message(chat_id=user_id, text="There was an error fetching class schedule. Please try again later.", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))

async def get_current_course_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        await context.bot.send_message(chat_id=user_id, text="Fetching current course...")
        response = await get_current_course(user_id)
        if response is None:
            # ! Need better exception handling
            await context.bot.send_message(chat_id=user_id, text="There was an error, maybe you are not logged in. Use /login to login.", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))
            return

        msg = get_courses_formatter(response)

        await context.bot.send_message(chat_id=user_id, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP), text=msg, parse_mode="HTML")
    except Exception as e:
        print(e)
        await context.bot.send_message(chat_id=user_id, text="There was an error fetching current course. Please try again later.", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))


async def login_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_text = update.message.text
    input_args = input_text.split(" ")

    if len(input_args) != 3:
        await update.message.reply_text("Invalid login command. \nUse the command like -> /login 837283 password.")
        return

    username = input_args[1]
    password = input_args[2]
    user_id = update.effective_user.id

    try:
        str = await create_profile(user_id, username, password)
        await update.message.reply_text("Successfully logged in", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))
    except Exception as e:
        print(e)
        await update.message.reply_text("There was an error logging in. Please try again later.")


async def get_attendance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        await context.bot.send_message(chat_id=user_id, text="Fetching attendance...")
        response = await get_attendance(user_id)
        # ! Need better exception handling
        if response is None:
            await context.bot.send_message(chat_id=user_id, text="There was an error, maybe you are not logged in. Use /login to login.", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))
            return
        
        msg = get_attendance_formatter(response)

        await context.bot.send_message(chat_id=user_id, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP), text=msg)
    except Exception as e:
        print(e)
        await context.bot.send_message(chat_id=user_id, text="There was an error fetching attendance. Please try again later.", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))


async def get_exam_schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        await context.bot.send_message(chat_id=user_id, text="Fetching exam schedule...")

        response = await get_exam_schedule(user_id)
        if response is None:
            # ! Need better exception handling
            await context.bot.send_message(chat_id=user_id, text="There was an error, maybe you are not logged in. Use /login to login.", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))
            return

        msg = get_exam_formatter(response)

        await context.bot.send_message(chat_id=user_id, text=msg, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))
    except Exception as e:
        print(e)
        await context.bot.send_message(chat_id=user_id, text="There was an error fetching exam schedule. Please try again later.", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP))
