import ts_aws.rds
import ts_logger
import ts_model.Exception
import ts_model.Montage

logger = ts_logger.get(__name__)

def save_montage(montage):
    logger.info("save_montage | start", montage=montage)
    session = ts_aws.rds.get_session()
    session.merge(montage)
    session.commit()
    session.close()
    logger.info("save_montage | success", montage=montage)

def get_montage(montage_id):
    logger.info("get_montage | start", montage_id=montage_id)
    session = ts_aws.rds.get_session()
    montage = session \
    .query(ts_model.Montage) \
    .filter_by(montage_id=montage_id) \
    .first()
    session.close()
    logger.info("get_montage | success", montage=montage)
    if montage is None:
        raise ts_model.Exception(ts_model.Exception.MONTAGE__NOT_EXIST)
    return montage

def get_montages():
    logger.info("get_montages | start")
    session = ts_aws.rds.get_session()
    montages = session \
    .query(ts_model.Montage) \
    .order_by(ts_model.Montage._date_created) \
    .limit(25) \
    .all()
    logger.info("get_montages | success", montages_length=len(montages))
    return montages

def get_user_montages(user_id):
    logger.info("get_user_montages | start", user_id=user_id)
    session = ts_aws.rds.get_session()
    montages = session \
    .query(ts_model.Montage) \
    .filter_by(user_id=user_id) \
    .order_by(ts_model.Montage._date_created) \
    .limit(25) \
    .all()
    logger.info("get_user_montages | success", montages_length=len(montages))
    return montages
