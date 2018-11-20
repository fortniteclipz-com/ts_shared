import ts_config
import ts_logger
import ts_model.Exception
import ts_model.Montage

logger = ts_logger.get(__name__)

def save_montage(montage):
    logger.info("save_montage | start", montage=montage)
    logger.info("save_montage | success")

def get_montage(montage_id):
    logger.info("get_montage | start", montage_id=montage_id)
    logger.info("get_montage | success")

def get_montages(montage_ids):
    logger.info("get_montages | start", montage_ids=montage_ids)
    logger.info("get_montages | success")

def get_user_montages(user_id):
    logger.info("get_user_montages | start", user_id=user_id)
    logger.info("get_user_montages | success")
