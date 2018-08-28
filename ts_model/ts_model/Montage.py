class Montage(dict):
    def __init__(self, **kwargs):
        super(Montage, self).__init__(**kwargs)

        self.montage_id = kwargs.get('montage_id')

        self.key_playlist_audio = kwargs.get('key_playlist_audio')
        self.key_playlist_master = kwargs.get('key_playlist_master')
        self.key_playlist_video = kwargs.get('key_playlist_video')

        self.key_media_export = kwargs.get('key_media_export')

        self._status_export = kwargs.get('_status_export', 0)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
