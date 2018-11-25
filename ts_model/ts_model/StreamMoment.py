import ts_model

import sqlalchemy as sa

class StreamMoment(ts_model.Base, ts_model.BaseMixin):
    __tablename__ = 'stream_moments'
    stream_id = sa.Column('stream_id', sa.String(255), primary_key=True)
    segment = sa.Column('segment', sa.Integer)
    time = sa.Column('time', sa.Float, primary_key=True)
    tag = sa.Column('tag', sa.String(255))

    def __init__(self, **kwargs):
        ts_model.Base.__init__(self, **kwargs)
        self.stream_moment_id = kwargs.get('stream_moment_id')
        self.stream_id = kwargs.get('stream_id')
        self.segment = kwargs.get('segment')
        self.time = kwargs.get('time')
        self.tag = kwargs.get('tag')
