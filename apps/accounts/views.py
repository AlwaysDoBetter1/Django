from django.views.generic import DetailView, UpdateView, CreateView
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.messages.views import SuccessMessageMixin

from .forms import UserRegisterForm, UserLoginForm


class ProfileDetailView(DetailView):
    """
    Profile view
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'accounts/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'User profile: {self.object.user.username}'
        return context


class ProfileUpdateView(UpdateView):
    """
    Profile editing view
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Editing a user profile: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})

class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Representation of registration on a website with a registration form
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/user_register.html'
    success_message = 'You have successfully registered. You can enter the site!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration on the site'
        return context

class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Authorization on the site
    """
    form_class = UserLoginForm
    template_name = 'accounts/user_login.html'
    next_page = 'home'
    success_message = 'Welcome to the site!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Authorization on the site'
        return context

class UserLogoutView(LogoutView):
    """
    Exit from the site
    """
    next_page = 'home'