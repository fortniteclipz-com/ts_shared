import ts_model

import datetime
import sqlalchemy as sa

class Montage(ts_model.Base, ts_model.BaseMixin):
    __tablename__ = 'montages'
    montage_id = sa.Column('montage_id', sa.String(255), primary_key=True)
    user_id = sa.Column('user_id', sa.String(255))
    stream_id = sa.Column('stream_id', sa.String(255), sa.ForeignKey('streams.stream_id'))
    streamer = sa.Column('streamer', sa.String(255))
    duration = sa.Column('duration', sa.Float)
    media_key = sa.Column('media_key', sa.String(255))
    _status = sa.Column('_status', sa.Integer)
    _date_created = sa.Column('_date_created', sa.DateTime)

    def __init__(self, **kwargs):
        ts_model.Base.__init__(self, **kwargs)
        self.montage_id = kwargs.get('montage_id')
        self.user_id = kwargs.get('user_id')
        self.stream_id = kwargs.get('stream_id')
        self.streamer = kwargs.get('streamer')
        self.duration = kwargs.get('duration')
        self.media_key = kwargs.get('media_key')
        self._status = kwargs.get('_status', 0)
        self._date_created = kwargs.get('_date_created', datetime.datetime.utcnow())
