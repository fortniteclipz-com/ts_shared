class StreamSegment(dict):
    def __init__(self, **kwargs):
        super(StreamSegment, self).__init__(**kwargs)

        self.stream_id = kwargs.get('stream_id')
        self.segment = kwargs.get('segment')

        self.padded = kwargs.get('padded')
        self.stream_time_in = kwargs.get('stream_time_in')
        self.stream_time_out = kwargs.get('stream_time_out')
        self.media_url = kwargs.get('media_url')

        self.media_key = kwargs.get('media_key')

        self._status_download = kwargs.get('_status_download', 0)
        self._status_analyze = kwargs.get('_status_analyze', 0)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
