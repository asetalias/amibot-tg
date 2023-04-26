from telegram.ext import Application, CommandHandler, CallbackQueryHandler, filters
from util.env import TOKEN
from controllers.telegram_handlers import *
import logging


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logger = logging.getLogger()

    logger.info("Starting bot...")

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("login", login_handler))
    app.add_handler(CommandHandler("attendance", get_attendance_handler))
    app.add_handler(CommandHandler("exam", get_exam_schedule_handler))
    app.add_handler(CommandHandler("course", get_current_course_handler))
    app.add_handler(CommandHandler("today", get_class_schedule_handler))
    app.add_handler(CommandHandler("continue", continue_handler))

    # Query Handler
    app.add_handler(CallbackQueryHandler(button_query_handler))

    logger.info("Starting bot polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
