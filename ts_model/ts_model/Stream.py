class Stream(dict):
    def __init__(self, **kwargs):
        super(Stream, self).__init__(**kwargs)

        self.stream_id = kwargs.get('stream_id')

        self.streamer = kwargs.get('streamer')
        self.game = kwargs.get('game')
        self.playlist_url = kwargs.get('playlist_url')
        self.duration = kwargs.get('duration')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.fps_numerator = kwargs.get('fps_numerator')
        self.fps_denominator = kwargs.get('fps_denominator')

        self._status_initialize = kwargs.get('_status_initialize', 0)
        self._status_analyze = kwargs.get('_status_analyze', 0)
        self._created = kwargs.get('_created')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
