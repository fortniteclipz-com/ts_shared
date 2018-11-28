import ts_model

import sqlalchemy as sa

class StreamSegment(ts_model.BaseMixin, ts_model.Base):
    __tablename__ = 'stream_segments'
    stream_id = sa.Column('stream_id', sa.String(255), primary_key=True)
    segment = sa.Column('segment', sa.Integer, primary_key=True)
    stream_time_in = sa.Column('stream_time_in', sa.Float)
    stream_time_out = sa.Column('stream_time_out', sa.Float)
    media_url = sa.Column('media_url', sa.String(255))
    media_key = sa.Column('media_key', sa.String(255))
    _status_download = sa.Column('_status_download', sa.Integer, default=0)
    _status_analyze = sa.Column('_status_analyze', sa.Integer, default=0)
