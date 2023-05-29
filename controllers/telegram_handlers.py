from formatter.response_formatters import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from controllers.db import create_profile
from controllers.rpc_calls import *
import logging
from util.env import TOKEN

logger = logging.getLogger()

BUTTON_MARKUP = [
    [InlineKeyboardButton("About", callback_data="about")],
    [
        InlineKeyboardButton("Attendance", callback_data="attendance"),
        InlineKeyboardButton("Exam Schedule", callback_data="exam"),
    ],
    [
        InlineKeyboardButton("Current Course", callback_data="current_course"),
        InlineKeyboardButton("Class Schedule", callback_data="class_schedule"),
    ],
    [InlineKeyboardButton("Faculty Feedback", callback_data="faculty_feedback")],
]

FEEDBACK_INSTRUCTIONS = """\
This method will submit feedback for all your faculty in a single step.

Reply with cancel to abort this operation, or with details in the following format:
{Score} {Query score} {Comment}

where
→ Score is a 1-5 score used for most feedback points (higher is better)
→ Query score is a 1-3 score used for query feedback (higher is better)
→ Comment is a remark that will be sent with the feedback

Example:
5 3 Taught us well

Please note that the same scores and comments will be used for all faculties with pending feedbacks.
"""


# Query Handlers
async def button_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "about" in update.callback_query.data:
        msg: str = "AmiBot is a Telegram bot that provides an easy way to access Amizone. \nIt is brought to you by ALIAS."
        await update.callback_query.message.reply_text(
            msg, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP)
        )

    if "attendance" in update.callback_query.data:
        await get_attendance_handler(update, context)

    if "exam" in update.callback_query.data:
        await get_exam_schedule_handler(update, context)

    if "current_course" in update.callback_query.data:
        await get_current_course_handler(update, context)

    if "class_schedule" in update.callback_query.data:
        await get_class_schedule_handler(update, context)

    if "faculty_feedback" in update.callback_query.data:
        await fill_faculty_feedback_handler(update, context)


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
    await update.message.reply_text(
        "Welcome back!", reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP)
    )


async def get_class_schedule_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    try:
        await context.bot.send_message(
            chat_id=user_id, text="Fetching class schedule..."
        )
        response = await get_class_schedule(user_id)
        if response is None:
            # ! Need better exception handling
            logger.debug(msg="Error fetching class schedule")
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login to login.",
                reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
            )
            return

        msg = get_class_schedule_formatter(response)

        await context.bot.send_message(
            chat_id=user_id, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP), text=msg
        )
    except Exception as e:
        print(e)
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error fetching class schedule. Please try again later.",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )


async def get_current_course_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user_id = update.effective_user.id
    try:
        await context.bot.send_message(
            chat_id=user_id, text="Fetching current course..."
        )
        response = await get_current_course(user_id)
        if response is None:
            # ! Need better exception handling
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login to login.",
                reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
            )
            return

        msg = get_courses_formatter(response)

        await context.bot.send_message(
            chat_id=user_id,
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
            text=msg,
            parse_mode="HTML",
        )
    except Exception as e:
        print(e)
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error fetching current course. Please try again later.",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )


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
        await context.bot.send_message(chat_id=user_id, text="Fetching attendance...")
        response = await get_attendance(user_id)
        # ! Need better exception handling
        if response is None:
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login to login.",
                reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
            )
            return

        msg = get_attendance_formatter(response)

        await context.bot.send_message(
            chat_id=user_id, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP), text=msg
        )
    except Exception as e:
        print(e)
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error fetching attendance. Please try again later.",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )


async def get_exam_schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        await context.bot.send_message(
            chat_id=user_id, text="Fetching exam schedule..."
        )

        response = await get_exam_schedule(user_id)
        if response is None:
            # ! Need better exception handling
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login to login.",
                reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
            )
            return

        msg = get_exam_formatter(response)

        await context.bot.send_message(
            chat_id=user_id, text=msg, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP)
        )
    except Exception as e:
        print(e)
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error fetching exam schedule. Please try again later.",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )


GET_FACULTY_FEEDBACK = range(1)


async def fill_faculty_feedback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_id = update.effective_user.id
    await context.bot.send_message(chat_id=user_id, text=FEEDBACK_INSTRUCTIONS)
    logger.info("Sent faculty feedback instructions")
    return GET_FACULTY_FEEDBACK


async def get_faculty_feedback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_id = update.effective_user.id
    user_response = update.message.text
    user_response_args = user_response.split(" ")
    logger.info("Received input for faculty feedback")

    if len(user_response_args) != 3:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Invalid format. Please enter your response in the format: {rating} {query rating} {comment}",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )
        return GET_FACULTY_FEEDBACK

    try:
        rating = int(user_response_args[0])
        query_rating = int(user_response_args[1])

        if not (1 <= rating <= 5) or not (1 <= query_rating <= 3):
            raise ValueError()

        comment = " ".join(user_response_args[2:])

        response = await fill_faculty_feedback(user_id, rating, query_rating, comment)
        if response is None:
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login to login.",
                reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
            )

    except ValueError:
        await context.bot.send_message(
            chat_id=user_id,
            text="Invalid format or values. Please enter your response in the format: {rating} {query rating} {comment} where rating is an integer between 1 and 5, and query rating is an integer between 1 and 3.",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )
    except Exception as e:
        print(e)
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error filling faculty feedback. Please try again later.",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )

    final = (
        "Feedback submitted successfully for "
        + str(response.filled_for)
        + " faculties."
    )
    await context.bot.send_message(
        chat_id=user_id,
        text=final,
        reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
    )

    return ConversationHandler.END
