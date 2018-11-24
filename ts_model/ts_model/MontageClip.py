import ts_model

import sqlalchemy as sa

class MontageClip(ts_model.Base, ts_model.BaseMixin):
    __tablename__ = 'montage_clips'
    montage_clip_id = sa.Column('montage_clip_id', sa.Integer, primary_key=True, autoincrement=True)
    montage_id = sa.Column('montage_id', sa.String(255))
    clip_id = sa.Column('clip_id', sa.String(255))
    clip_order = sa.Column('clip_order', sa.Integer)

    def __init__(self, **kwargs):
        ts_model.Base.__init__(self, **kwargs)
        self.montage_clip_id = kwargs.get('montage_clip_id')
        self.montage_id = kwargs.get('montage_id')
        self.clip_id = kwargs.get('clip_id')
        self.clip_order = kwargs.get('clip_order')
