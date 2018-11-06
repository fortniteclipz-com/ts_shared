class UserMontage(dict):
    def __init__(self, **kwargs):
        super(UserMontage, self).__init__(**kwargs)

        self.user_id = kwargs.get('user_id')
        self.montage_id = kwargs.get('montage_id')
        self.created = kwargs.get('created')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
