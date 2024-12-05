from unittest import TestCase

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from petstagram.photos.validators import FileSizeValidator


class TestFileSizeValidator(TestCase):
    def setUp(self):
        self.validator = FileSizeValidator(file_size_mb=5)

    def test_valid_file_size__expect_no_errors(self):
        small_file = SimpleUploadedFile(
            'small.txt',
            b"a" * (4 * 1024 * 1024),
        )

        try:
            self.validator(small_file)
        except ValidationError:
            self.fail('FileSize validator gave a ValidationError')

    def test_uploading_bigger_file_then_max__expect_validation_error(self):
        file = SimpleUploadedFile(
            'small.txt',
            b"a" * (6 * 1024 * 1024),
        )

        with self.assertRaises(ValidationError) as vae:
            self.validator(file)

        self.assertEqual(str(vae.exception), "['File size must be below or equal to 5MB']")

    def test_custom_message__expect_validation_error_with_custom_message(self):
        self.validator = FileSizeValidator(file_size_mb=5, message='Custom Error: file too big!')

        file = SimpleUploadedFile(
            'small.txt',
            b"a" * (6 * 1024 * 1024),
        )

        with self.assertRaises(ValidationError) as vae:
            self.validator(file)

        self.assertEqual(str(vae.exception), "['Custom Error: file too big!']")
