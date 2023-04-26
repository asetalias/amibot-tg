from controllers.db import get_profile
import gen.amizone_pb2 as pb
from util.stub import stubber
from datetime import date
from google.type import date_pb2 as _date_pb2
import logging

logger = logging.getLogger()

async def get_class_schedule(telegram_id: int) -> pb.ScheduledClasses | None:
    profile = await get_profile(telegram_id)
    if profile is None:
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])

    today = date.today()
    val = _date_pb2.Date(year=today.year, month=today.month, day=4)

    try:
        logger.info("Getting class schedule via grpc")
        response = await stub.GetClassSchedule(pb.ClassScheduleRequest(date=val), metadata=metadata)
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
