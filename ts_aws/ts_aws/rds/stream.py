import ts_aws.rds
import ts_logger
import ts_model.Exception

logger = ts_logger.get(__name__)

def save_stream(stream):
    logger.info("save_stream | start", stream=stream)
    session = ts_aws.rds.get_session()
    session.merge(stream)
    session.commit()
    session.close()
    return stream
    logger.info("save_stream | success", stream=stream)

def get_stream(stream_id):
    logger.info("get_stream | start", stream_id=stream_id)
    logger.info("get_stream | success", stream_id=stream_id)

def get_streams(stream_id):
    logger.info("get_streams | start", stream_id=stream_id)
    logger.info("get_streams | success", stream_id=stream_id)
