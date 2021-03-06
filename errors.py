class MajorError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class MinorError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class NoDriverError(MajorError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class GetPageError(MajorError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ImageDownloadError(MinorError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class ImageSaveError(MinorError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class NotAllowedUrlFormatError(MajorError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class SaveError(MajorError):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
