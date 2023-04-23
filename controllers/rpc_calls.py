from controllers.db import get_profile
import gen.amizone_pb2 as pb
from util.stub import stubber


async def get_attendance(telegram_id: int) -> pb.AttendanceRecords | None:
    profile = get_profile(telegram_id)
    if profile is None:
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])
    try:
        print("Getting attendance via grpc")
        response = await stub.GetAttendance(pb.EmptyMessage(), metadata=metadata)
        return response
    except Exception as e:
        print(e)
        return None
    finally:
        channel.close()


async def get_exam_schedule(telegram_id) -> pb.ExaminationSchedule | None:
    profile = await get_profile(telegram_id)
    if profile is None:
        return None

    stub, metadata, channel = stubber(profile["username"], profile["password"])

    try:
        response = await stub.GetExamSchedule(pb.EmptyMessage(), metadata=metadata)
        return response
    except Exception as e:
        print(e)
        return None
    finally:
        channel.close()
