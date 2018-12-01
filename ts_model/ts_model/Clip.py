import ts_model

import datetime
import sqlalchemy as sa

class Clip(ts_model.BaseMixin, ts_model.Base):
    __tablename__ = 'clips'
    clip_id = sa.Column('clip_id', sa.String(255), primary_key=True)
    user_id = sa.Column('user_id', sa.String(255))
    stream_id = sa.Column('stream_id', sa.String(255))
    time_in = sa.Column('time_in', sa.Float)
    time_out = sa.Column('time_out', sa.Float)
    media_key = sa.Column('media_key', sa.String(255))
    _status = sa.Column('_status', sa.Integer, default=0)
    _date_created = sa.Column('_date_created', sa.DateTime, default=datetime.datetime.utcnow)
