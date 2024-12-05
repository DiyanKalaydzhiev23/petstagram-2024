from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


# def validate_size(value):
#     if value.size > 5 * 1024 * 1024:
#         raise ValidationError('File is too big')
#

@deconstructible
class FileSizeValidator:
    def __init__(self, file_size_mb: int, message=None):
        self.file_size_mb = file_size_mb
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = f"File size must be below or equal to {self.file_size_mb}MB"
        else:
            self.__message = value

    def __call__(self, value):
        if value.size > self.file_size_mb * 1024 * 1024:
            raise ValidationError(self.message)
