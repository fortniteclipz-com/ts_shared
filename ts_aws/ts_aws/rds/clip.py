import ts_aws.rds
import ts_logger
import ts_model.Clip
import ts_model.MontageClip
import ts_model.Exception

logger = ts_logger.get(__name__)

def save_clip(clip):
    logger.info("save_clip | start", clip=clip)
    session = ts_aws.rds.get_session()
    session.merge(clip)
    session.commit()
    session.close()
    logger.info("save_clip | success", clip=clip)

def get_clip(clip_id):
    logger.info("get_clip | start", clip_id=clip_id)
    session = ts_aws.rds.get_session()
    clip = session.query(ts_model.Clip).filter_by(clip_id=clip_id).first()
    session.close()
    logger.info("get_clip | success", clip=clip)
    if clip is None:
        raise ts_model.Exception(ts_model.Exception.CLIP__NOT_EXIST)
    return clip

def save_clips(clips):
    logger.info("save_clips | start", clips_length=len(clips))
    session = ts_aws.rds.get_session()
    session.bulk_save_objects(clips)
    session.commit()
    session.close()
    logger.info("save_clips | success")

def get_all_clips(limit):
    logger.info("get_all_clips | start", limit=limit)
    logger.info("get_all_clips | success")
