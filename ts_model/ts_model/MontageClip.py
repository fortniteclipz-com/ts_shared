class MontageClip():
    def __init__(self, **kwargs):
        self.montage_id = kwargs.get('montage_id')
        self.clip_id = kwargs.get('clip_id')
        self.clip_order = kwargs.get('clip_order')
