class StreamSegment(dict):
    def __init__(self, **kwargs):
        super(StreamSegment, self).__init__(**kwargs)

        self.stream_id = kwargs.get('stream_id')
        self.segment = kwargs.get('segment')

        self.padded = kwargs.get('padded')
        self.time_duration = kwargs.get('time_duration')
        self.time_in = kwargs.get('time_in')
        self.time_out = kwargs.get('time_out')
        self.media_url = kwargs.get('media_url')

        self.media_key = kwargs.get('media_key')

        self._status_download = kwargs.get('_status_download', 0)
        self._status_analyze = kwargs.get('_status_analyze', 0)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
