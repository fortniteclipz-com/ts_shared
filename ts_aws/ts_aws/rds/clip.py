import ts_aws.rds
import ts_logger
import ts_model.Clip
import ts_model.Exception

logger = ts_logger.get(__name__)

def save_clip(clip):
    logger.info("save_clip | start", clip=clip)
    with ts_aws.rds.get_session() as session:
        session.merge(clip)
        session.commit()
    logger.info("save_clip | success", clip=clip)

def get_clip(clip_id):
    logger.info("get_clip | start", clip_id=clip_id)
    with ts_aws.rds.get_session() as session:
        query = session \
            .query(ts_model.Clip) \
            .filter_by(clip_id=clip_id) \
            .limit(1)
        logger.info("get_clip | query", query=ts_aws.rds.print_query(query))
        clip = query.first()
    logger.info("get_clip | success", clip=clip)
    if clip is None:
        raise ts_model.Exception(ts_model.Exception.CLIP__NOT_EXIST)
    return clip

def save_clips(clips):
    logger.info("save_clips | start", clips_length=len(clips))
    columns = [column.key for column in ts_model.Clip.__table__.columns]
    values = ', '.join(list(map(lambda ss: str(tuple([('NULL' if ss[column.key] is None else ss[column.key]) for column in ts_model.Clip.__table__.columns])), clips)))
    query = f"REPLACE INTO {ts_model.Clip.__tablename__} ({', '.join(columns)}) VALUES {values};"
    logger.info("save_clips | query", query=query)
    engine = ts_aws.rds.get_engine()
    with engine.connect() as c:
        c.execute(query)
    logger.info("save_clips | success", clips_length=len(clips))

def get_montage_clips(montage):
    logger.info("get_montage_clips | start", montage=montage)
    with ts_aws.rds.get_session() as session:
        query = session \
            .query(ts_model.Clip) \
            .join(ts_model.MontageClip, ts_model.MontageClip.clip_id == ts_model.Clip.clip_id) \
            .filter_by(montage_id=montage.montage_id) \
            .order_by(ts_model.MontageClip.clip_order.asc())
        logger.info("get_montage_clips | query", query=ts_aws.rds.print_query(query))
        montage_clips = query.all()
    logger.info("get_montage_clips | success", montage_clips_length=len(montage_clips))
    if len(montage_clips) == 0:
        raise ts_model.Exception(ts_model.Exception.MONTAGE_CLIPS__NOT_EXIST)
    return montage_clips
