import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class StreamMoment(dict, Base):
    __tablename__ = 'stream_moments'
    stream_moment_id = sa.Column('stream_moment_id', sa.Integer, primary_key=True, autoincrement=True)
    stream_id = sa.Column('stream_id', sa.String(255), sa.ForeignKey('streams.stream_id'))
    segment = sa.Column('segment', sa.Integer)
    moment_id = sa.Column('moment_id', sa.String(255))
    time = sa.Column('time', sa.Float)
    tag = sa.Column('tag', sa.String(255))
    game = sa.Column('game', sa.String(255))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        stream_moment_id = kwargs.get('stream_moment_id')
        stream_id = kwargs.get('stream_id')
        segment = kwargs.get('segment')
        moment_id = kwargs.get('moment_id')
        time = kwargs.get('time')
        tag = kwargs.get('tag')
        game = kwargs.get('game')
