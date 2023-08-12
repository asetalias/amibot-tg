from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from util.env import TOKEN, SENTRY_DSN, dev_mode
from controllers.telegram_handlers import *
from controllers.api import wear_os_controllers
from controllers.db import get_profile_via_token
import logging
import sentry_sdk
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import threading
import uvicorn

def api():
    class Data(BaseModel):
        token: int

    app = FastAPI()

    @app.get("/")
    async def index():
        return "Hello World!"

    @app.post("/login")
    async def login(data: Data):
        profile = await get_profile_via_token(data.token)
        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return {"status": "success", "message": "Logged in successfully"}


    @app.post("/class_schedule")
    async def class_schedule(data: Data):
        schedule = await wear_os_controllers.get_class_schedule_api(data.token)
        if schedule is None:
            return {"status": "error", "message": "No schedule found"}
        
        classes = []

        for i in schedule.classes:
            start = datetime.fromtimestamp(i.start_time.seconds)
            end = datetime.fromtimestamp(i.end_time.seconds)
            classes.append({
                "attendance": i.attendance,
                "course_code": i.course.code,
                "course_name": i.course.name,
                "time": f"{start.strftime('%H:%M')} to {end.strftime('%H:%M')}",
                "faculty": i.faculty,
            })

        return {"classes": classes}

    server_thread = threading.Thread(target=uvicorn.run, kwargs={"app": app, "host": "0.0.0.0", "port": 8081})
    server_thread.start()

def main():
    
    # Sentry, skip for dev mode
    if not dev_mode:
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            traces_sample_rate=1.0,
        )

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    logger = logging.getLogger()

    logger.info("Running API...")
    api()

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

