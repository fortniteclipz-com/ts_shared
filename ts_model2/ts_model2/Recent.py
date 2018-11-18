class Recent(dict):
    def __init__(self, **kwargs):
        super(Recent, self).__init__(**kwargs)

        self.media = kwargs.get('media')
        self.media_ids = kwargs.get('media_ids')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
