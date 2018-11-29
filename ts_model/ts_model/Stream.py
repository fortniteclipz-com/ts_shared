import ts_model

import datetime
import sqlalchemy as sa

class Stream(ts_model.BaseMixin, ts_model.Base):
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
    _status_initialize = sa.Column('_status_initialize', sa.Integer, default=0)
    _status_analyze = sa.Column('_status_analyze', sa.Integer, default=0)
    _date_created = sa.Column('_date_created', sa.DateTime, default=datetime.datetime.utcnow)
