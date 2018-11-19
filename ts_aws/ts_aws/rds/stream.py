import ts_aws.rds
import ts_logger
import ts_model.Exception
import ts_model2.Stream

logger = ts_logger.get(__name__)

def save_stream(stream):
    logger.info("save_stream | start", stream=stream)
    session = ts_aws.rds.get_session()
    session.merge(stream)
    session.commit()
    session.close()
    return stream
    logger.info("save_stream | success", stream=stream)
