class Clip(dict):
    def __init__(self, **kwargs):
        super(Clip, self).__init__(**kwargs)

        self.clip_id = kwargs.get('clip_id')
        self.stream_id = kwargs.get('stream_id')
        self.time_in = kwargs.get('time_in')
        self.time_out = kwargs.get('time_out')

        self.key_playlist_audio = kwargs.get('key_playlist_audio')
        self.key_playlist_master = kwargs.get('key_playlist_master')
        self.key_playlist_video = kwargs.get('key_playlist_video')

        self.key_media_export = kwargs.get('key_media_export')

        self._status = kwargs.get('_status')
        self._status_export = kwargs.get('_status_export')

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
