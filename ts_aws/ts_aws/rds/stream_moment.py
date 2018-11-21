import ts_config
import ts_logger

logger = ts_logger.get(__name__)

def save_stream_moments(stream_moments):
    logger.info("save_stream_moments | start", stream_moments_length=len(stream_moments))
    logger.info("save_stream_moments | success")

def get_stream_moments(stream_id):
    logger.info("get_stream_moments | start", stream_id=stream_id)
    logger.info("get_stream_moments | success")
