from django import forms
from petstagram.photos.models import Photo


class PhotoBaseForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = "__all__"


class PhotoAddForm(PhotoBaseForm):
    pass


class PhotoEditForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ['photo']


class PhotoDeleteForm(PhotoBaseForm):
    pass

