import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class StreamSegment(dict, Base):
    __tablename__ = 'stream_segments'
    stream_segment_id = sa.Column('stream_segment_id', sa.Integer, primary_key=True, autoincrement=True)
    stream_id = sa.Column('stream_id', sa.String(250))
    segment = sa.Column('segment', sa.Integer)
    stream_time_in = sa.Column('stream_time_in', sa.Float)
    stream_time_out = sa.Column('stream_time_out', sa.Float)
    media_url = sa.Column('media_url', sa.String(250))
    media_key = sa.Column('media_key', sa.String(250))
    _status_download = sa.Column('_status_download', sa.Integer)
    _status_analyze = sa.Column('_status_analyze', sa.Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stream_segment_id = kwargs.get('stream_segment_id')
        self.stream_id = kwargs.get('stream_id')
        self.segment = kwargs.get('segment')
        self.stream_time_in = kwargs.get('stream_time_in')
        self.stream_time_out = kwargs.get('stream_time_out')
        self.media_url = kwargs.get('media_url')
        self.media_key = kwargs.get('media_key')
        self._status_download = kwargs.get('_status_download', 0)
        self._status_analyze = kwargs.get('_status_analyze', 0)
