import ts_model

import datetime
import sqlalchemy as sa

class Montage(ts_model.BaseMixin, ts_model.Base):
    __tablename__ = 'montages'
    montage_id = sa.Column('montage_id', sa.String(255), primary_key=True)
    user_id = sa.Column('user_id', sa.String(255))
    stream_id = sa.Column('stream_id', sa.String(255))
    streamer = sa.Column('streamer', sa.String(255))
    duration = sa.Column('duration', sa.Float)
    clips = sa.Column('clips', sa.Integer)
    media_key = sa.Column('media_key', sa.String(255))
    _status = sa.Column('_status', sa.Integer, default=0)
    _date_created = sa.Column('_date_created', sa.DateTime, default=datetime.datetime.utcnow())
