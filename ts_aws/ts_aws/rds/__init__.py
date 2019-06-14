import sqlalchemy.dialects
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ts_config
import ts_logger

logger = ts_logger.get(__name__)
engine = None

def get_engine():
    global engine
    if engine is None:
        username = ts_config.get('rds.username')
        password = ts_config.get('rds.password')
        stage = ts_config.get('stage')
        host = ts_config.get('rds.host')
        db = ts_config.get('rds.db')
        connection_url = f"mysql+pymysql://{username}:{password}@ts-{stage}.{host}/{db}"
        logger.info("connection_url", connection_url=connection_url)
        engine = create_engine(connection_url)
    return engine

@contextmanager
def get_session():
    engine = get_engine()
    Session = sessionmaker(bind = engine)
    session = Session()
    yield session
    session.close()

def print_query(query):
    return str(query.statement.compile(dialect=sqlalchemy.dialects.mysql.dialect(), compile_kwargs={'literal_binds': True})).replace('\n', ' ').replace('\r', '')
