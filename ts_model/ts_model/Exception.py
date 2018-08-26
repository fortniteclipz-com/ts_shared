class Exception(Exception):
    def __init__(self, code):
        super().__init__()
        self.code = code
    def __str__(self):
        return str(self.code)

    STREAM_NOT_EXIST = "STREAM_NOT_EXIST"
    STREAM_NOT_READY = "STREAM_NOT_READY"
    STREAM_SEGMENTS_NOT_READY = "STREAM_SEGMENTS_NOT_READY"
    STREAM_ALREADY_PROCESSED = "STREAM_ALREADY_PROCESSED"

    CLIP_NOT_EXIST = "CLIP_NOT_EXIST"
    CLIP_ALREADY_PROCESSED = "CLIP_ALREADY_PROCESSED"

    STREAM_SEGMENT_NOT_EXISTS = "STREAM_SEGMENTS_NOT_EXISTS"
