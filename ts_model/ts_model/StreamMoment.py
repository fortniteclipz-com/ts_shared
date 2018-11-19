class StreamMoment(dict):
    def __init__(self, **kwargs):
        super(StreamMoment, self).__init__(**kwargs)

        self.stream_moment_id = kwargs.get('stream_moment_id')
        self.stream_id = kwargs.get('stream_id')
        self.segment = kwargs.get('segment')
        self.moment_id = kwargs.get('moment_id')
        self.time = kwargs.get('time')
        self.tag = kwargs.get('tag')
        self.game = kwargs.get('game')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
