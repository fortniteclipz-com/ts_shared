import ts_model

class ClipSegment(ts_model.DictMixin):
    def __init__(self, **kwargs):
        self.media_key = kwargs.get('media_key')
        self.segment_time_in = kwargs.get('segment_time_in')
        self.segment_time_out = kwargs.get('segment_time_out')
