from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from util.env import TOKEN, SENTRY_DSN, DEV_MODE, TEST_TOKEN
from util.logger import AmibotLogger
from controllers.telegram_handlers import *
from controllers.db import get_profile_via_token

import sentry_sdk


def main():
 
    logger = AmibotLogger("AmiBot")

    # Set token according to dev mode
    if DEV_MODE == "True":
        logger.debug("Running in dev mode...")
        curr_token = TEST_TOKEN
    else:
        logger.debug("Running in prod mode...")
        curr_token = TOKEN

    logger.info("Starting bot...")
    app = Application.builder().token(curr_token).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("login", login_handler))
    app.add_handler(CommandHandler("attendance", get_attendance_handler))
    app.add_handler(CommandHandler("exam", get_exam_schedule_handler))
    app.add_handler(CommandHandler("course", get_current_course_handler))
    app.add_handler(CommandHandler("today", get_class_schedule_handler))
    app.add_handler(CommandHandler("continue", continue_handler))
    app.add_handler(CommandHandler("wifiInfo", get_wifi_info_handler))

    # Conversation Handlers
    feedback_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("facultyFeedback", fill_faculty_feedback_handler)],
        states={
            GET_FACULTY_FEEDBACK: [MessageHandler(filters.ALL, get_faculty_feedback)]
        },
        fallbacks=[],
    )

    register_wifi_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("addWifi", register_wifi_entry)],
        states={
            REGISTER_WIFI: [MessageHandler(filters.ALL, register_wifi_handler)],
        },
        fallbacks={},
    )

    app.add_handler(feedback_conv_handler)
    app.add_handler(register_wifi_conv_handler)
    app.add_handler(CallbackQueryHandler(button_query_handler))

    # Query Handler
    app.add_handler(CallbackQueryHandler(button_query_handler))

    logger.info("Starting bot polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
