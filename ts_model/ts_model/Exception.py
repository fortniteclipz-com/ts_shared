class Exception(Exception):
    def __init__(self, code):
        super().__init__()
        self.code = code
    def __str__(self):
        return str(self.code)

    STREAM_NOT_EXISTS = "STREAM_NOT_EXISTS"
    STREAM_NOT_READY = "STREAM_NOT_READY"
    STREAM_SEGMENTS_NOT_READY = "STREAM_SEGMENTS_NOT_READY"

    CLIP_NOT_EXISTS = "CLIP_NOT_EXISTS"
    CLIP_ALREADY_PROCESSED = "CLIP_ALREADY_PROCESSED"
