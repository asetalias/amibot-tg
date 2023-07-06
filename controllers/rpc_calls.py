from controllers.db import get_profile
import gen.amizone_pb2 as pb
from util.stub import stubber
from datetime import date, timedelta
from google.type import date_pb2 as _date_pb2
import logging
from . import db

logger = logging.getLogger()


async def remove_profile(telegram_id: int):
    logger.info("Removing profile")
    profile = await get_profile(telegram_id)
    if profile is None:
        logger.info("Profile not found, nothing to delete")
    else:
        await db.delete_profile(telegram_id)
        logger.info("Profile deleted successfully")


async def get_user_profile(telegram_id: int):
    logger.info("Getting user profile")
    profile = await db.get_profile(telegram_id)
    if profile is None:
        logger.info("User does not exist")
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])

    try:
        logger.info("Getting user profile via grpc")
        response = await stub.GetUserProfile(pb.EmptyMessage(), metadata=metadata)
        return response
    except Exception as e:
        print(e.with_traceback(e.__traceback__))
        return None
    finally:
        channel.close()


async def get_class_schedule(telegram_id: int, tomorrow = False) -> pb.ScheduledClass | None:
    profile = await get_profile(telegram_id)
    if profile is None:
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])

    if tomorrow:
        today = date.today() + timedelta(days=1)
    else:
        today = date.today() 

    val = _date_pb2.Date(year=today.year, month=today.month, day=today.day)

    try:
        logger.info("Getting class schedule via grpc")
        response = await stub.GetClassSchedule(
            pb.ClassScheduleRequest(date=val), metadata=metadata
        )

        return response
    except Exception as e:
        print(e.with_traceback(e.__traceback__))
        return None
    finally:
        await channel.close()


async def get_current_course(telegram_id: int) -> pb.Courses | None:
    profile = await get_profile(telegram_id)
    if profile is None:
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])
    try:
        logger.info("Getting current course via grpc")
        response = await stub.GetCurrentCourses(pb.EmptyMessage(), metadata=metadata)
        return response
    except Exception as e:
        return None
    finally:
        await channel.close()


async def get_attendance(telegram_id: int) -> pb.AttendanceRecords | None:
    profile = await get_profile(telegram_id)
    if profile is None:
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])
    try:
        logger.info("Getting attendance via grpc")
        response = await stub.GetAttendance(pb.EmptyMessage(), metadata=metadata)
        return response
    except Exception as e:
        print(e)
        return None
    finally:
        await channel.close()


async def get_exam_schedule(telegram_id) -> pb.ExaminationSchedule | None:
    profile = await get_profile(telegram_id)
    if profile is None:
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])
    try:
        logger.info("Getting exam schedule via grpc")
        response = await stub.GetExamSchedule(pb.EmptyMessage(), metadata=metadata)
        return response
    except Exception as e:
        print(e)
        return None
    finally:
        await channel.close()


async def fill_faculty_feedback(
    telegram_id, rating, query_rating, comment
) -> pb.FillFacultyFeedbackRequest | None:
    profile = await get_profile(telegram_id)
    if profile is None:
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])
    try:
        logger.info("Filling faculty feedback via grpc")
        response = await stub.FillFacultyFeedback(
            pb.FillFacultyFeedbackRequest(
                rating=rating, query_rating=query_rating, comment=comment
            ),
            metadata=metadata,
        )
        return response
    except Exception as e:
        print(e)
        return None
    finally:
        await channel.close()


async def get_wifi_info(telegram_id) -> pb.WifiMacInfo | None:
    profile = await get_profile(telegram_id)
    if profile is None:
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])

    try:
        response = await stub.GetWifiMacInfo(
            pb.EmptyMessage(),
            metadata=metadata,
        )
        return response
    except Exception as e:
        logger.warning(f"From get_wifi_info: {e}")
        return None
    finally:
        await channel.close()


async def register_wifi(
    telegram_id, mac_address, override_limit
) -> pb.RegisterWifiMacRequest | None:
    profile = await get_profile(telegram_id)
    if profile is None:
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])
    try:
        response = await stub.RegisterWifiMac(
            pb.RegisterWifiMacRequest(
                address=mac_address, override_limit=override_limit
            ),
            metadata=metadata,
        )
        return response
    except Exception as e:
        logger.warning(f"From register_wifi: {e}")
        return None
    finally:
        await channel.close()
