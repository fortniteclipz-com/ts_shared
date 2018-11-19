from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ts_config

engine = None
def get_engine():
    global engine
    connection_url = "mysql+pymysql://twitchstitch:3XU8E61jvCFC@twitch-stitch-test.ctpn1m9y40sj.us-west-2.rds.amazonaws.com/twitchstitch"
    if engine is None:
        engine = create_engine(connection_url)
    return engine

def get_session():
    engine = get_engine()
    session = sessionmaker(bind = engine)
    return session()
