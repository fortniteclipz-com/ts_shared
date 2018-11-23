import ts_aws.rds
import ts_logger

logger = ts_logger.get(__name__)

def save_stream_moments(stream_moments):
    logger.info("save_stream_moments | start", stream_moments_length=len(stream_moments))
    session = ts_aws.rds.get_session()
    session.bulk_save_objects(stream_moments)
    session.commit()
    session.close()
    logger.info("save_stream_moments | success")

def get_stream_moments(stream):
    logger.info("get_stream_moments | start", stream=stream)
    logger.info("get_stream_moments | success")
