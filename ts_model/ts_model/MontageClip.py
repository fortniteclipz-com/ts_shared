class MontageClip(dict):
    def __init__(self, **kwargs):
        super(MontageClip, self).__init__(**kwargs)

        self.montage_id = kwargs.get('montage_id')
        self.clip_id = kwargs.get('clip_id')

        self.clip_order = kwargs.get('clip_order')
        self.media_key = kwargs.get('media_key')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
