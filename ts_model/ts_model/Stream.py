class Stream(dict):
    def __init__(self, **kwargs):
        super(Stream, self).__init__(**kwargs)

        self.stream_id = kwargs.get('stream_id')

        self.playlist_url = kwargs.get('playlist_url')
        self.fps = kwargs.get('fps')

        self._status_initialize = kwargs.get('_status_initialize', 0)
        self._status_analyze = kwargs.get('_status_analyze', 0)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
