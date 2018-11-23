import ts_aws.rds
import ts_logger
import ts_model.Exception
import ts_model.MontageClip

logger = ts_logger.get(__name__)

def save_montage_clips(montage_clips):
    logger.info("save_montage_clips | start", montage_clips_length=len(montage_clips))
    session = ts_aws.rds.get_session()
    session.bulk_save_objects(montage_clips)
    session.commit()
    session.close()
    logger.info("save_montage_clips | success")

def get_montage_clips(montage):
    logger.info("get_montage_clips | start", montage=montage)
    session = ts_aws.rds.get_session()
    montage_clips = session \
        .query(ts_model.Clip) \
        .join(ts_model.MontageClip, ts_model.MontageClip.clip_id == ts_model.Clip.clip_id) \
        .filter_by(montage_id=montage.montage_id) \
        .order_by(ts_model.MontageClip.clip_order) \
        .all()
    session.close()
    logger.info("get_montage_clips | success", montage_clips=montage_clips)
    if len(montage_clips) == 0:
        raise ts_model.Exception(ts_model.Exception.MONTAGE_CLIPS__NOT_EXIST)
    return montage_clips
