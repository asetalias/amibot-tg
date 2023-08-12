from controllers.db import get_profile_via_token
from controllers.rpc_calls import get_class_schedule_profile
import gen.amizone_pb2 as pb
import logging

logger = logging.getLogger()

async def get_class_schedule_api(token: int) -> pb.ScheduledClass | None:
    try:
        profile = await get_profile_via_token(token)
        if profile is None:
            logger.info("No profile found")
            return None

        schedule = await get_class_schedule_profile(profile)
        if schedule is None:
            return None

        return schedule
        
    except Exception as e:
        logger.error(e)
        return None