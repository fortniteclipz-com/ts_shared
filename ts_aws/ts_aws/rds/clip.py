import ts_aws.rds
import ts_logger
import ts_model.Clip
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
    query = session \
        .query(ts_model.Clip) \
        .filter_by(clip_id=clip_id) \
        .limit(1)
    logger.info("get_clip | query", query=ts_aws.rds.print_query(query))
    clip = query.first()
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
    logger.info("save_clips | success", clips_length=len(clips))

def get_montage_clips(montage):
    logger.info("get_montage_clips | start", montage=montage)
    session = ts_aws.rds.get_session()
    query = session \
        .query(ts_model.Clip) \
        .join(ts_model.MontageClip, ts_model.MontageClip.clip_id == ts_model.Clip.clip_id) \
        .filter_by(montage_id=montage.montage_id) \
        .order_by(ts_model.MontageClip.clip_order)
    logger.info("get_montage_clips | query", query=ts_aws.rds.print_query(query))
    montage_clips = query.all()
    session.close()
    logger.info("get_montage_clips | success", montage_clips_length=len(montage_clips))
    if len(montage_clips) == 0:
        raise ts_model.Exception(ts_model.Exception.MONTAGE_CLIPS__NOT_EXIST)
    return montage_clips
