import ts_aws.rds
import ts_logger
import ts_model.Exception
import ts_model.MontageClip

logger = ts_logger.get(__name__)

def save_montage_clips(montage_clips):
    logger.info("save_montage_clips | start", montage_clips_length=len(montage_clips))
    columns = [column.key for column in ts_model.MontageClip.__table__.columns]
    values = ', '.join(list(map(lambda ss: str(tuple([('NULL' if ss[column.key] is None else ss[column.key]) for column in ts_model.MontageClip.__table__.columns])), stream_segments)))
    query = f"REPLACE INTO {ts_model.MontageClip.__tablename__} ({', '.join(columns)}) VALUES {values};"
    logger.info("save_stream_segments | query", query=query)
    engine = ts_aws.rds.get_engine()
    with engine.connect() as c:
        c.execute(query)
    logger.info("save_montage_clips | success", montage_clips_length=len(montage_clips))
