import ts_aws.rds
import ts_logger
import ts_model.Exception
import ts_model.StreamSegment

logger = ts_logger.get(__name__)

def save_stream_segment(stream_segment):
    logger.info("save_stream_segment | start", stream_segment=stream_segment)
    session = ts_aws.rds.get_session()
    session.merge(stream_segment)
    session.commit()
    session.close()
    return stream_segment
    logger.info("save_stream_segment | success", stream_segment=stream_segment)

def get_stream_segment(stream_id, segment):
    logger.info("get_stream_segment | start", stream_id=stream_id, segment=segment)
    session = ts_aws.rds.get_session()
    stream_segment = session.query(ts_model.StreamSegment).filter_by(stream_id=stream_id, segment=segment).first()
    session.close()
    logger.info("get_stream_segment | success", stream_segment=stream_segment)
    if stream_segment is None:
        raise ts_model.Exception(ts_model.Exception.STREAM_SEGMENT__NOT_EXIST)
    return stream_segment

def save_stream_segments(stream_segments):
    logger.info("save_stream_segments | start", stream_segments_length=len(stream_segments))
    session = ts_aws.rds.get_session()
    session.bulk_save_objects(stream_segments)
    session.commit()
    session.close()
    logger.info("save_stream_segments | success")

def get_stream_segments(stream_id):
    logger.info("get_stream_segments | start", stream_id=stream_id)
    logger.info("get_stream_segments | success", stream_segments_length=len(stream_segments))

def get_clip_stream_segments(clip):
    logger.info("get_clip_stream_segments | start", clip=clip)
    logger.info("get_clip_stream_segments | success", clip_stream_segments_length=len(clip_stream_segments))
