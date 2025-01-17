import ts_aws.rds
import ts_logger
import ts_model.Exception
import ts_model.Status
import ts_model.Stream

logger = ts_logger.get(__name__)

def save_stream(stream):
    logger.info("save_stream | start", stream=stream)
    with ts_aws.rds.get_session() as session:
        session.merge(stream)
        session.commit()
    logger.info("save_stream | success", stream=stream)

def get_stream(stream_id):
    logger.info("get_stream | start", stream_id=stream_id)
    with ts_aws.rds.get_session() as session:
        query = session \
            .query(ts_model.Stream) \
            .filter_by(stream_id=stream_id) \
            .limit(1)
        logger.info("get_stream | query", query=ts_aws.rds.print_query(query))
        stream = query.first()
    logger.info("get_stream | success", stream=stream)
    if stream is None:
        raise ts_model.Exception(ts_model.Exception.STREAM__NOT_EXIST)
    return stream

def get_streams():
    logger.info("get_streams | start")
    with ts_aws.rds.get_session() as session:
        query = session \
            .query(ts_model.Stream) \
            .filter_by(_status_analyze=ts_model.Status.DONE) \
            .order_by(ts_model.Stream._date_created.desc()) \
            .limit(15)
        logger.info("get_streams | query", query=ts_aws.rds.print_query(query))
        streams = query.all()
    logger.info("get_streams | success", streams_length=len(streams))
    return streams
