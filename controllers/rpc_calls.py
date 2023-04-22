from controllers.auth import get_profile
import gen.amizone_pb2 as pb
from util.stub import stubber


def get_attendance(telegram_id) -> pb.AttendanceRecords | None:

    profile = get_profile(telegram_id)
    if profile is None:
        return None
    
    stub, metadata, channel = stubber(profile["username"], profile["password"])
    
    try:
        response = stub.GetAttendance(pb.EmptyMessage(), metadata=metadata)
        return response
    except Exception as e:
        print(e)
        return None
    finally:
        channel.close()
    

