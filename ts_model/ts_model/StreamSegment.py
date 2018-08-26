class StreamSegment(dict):
    def __init__(self, **kwargs):
        super(StreamSegment, self).__init__(**kwargs)

        self.stream_id = kwargs.get('stream_id')
        self.segment = kwargs.get('segment')
        self.padded = kwargs.get('padded')
        self.time_duration = kwargs.get('time_duration')
        self.time_in = kwargs.get('time_in')
        self.time_out = kwargs.get('time_out')
        self.url_media_raw = kwargs.get('url_media_raw')

        self.key_media_video = kwargs.get('key_media_video')
        self.key_media_audio = kwargs.get('key_media_audio')
        self.key_packets_video = kwargs.get('key_packets_video')
        self.key_packets_audio = kwargs.get('key_packets_audio')
        self.key_media_video_fresh = kwargs.get('key_media_video_fresh')
        self.key_packets_video_fresh = kwargs.get('key_packets_video_fresh')

        self._status_download = kwargs.get('_status_download')
        self._status_fresh = kwargs.get('_status_fresh')
        self._status_analyze = kwargs.get('_status_analyze')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
