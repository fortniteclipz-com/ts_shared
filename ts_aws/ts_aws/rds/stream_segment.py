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

def get_stream_segment(stream, segment):
    logger.info("get_stream_segment | start", stream=stream, segment=segment)
    session = ts_aws.rds.get_session()
    stream_segment = session \
    .query(ts_model.StreamSegment) \
    .filter_by(stream_id=stream.stream_id, segment=segment) \
    .first()
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

def get_stream_segments(stream):
    logger.info("get_stream_segments | start", stream=stream)
    session = ts_aws.rds.get_session()
    stream_segments = session \
    .query(ts_model.StreamSegment) \
    .filter_by(stream_id=stream.stream_id) \
    .all()
    logger.info("get_stream_segments | success", stream_segments_length=len(stream_segments))
    if stream_segments is None:
        raise ts_model.Exception(ts_model.Exception.STREAM_SEGMENTS__NOT_EXIST)
    return stream_segments

def get_clip_stream_segments(clip):
    logger.info("get_clip_stream_segments | start", clip=clip)
    session = ts_aws.rds.get_session()
    stream_segments = session \
    .query(ts_model.StreamSegment) \
    .filter(
        ts_model.StreamSegment.stream_id == clip.stream_id,
        ts_model.StreamSegment.stream_time_out >= clip.time_in,
        ts_model.StreamSegment.stream_time_in < clip.time_out
    ) \
    .order_by(ts_model.StreamSegment.segment) \
    .all()
    session.close()
    logger.info("get_clip_stream_segments | success", stream_segments_length=len(stream_segments))
    if len(stream_segments) == 0:
        raise ts_model.Exception(ts_model.Exception.CLIP_STREAM_SEGMENTS__NOT_EXIST)
    return stream_segments
