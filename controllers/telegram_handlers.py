from formatter.response_formatters import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
from controllers.db import *
from controllers.rpc_calls import *
import logging
from util.env import TOKEN
from util import helpers

logger = logging.getLogger()

BUTTON_MARKUP = [
    [
        InlineKeyboardButton("About", callback_data="about"),
        InlineKeyboardButton("WearOS", callback_data="wearos"),
    ],
    [
        InlineKeyboardButton("Attendance", callback_data="attendance"),
        InlineKeyboardButton("Class Schedule", callback_data="class_schedule"),
        
    ],
    [
        InlineKeyboardButton("Current Course", callback_data="current_course"),
        InlineKeyboardButton("Tomorrow Schedule", callback_data="tomorrow_schedule"),
    ],
    [
        InlineKeyboardButton("Get WiFi info", callback_data="get_wifi_info"),
        InlineKeyboardButton("Register for WiFi", callback_data="register_wifi"),
    ],
    [
        InlineKeyboardButton("Exam Schedule", callback_data="exam"),
        InlineKeyboardButton("Faculty Feedback", callback_data="faculty_feedback"),
    ],
]

ABOUT_MESSAGE = """\
AmiBot is a telegram bot designed to take the frustration out of using Amizone.

AmiBot is an open-source initiative, inviting users to contribute and improve its capabilities for all. Interested? Learn more by <a href='https://github.com/asetalias/amibot-tg'>Clicking here</a>

Made with ❤️ by <a href='https://asetalias.in/'>ALiAS</a>
"""

WIFI_MESSAGE = """Register for wifi: add as many devices as you want!

Type /addwifi to get started."""

WIFI_INSTRUCTIONS = """\
This method will register your device to Amity wifi.

Reply with cancel to abort this operation, or with details in the following format:
{MAC address} {override}

where
→ MAC address is the mac address of your device. Not sure how to find your MAC address? <a href='https://www.wikihow.com/Find-the-MAC-Address-of-Your-Computer'>Click here</a>
→ TRUE or FALSE where true allows you to register for more than 2 devices

Example:
AA:BB:CC:DD:EE:FF true
"""

FEEDBACK_MESSAGE = """Submit feedback for all faculty, in one go 🚀
        
Type /facultyFeedback to get started."""

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
        await update.callback_query.message.reply_text(
            ABOUT_MESSAGE, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP)
        )

    if "wearos" in update.callback_query.data:
        await wearos_token_handler(update, context)

    if "attendance" in update.callback_query.data:
        await get_attendance_handler(update, context)

    if "current_course" in update.callback_query.data:
        await get_current_course_handler(update, context)

    if "class_schedule" in update.callback_query.data:
        await get_class_schedule_handler(update, context)

    if "tomorrow_schedule" in update.callback_query.data:
        await get_class_schedule_handler(update, context, tomorrow=True)
    
    if "exam" in update.callback_query.data:
        await get_exam_schedule_handler(update, context)

    if "faculty_feedback" in update.callback_query.data:
        await update.callback_query.message.reply_text(
            FEEDBACK_MESSAGE, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP)
        )

    if "get_wifi_info" in update.callback_query.data:
        await get_wifi_info_handler(update, context)

    if "register_wifi" in update.callback_query.data:
        await update.callback_query.message.reply_text(
            WIFI_MESSAGE, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP)
        )


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


async def get_class_schedule_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, tomorrow = False):
    user_id = update.effective_user.id
    try:
        await context.bot.send_message(chat_id=user_id, text="Fetching class schedule...")
        response = await get_class_schedule(user_id, tomorrow = tomorrow)
        if response is None:
            # ! Need better exception handling
            logger.debug(msg="Error fetching class schedule")
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login {amizone_id} {password} to login.",
            )
            return
        if len(response.classes) == 0:
            msg = "Enjoy your class-free day! 😄🎉"
        else:
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
                text="There was an error, maybe you are not logged in. Use /login {amizone_id} {password} to login.",
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

    await context.bot.send_message(
        chat_id=user_id,
        text="Logging you in...",
    )

    try:
        logger.info("Creating user profile for login validation")
        await create_profile(user_id, username, password)
        user = await get_user_profile(user_id)
        if user:
            logger.info("User exists, logging in")
            await update.message.reply_text(
                f"Successfully logged in\n\nWelcome to AmiBot {user.name.split(' ')[0]}!",
                reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
            )
        else:
            logger.info("User does not exist, removing profile")
            await remove_profile(user_id)
            await update.message.reply_text(
                f"Invalid username or password. Try again with correct credentials.",
            )
    except Exception as e:
        print(e)
        await update.message.reply_text(
            "There was an error logging in. Please try again later."
        )
        
    await update.message.delete()

async def wearos_token_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    try:
        profile = await get_profile(user_id)
        if profile is None:
            await context.bot.send_message(
                chat_id=user_id,
                text="You are not logged in. Use /login {amizone_id} {password} to login.",
            )
            return

        for i in range(3):
            token = helpers.get_random()
            
            val = await checkToken(profile["_id"], token)
            
            if val:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"Your token is {token}. Please enter this token in the WearOS app.",
                )
                return


        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error generating token. Please try again later.",
        )

    except Exception as e:
        logger.error(e)
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error fetching your profile. Please try again later.",
        )
        return
        


async def get_attendance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        await context.bot.send_message(chat_id=user_id, text="Fetching attendance...")
        response = await get_attendance(user_id)
        # ! Need better exception handling
        if response is None:
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login {amizone_id} {password} to login.",
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

        if response == "not_logged_in":
            await context.bot.send_message(
            chat_id=user_id,
            text="You are not logged in. Use /login {amizone_id} {password} to login.",
            )
            return
        elif response is None:
            # ! Need better exception handling
            await context.bot.send_message(
                chat_id=user_id,
                text="No Exams! Chill......🤓",
                reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
            )
            return
        else:
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

    cancelled = helpers.check_cancel(user_response_args)

    if cancelled:
        await context.bot.send_message(
            chat_id=user_id,
            text="Operation cancelled",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )
        return ConversationHandler.END

    if len(user_response_args) < 3:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Invalid format. Please enter your response in the format: {rating} {query rating} {comment} or type cancel to abort the operation.",
        )
        return GET_FACULTY_FEEDBACK

    try:
        rating = int(user_response_args[0])
        query_rating = int(user_response_args[1])

        if not (1 <= rating <= 5) or not (1 <= query_rating <= 3):
            raise ValueError()

        comment = " ".join(user_response_args[2:])

        await context.bot.send_message(
                chat_id=user_id,
                text="Filling faculty feedback...",
            )

        response = await fill_faculty_feedback(user_id, rating, query_rating, comment)
        if response is None:
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login {amizone_id} {password} to login.",
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

    except ValueError:
        await context.bot.send_message(
            chat_id=user_id,
            text="Invalid format or values. Please enter your response in the format: {rating} {query rating} {comment} where rating is an integer between 1 and 5, and query rating is an integer between 1 and 3.\nType cancel to abort the operation.",
        )
        return GET_FACULTY_FEEDBACK
    except Exception as e:
        print(e)
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error filling faculty feedback. Please try again later.",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )

    return ConversationHandler.END


async def get_wifi_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        await context.bot.send_message(
            chat_id=user_id, text="Fetching WiFi information..."
        )

        response = await get_wifi_info(user_id)
        if response is None:
            # ! Need better exception handling
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login {amizone_id} {password} to login.",
            )
            return

        msg = get_wifi_info_formatter(response)

        await context.bot.send_message(
            chat_id=user_id, text=msg, reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP)
        )
    except Exception as e:
        print(e)
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error fetching WiFi information. Please try again later.",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )


REGISTER_WIFI = range(1)


async def register_wifi_entry(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_id = update.effective_user.id
    await context.bot.send_message(
        chat_id=user_id, text=WIFI_INSTRUCTIONS, parse_mode=ParseMode.HTML
    )
    logger.info("Sent WiFi registration instructions")
    return REGISTER_WIFI


async def register_wifi_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_id = update.effective_user.id
    user_response = update.message.text
    user_response_args = user_response.split(" ")
    logger.info("Received input for WiFi registration")

    cancelled = helpers.check_cancel(user_response_args)

    if cancelled:
        await context.bot.send_message(
            chat_id=user_id,
            text="Operation cancelled",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )
        return ConversationHandler.END

    if len(user_response_args) != 2:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Invalid format. Please enter your response in the format:\n{MAC Address} {true/false}.\nType cancel to abort the operation.",
        )
        return REGISTER_WIFI

    try:
        address = user_response_args[0]
        override = user_response_args[1]
        if not ("true" or "false" in override.lower()):
            raise ValueError()
        override = False if "false" in override.lower() else True

        response = await register_wifi(user_id, address, override)
        if response is None:
            await context.bot.send_message(
                chat_id=user_id,
                text="There was an error, maybe you are not logged in. Use /login {amizone_id} {password} to login.",
            )
        else:
            await context.bot.send_message(
                chat_id=user_id,
                text="Registered for wifi",
                reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
            )

    except ValueError:
        await context.bot.send_message(
            chat_id=user_id,
            text="Invalid format or values. Please enter your response in the format: {address} {override} where address is the MAC address of the device you wish to add and override is True/Flase.\nType cancel to abort the operation.",
        )
        return REGISTER_WIFI
    except Exception as e:
        print(e)
        await context.bot.send_message(
            chat_id=user_id,
            text="There was an error registering your MAC address on amizone. Please try again later.",
            reply_markup=InlineKeyboardMarkup(BUTTON_MARKUP),
        )

    return ConversationHandler.END
