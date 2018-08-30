class Montage(dict):
    def __init__(self, **kwargs):
        super(Montage, self).__init__(**kwargs)

        self.montage_id = kwargs.get('montage_id')

        self.media_key = kwargs.get('media_key')

        self._status = kwargs.get('_status', 0)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
