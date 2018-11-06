class ClipSegment(dict):
    def __init__(self, **kwargs):
        super(ClipSegment, self).__init__(**kwargs)

        self.media_key = kwargs.get('media_key')
        self.segment_time_in = kwargs.get('segment_time_in')
        self.segment_time_out = kwargs.get('segment_time_out')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
