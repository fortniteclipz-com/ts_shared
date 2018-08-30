class ClipSegment(dict):
    def __init__(self, **kwargs):
        super(ClipSegment, self).__init__(**kwargs)

        self.clip_id = kwargs.get('clip_id')
        self.segment = kwargs.get('segment')

        self.time_in = kwargs.get('time_in')
        self.time_out = kwargs.get('time_out')
        self.stream_id = kwargs.get('stream_id')
        self.media_key = kwargs.get('media_key')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
