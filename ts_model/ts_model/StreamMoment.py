import ts_model

import sqlalchemy as sa

class StreamMoment(ts_model.BaseMixin, ts_model.Base):
    __tablename__ = 'stream_moments'
    stream_moment_id = sa.Column('stream_moment_id', sa.Integer, primary_key=True, autoincrement=True)
    stream_id = sa.Column('stream_id', sa.String(255))
    segment = sa.Column('segment', sa.Integer)
    time = sa.Column('time', sa.Float)
    tag = sa.Column('tag', sa.String(255))
