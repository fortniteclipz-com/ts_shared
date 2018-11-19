import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stream(Base):
    __tablename__ = 'streams'
    stream_id = sa.Column('stream_id', sa.String(250), primary_key=True)
    streamer = sa.Column('streamer', sa.String(250))
    playlist_url = sa.Column('playlist_url', sa.String(250))
    duration = sa.Column('duration', sa.Float)
    width = sa.Column('width', sa.Integer)
    height = sa.Column('height', sa.Integer)
    fps_numerator = sa.Column('fps_numerator', sa.Integer)
    fps_denominator = sa.Column('fps_denominator', sa.Integer)
    game = sa.Column('game', sa.String(250))

    _status_initialize = sa.Column('_status_initialize', sa.Integer)
    _status_analyze = sa.Column('_status_analyze', sa.Integer)
    _created = sa.Column('_created', sa.DateTime)


