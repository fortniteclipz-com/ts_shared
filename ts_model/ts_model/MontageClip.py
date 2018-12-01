import ts_model

import sqlalchemy as sa

class MontageClip(ts_model.BaseMixin, ts_model.Base):
    __tablename__ = 'montage_clips'
    montage_id = sa.Column('montage_id', sa.String(255), primary_key=True)
    clip_id = sa.Column('clip_id', sa.String(255), primary_key=True)
    clip_order = sa.Column('clip_order', sa.Integer)
