import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Montage(dict, Base):
    __tablename__ = 'montages'
    montage_id = sa.Column('montage_id', sa.String(250), primary_key=True)
    user_id = sa.Column('user_id', sa.String(250))
    stream_id = sa.Column('stream_id', sa.String(250))
    streamer = sa.Column('streamer', sa.String(250))
    duration = sa.Column('duration', sa.Float)
    media_key = sa.Column('media_key', sa.String(250))
    _status = sa.Column('_status', sa.Integer)
    _date_created = sa.Column('_date_created', sa.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.montage_id = kwargs.get('montage_id')
        self.user_id = kwargs.get('user_id')
        self.stream_id = kwargs.get('stream_id')
        self.streamer = kwargs.get('streamer')
        self.duration = kwargs.get('duration')
        self.media_key = kwargs.get('media_key')
        self._status = kwargs.get('_status')
        self._date_created = kwargs.get('_date_created')
