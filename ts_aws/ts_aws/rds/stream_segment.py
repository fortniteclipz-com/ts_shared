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
    query = session \
        .query(ts_model.StreamSegment) \
        .filter_by(
            stream_id=stream.stream_id,
            segment=segment
        ) \
        .limit(1)
    logger.info("get_stream_segment | query", query=ts_aws.rds.print_query(query))
    stream_segment = query.first()
    session.close()
    logger.info("get_stream_segment | success", stream_segment=stream_segment)
    if stream_segment is None:
        raise ts_model.Exception(ts_model.Exception.STREAM_SEGMENT__NOT_EXIST)
    return stream_segment

def save_stream_segments(stream_segments):
    logger.info("save_stream_segments | start", stream_segments_length=len(stream_segments))
    columns = [column.key for column in ts_model.StreamSegment.__table__.columns]
    values = ', '.join(list(map(lambda ss: str(tuple([('NULL' if ss[column.key] is None else ss[column.key]) for column in ts_model.StreamSegment.__table__.columns])), stream_segments)))
    query = f"REPLACE INTO {ts_model.StreamSegment.__tablename__} ({', '.join(columns)}) VALUES {values};"
    logger.info("save_stream_segments | query", query=query)
    engine = ts_aws.rds.get_engine()
    with engine.connect() as c:
        c.execute(query)
    logger.info("save_stream_segments | success", stream_segments_length=len(stream_segments))

def get_stream_segments(stream):
    logger.info("get_stream_segments | start", stream=stream)
    session = ts_aws.rds.get_session()
    query = session \
        .query(ts_model.StreamSegment) \
        .filter_by(stream_id=stream.stream_id)
    stream_segments = query.all()
    logger.info("get_stream_segments | query", query=ts_aws.rds.print_query(query))
    session.close()
    logger.info("get_stream_segments | success", stream_segments_length=len(stream_segments))
    if stream_segments is None:
        raise ts_model.Exception(ts_model.Exception.STREAM_SEGMENTS__NOT_EXIST)
    return stream_segments

def get_clip_stream_segments(clip):
    logger.info("get_clip_stream_segments | start", clip=clip)
    session = ts_aws.rds.get_session()
    query = session \
        .query(ts_model.StreamSegment) \
        .filter(
            ts_model.StreamSegment.stream_id == clip.stream_id,
            ts_model.StreamSegment.stream_time_in < clip.time_out,
            ts_model.StreamSegment.stream_time_out >= clip.time_in,
        ) \
        .order_by(ts_model.StreamSegment.segment)
    logger.info("get_clip_stream_segments | query", query=ts_aws.rds.print_query(query))
    stream_segments = query.all()
    session.close()
    logger.info("get_clip_stream_segments | success", stream_segments=stream_segments)
    if len(stream_segments) == 0:
        raise ts_model.Exception(ts_model.Exception.CLIP_STREAM_SEGMENTS__NOT_EXIST)
    return stream_segments
