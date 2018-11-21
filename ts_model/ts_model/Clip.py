import datetime
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Clip(dict, Base):
    __tablename__ = 'clips'
    clip_id = sa.Column('clip_id', sa.String(255), primary_key=True)
    user_id = sa.Column('user_id', sa.String(255))
    stream_id = sa.Column('stream_id', sa.String(255), sa.ForeignKey('streams.stream_id'))
    time_in = sa.Column('time_in', sa.Float)
    time_out = sa.Column('time_out', sa.Float)
    media_key = sa.Column('media_key', sa.String(255))
    _status = sa.Column('_status', sa.Integer)
    _date_created = sa.Column('_date_created', sa.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clip_id = kwargs.get('clip_id')
        self.user_id = kwargs.get('user_id')
        self.stream_id = kwargs.get('stream_id')
        self.time_in = kwargs.get('time_in')
        self.time_out = kwargs.get('time_out')
        self.media_key = kwargs.get('media_key')
        self._status = kwargs.get('_status', 0)
        self._date_created = kwargs.get('_date_created', datetime.datetime.utcnow())
