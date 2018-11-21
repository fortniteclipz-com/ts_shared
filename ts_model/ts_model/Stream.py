import ts_model

import datetime
import sqlalchemy as sa

class Stream(dict, ts_model.Base):
    __tablename__ = 'streams'
    stream_id = sa.Column('stream_id', sa.String(255), primary_key=True)
    streamer = sa.Column('streamer', sa.String(255))
    playlist_url = sa.Column('playlist_url', sa.String(255))
    duration = sa.Column('duration', sa.Float)
    width = sa.Column('width', sa.Integer)
    height = sa.Column('height', sa.Integer)
    fps_numerator = sa.Column('fps_numerator', sa.Integer)
    fps_denominator = sa.Column('fps_denominator', sa.Integer)
    game = sa.Column('game', sa.String(255))
    _status_initialize = sa.Column('_status_initialize', sa.Integer)
    _status_analyze = sa.Column('_status_analyze', sa.Integer)
    _date_created = sa.Column('_date_created', sa.DateTime)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stream_id = kwargs.get('stream_id')
        self.streamer = kwargs.get('streamer')
        self.playlist_url = kwargs.get('playlist_url')
        self.duration = kwargs.get('duration')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.fps_numerator = kwargs.get('fps_numerator')
        self.fps_denominator = kwargs.get('fps_denominator')
        self.game = kwargs.get('game')
        self._status_initialize = kwargs.get('_status_initialize', 0)
        self._status_analyze = kwargs.get('_status_analyze', 0)
        self._date_created = kwargs.get('_date_created', datetime.datetime.utcnow())
