from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from petstagram.common.forms import CommentForm
from petstagram.pets.forms import PetAddForm, PetEditForm, PetDeleteForm
from petstagram.pets.models import Pet


class PetAddPage(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetAddForm
    template_name = 'pets/pet-add-page.html'

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.request.user.pk,
            }
        )


class PetEditPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Pet
    template_name = 'pets/pet-edit-page.html'
    form_class = PetEditForm
    slug_url_kwarg = 'pet_slug'

    def test_func(self):
        pet = get_object_or_404(Pet, slug=self.kwargs['pet_slug'])
        return self.request.user == pet.user

    def get_success_url(self):
        return reverse_lazy(
            'pet-details',
            kwargs={
                'username': self.kwargs['username'],
                'pet_slug': self.kwargs['pet_slug'],
            }
        )

class PetDeletePage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Pet
    template_name = 'pets/pet-delete-page.html'
    slug_url_kwarg = 'pet_slug'
    form_class = PetDeleteForm

    def get_success_url(self):
        return reverse_lazy(
            'profile-details',
            kwargs={
                'pk': self.request.user.pk,
            }
        )

    def test_func(self):
        pet = get_object_or_404(Pet, slug=self.kwargs['pet_slug'])
        return self.request.user == pet.user

    def get_initial(self) -> dict:
        return self.get_object().__dict__

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'data': self.get_initial(),
        })

        return kwargs


class PetDetailsPage(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = 'pets/pet-details-page.html'
    slug_url_kwarg = 'pet_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_photos'] = context['pet'].photo_set.all()
        context['comment_form'] = CommentForm()

        all_photos = context['pet'].photo_set.all()

        for photo in all_photos:
            photo.has_liked = photo.like_set.filter(user=self.request.user).exists()

        context['all_photos'] = all_photos

        return context
