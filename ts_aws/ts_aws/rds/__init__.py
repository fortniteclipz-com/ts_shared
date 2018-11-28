import sqlalchemy.dialects
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ts_config
import ts_logger

logger = ts_logger.get(__name__)
engine = None

def get_engine():
    global engine
    username = ts_config.get('rds.username')
    password = ts_config.get('rds.password')
    stage = ts_config.get('stage')
    host = ts_config.get('rds.host')
    db = ts_config.get('rds.db')
    connection_url = f"mysql+pymysql://{username}:{password}@twitch-stitch-{stage}.{host}/{db}"
    logger.info("connection_url", connection_url=connection_url)
    if engine is None:
        engine = create_engine(connection_url)
    return engine

def get_session():
    engine = get_engine()
    session = sessionmaker(bind = engine)
    return session()

def print_query(query):
    return str(query.statement.compile(dialect=sqlalchemy.dialects.mysql.dialect(), compile_kwargs={'literal_binds': True})).replace('\n', ' ').replace('\r', '')
