class UserClip(dict):
    def __init__(self, **kwargs):
        super(ClipSegment, self).__init__(**kwargs)

        self.user_id = kwargs.get('user_id')
        self.clip_id = kwargs.get('clip_id')
        self.created = kwargs.get('created')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
