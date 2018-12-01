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
    logger.info("save_montage_clips | success", montage_clips_length=len(montage_clips))
