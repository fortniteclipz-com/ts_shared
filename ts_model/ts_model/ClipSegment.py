class ClipSegment(dict):
    def __init__(self, **kwargs):
        super(ClipSegment, self).__init__(**kwargs)

        self.clip_id = kwargs.get('clip_id')
        self.segment = kwargs.get('segment')

        self.audio_packets_byterange = kwargs.get('audio_packets_byterange')
        self.audio_packets_pos = kwargs.get('audio_packets_pos')
        self.audio_time_duration = kwargs.get('audio_time_duration')
        self.audio_time_out = kwargs.get('audio_time_out')
        self.audio_time_in = kwargs.get('audio_time_in')
        self.audio_url_media = kwargs.get('audio_url_media')
        self.video_packets_byterange = kwargs.get('video_packets_byterange')
        self.video_packets_pos = kwargs.get('video_packets_pos')
        self.video_time_duration = kwargs.get('video_time_duration')
        self.video_time_out = kwargs.get('video_time_out')
        self.video_time_in = kwargs.get('video_time_in')
        self.video_url_media = kwargs.get('video_url_media')

        self.discontinuity = kwargs.get('discontinuity')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
