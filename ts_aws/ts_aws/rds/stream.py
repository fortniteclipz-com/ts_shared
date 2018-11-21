import ts_aws.rds
import ts_logger
import ts_model.Exception
import ts_model.Stream

logger = ts_logger.get(__name__)

def save_stream(stream):
    logger.info("save_stream | start", stream=stream)
    session = ts_aws.rds.get_session()
    session.merge(stream)
    session.commit()
    session.close()
    logger.info("save_stream | success", stream=stream)

def get_stream(stream_id):
    logger.info("get_stream | start", stream_id=stream_id)
    session = ts_aws.rds.get_session()
    stream = session.query(ts_model.Stream).filter_by(stream_id = stream_id).first()
    session.close()
    logger.info("get_stream | success", stream=stream)
    if stream is None:
        raise ts_model.Exception(ts_model.Exception.STREAM__NOT_EXIST)
    return stream

def get_streams(stream_id):
    logger.info("get_streams | start", stream_id=stream_id)
    logger.info("get_streams | success", stream_id=stream_id)
