import ts_model

import sqlalchemy as sa

class StreamMoment(ts_model.Base, ts_model.BaseMixin):
    __tablename__ = 'stream_moments'
    stream_moment_id = sa.Column('stream_moment_id', sa.Integer, primary_key=True, autoincrement=True)
    stream_id = sa.Column('stream_id', sa.String(255), sa.ForeignKey('streams.stream_id'))
    segment = sa.Column('segment', sa.Integer)
    moment_id = sa.Column('moment_id', sa.String(255))
    time = sa.Column('time', sa.Float)
    tag = sa.Column('tag', sa.String(255))
    game = sa.Column('game', sa.String(255))

    def __init__(self, **kwargs):
        ts_model.Base.__init__(self, **kwargs)
        self.stream_moment_id = kwargs.get('stream_moment_id')
        self.stream_id = kwargs.get('stream_id')
        self.segment = kwargs.get('segment')
        self.moment_id = kwargs.get('moment_id')
        self.time = kwargs.get('time')
        self.tag = kwargs.get('tag')
        self.game = kwargs.get('game')
