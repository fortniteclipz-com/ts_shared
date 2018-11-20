import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Clip(dict, Base):
    __tablename__ = 'clips'
    clip_id = sa.Column('clip_id', sa.String(250), primary_key=True)
    stream_id = sa.Column('stream_id', sa.String(250))
    time_in = sa.Column('time_in', sa.Float)
    time_out = sa.Column('time_out', sa.Float)
    media_key = sa.Column('media_key', sa.String(250))
    _status = sa.Column('_status', sa.Integer)
    _created = sa.Column('_created', sa.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clip_id = kwargs.get('clip_id')
        self.stream_id = kwargs.get('stream_id')
        self.time_in = kwargs.get('time_in')
        self.time_out = kwargs.get('time_out')
        self.media_key = kwargs.get('media_key')
        self._status = kwargs.get('_status')
        self._created = kwargs.get('_created')
