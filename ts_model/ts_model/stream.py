class Stream():
    def __init__(self, **kwargs):
        self.stream_id = kwargs.get('stream_id')
        self.time_offset = kwargs.get('time_offset')
        self.url_playlist_raw = kwargs.get('url_playlist_raw')

        self._status = kwargs.get('_status')

