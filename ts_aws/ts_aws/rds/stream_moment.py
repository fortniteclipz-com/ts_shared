import ts_aws.rds
import ts_logger
import ts_model.StreamMoment

import sqlalchemy.dialects

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
    query = session \
        .query(ts_model.StreamMoment) \
        .filter_by(stream_id=stream.stream_id) \
        .order_by(ts_model.StreamMoment.time)
    logger.info("get_stream_moments | query", query=query.statement.compile(dialect=sqlalchemy.dialects.mysql.dialect(), compile_kwargs={'literal_binds': True}))
    stream_moments = query.all()
    session.close()
    logger.info("get_stream_moments | success", stream_moments_length=len(stream_moments))
    return stream_moments
