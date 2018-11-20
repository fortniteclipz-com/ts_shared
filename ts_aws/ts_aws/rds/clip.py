import ts_config
import ts_logger
import ts_model.Clip
import ts_model.ClipSegment
import ts_model.Exception
import ts_model.StreamSegment

logger = ts_logger.get(__name__)

def save_clip(clip):
    logger.info("save_clip | start", clip=clip)
    logger.info("save_clip | success")

def get_clip(clip_id):
    logger.info("get_clip | start", clip_id=clip_id)
    logger.info("get_clip | success")

def save_clips(clips):
    logger.info("save_clips | start", clips_length=len(clips))
    logger.info("save_clips | success")

def get_clips(clip_ids):
    logger.info("get_clips | start", clip_ids=clip_ids)
    logger.info("get_clips | success")

def get_all_clips(limit):
    logger.info("get_all_clips | start", limit=limit)
    logger.info("get_all_clips | success")
