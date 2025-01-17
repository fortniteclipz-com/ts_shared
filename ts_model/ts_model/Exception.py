class Exception(Exception):
    def __init__(self, code):
        super().__init__()
        self.code = code
    def __str__(self):
        return str(self.code)

exceptions = [
    "CLIP__NOT_EXIST",
    "CLIP__STATUS_DONE",

    "CLIP_STREAM_SEGMENTS__NOT_EXIST",

    "MEDIA__NOT_EXIST",

    "MONTAGE__NOT_EXIST",
    "MONTAGE__STATUS_DONE",

    "MONTAGE_CLIPS__NOT_EXIST",
    "MONTAGE_CLIPS__STATUS_NOT_DONE",

    "STREAM__NOT_EXIST",
    "STREAM__STATUS_ANALYZE_DONE",
    "STREAM__STATUS_ANALYZE_NOT_DONE",
    "STREAM__STATUS_ANALYZE_WORKING",
    "STREAM__STATUS_INITIALIZE_DONE",
    "STREAM__STATUS_INITIALIZE_ERROR",
    "STREAM__STATUS_INITIALIZE_NOT_DONE",

    "STREAM_ID__NOT_VALID",

    "STREAM_MOMENTS__GAME_NOT_SUPPORTED",

    "STREAM_SEGMENT__NOT_EXIST",
    "STREAM_SEGMENT__STATUS_ANALYZE_DONE",
    "STREAM_SEGMENT__STATUS_DOWNLOAD_DONE",
    "STREAM_SEGMENT__STATUS_DOWNLOAD_NOT_DONE",

    "STREAM_SEGMENTS__NOT_EXIST",
    "STREAM_SEGMENTS__STATUS_DOWNLOAD_NOT_DONE",
]

for e in exceptions:
    setattr(Exception, e, e)
