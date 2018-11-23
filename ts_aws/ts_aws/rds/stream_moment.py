import ts_aws.rds
import ts_logger
import ts_model.StreamMoment

logger = ts_logger.get(__name__)

def save_stream_moments(stream_moments):
    logger.info("save_stream_moments | start", stream_moments_length=len(stream_moments))
    session = ts_aws.rds.get_session()
    session.bulk_save_objects(stream_moments)
    session.commit()
    session.close()
    logger.info("save_stream_moments | success", stream_moments_length=len(stream_moments))

def get_stream_moments(stream):
    logger.info("get_stream_moments | start", stream=stream)
    session = ts_aws.rds.get_session()
    stream_moments = session \
    .query(ts_model.StreamMoment) \
    .filter_by(stream_id=stream.stream_id) \
    .all()
    logger.info("get_stream_moments | success", stream_moments_length=len(stream_moments))
    if len(stream_moments) == 0:
        raise ts_model.Exception(ts_model.Exception.STREAM_MOMENTS__NOT_EXIST)
    return stream_moments
