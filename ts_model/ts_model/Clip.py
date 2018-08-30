class Clip(dict):
    def __init__(self, **kwargs):
        super(Clip, self).__init__(**kwargs)

        self.clip_id = kwargs.get('clip_id')

        self.stream_id = kwargs.get('stream_id')
        self.time_in = kwargs.get('time_in')
        self.time_out = kwargs.get('time_out')

        self.key_media = kwargs.get('key_media')

        self._status = kwargs.get('_status', 0)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
