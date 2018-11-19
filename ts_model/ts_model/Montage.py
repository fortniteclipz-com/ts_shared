class Montage(dict):
    def __init__(self, **kwargs):
        super(Montage, self).__init__(**kwargs)

        self.montage_id = kwargs.get('montage_id')
        self.user_id = kwargs.get('user_id')
        self.stream_id = kwargs.get('stream_id')
        self.streamer = kwargs.get('streamer')
        self.duration = kwargs.get('duration')
        self.media_key = kwargs.get('media_key')

        self._status = kwargs.get('_status', 0)
        self._created = kwargs.get('_status')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
