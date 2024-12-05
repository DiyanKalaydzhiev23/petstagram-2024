from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from petstagram.photos.models import Photo

UserModel = get_user_model()

class TestPhotoDelete(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@test.com',
            password='password'
        )

        self.other_user = UserModel.objects.create_user(
            email='test2@test.com',
            password='password'
        )

        self.photo = Photo.objects.create(
            photo="my_photo.png",
            description="Cute photo",
            location="Test",
            user=self.user,
        )

        self.client.login(
            email='test@test.com',
            password='password'
        )

    def test_photo_delete__from_author_user__expect_in_success(self):
        self.assertTrue(Photo.objects.filter(pk=self.photo.pk).exists())

        response = self.client.post(
            reverse('photo-delete', kwargs={'pk': self.photo.pk})
        )

        self.assertFalse(Photo.objects.filter(pk=self.photo.pk).exists())
        self.assertRedirects(response, reverse('home'))

    def test_photo_delete__from_non_author_user__expect_photo_to_not_be_deleted(self):
        self.client.login(
            email='test2@test.com',
            password='password'
        )

        response = self.client.post(
            reverse('photo-delete', kwargs={'pk': self.photo.pk})
        )

        self.assertTrue(Photo.objects.filter(pk=self.photo.pk).exists())
        self.assertRedirects(response, reverse('home'))

    def test_photo_delete__from_anonymous_user__expect_redirect_to_login(self):
        self.client.logout()

        response = self.client.post(
            reverse('photo-delete', kwargs={'pk': self.photo.pk})
        )

        self.assertTrue(Photo.objects.filter(pk=self.photo.pk).exists())
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('photo-delete', kwargs={'pk': self.photo.pk})}")