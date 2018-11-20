import ts_config
import ts_logger
import ts_model.StreamSegment

logger = ts_logger.get(__name__)

def save_stream_segment(stream_segment):
    logger.info("save_stream_segment | start", stream_segment=stream_segment)
    logger.info("save_stream_segment | success")

def get_stream_segment(stream_id, segment):
    logger.info("get_stream_segment | start", stream_id=stream_id, segment=segment)
    logger.info("get_stream_segment | success")

def save_stream_segments(stream_segments):
    logger.info("save_stream_segments | start", stream_segments_length=len(stream_segments))
    logger.info("save_stream_segments | success")

def get_stream_segments(stream_id):
    logger.info("get_stream_segments | start", stream_id=stream_id)
    logger.info("get_stream_segments | success")

def get_clip_stream_segments(clip):
    logger.info("get_clip_stream_segments | start", clip=clip)
    logger.info("get_clip_stream_segments | success")
