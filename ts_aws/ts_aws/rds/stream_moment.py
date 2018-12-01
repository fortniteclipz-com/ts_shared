import ts_aws.rds
import ts_logger
import ts_model.StreamMoment

logger = ts_logger.get(__name__)

def save_stream_moments(stream_moments):
    logger.info("save_stream_moments | start", stream_moments_length=len(stream_moments))
    with ts_aws.rds.get_session() as session:
        session.bulk_save_objects(stream_moments)
        session.commit()
    logger.info("save_stream_moments | success", stream_moments_length=len(stream_moments))

def get_stream_moments(stream):
    logger.info("get_stream_moments | start", stream=stream)
    with ts_aws.rds.get_session() as session:
        query = session \
            .query(ts_model.StreamMoment) \
            .filter_by(stream_id=stream.stream_id) \
            .order_by(ts_model.StreamMoment.time.asc())
        logger.info("get_stream_moments | query", query=ts_aws.rds.print_query(query))
        stream_moments = query.all()
    logger.info("get_stream_moments | success", stream_moments_length=len(stream_moments))
    return stream_moments
