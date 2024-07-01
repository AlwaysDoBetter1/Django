from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django_recaptcha.fields import ReCaptchaField

from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """
    User data update form
    """
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(
                                   attrs={"class": "form-control mb-1"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    first_name = forms.CharField(max_length=100,
                                 widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    last_name = forms.CharField(max_length=100,
                                widget=forms.TextInput(attrs={"class": "form-control mb-1"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        """
        Checking email for uniqueness
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email address must be unique')
        return email


class ProfileUpdateForm(forms.ModelForm):
    """
    User Profile Data Update Form
    """
    slug = forms.CharField(max_length=100,
                           widget=forms.TextInput(
                               attrs={"class": "form-control mb-1"}))
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={"class": "form-control mb-1"}))
    bio = forms.CharField(max_length=500,
                          widget=forms.Textarea(attrs={'rows': 5, "class": "form-control mb-1"}))

    avatar = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control mb-1"}))

    class Meta:
        model = Profile
        fields = ('slug', 'birth_date', 'bio', 'avatar')


class UserRegisterForm(UserCreationForm):
    """
    Overridden user registration form
    """

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def clean_email(self):
        """
        Checking email for uniqueness
        """
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('This email is already used in the system')
        return email

    def __init__(self, *args, **kwargs):
        """
        Updating Registration Form Styles
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder": "Create your own login"})
        self.fields['email'].widget.attrs.update({"placeholder": "Enter your email"})
        self.fields['first_name'].widget.attrs.update({"placeholder": "Your first name"})
        self.fields['last_name'].widget.attrs.update({"placeholder": "Your last name"})
        self.fields['password1'].widget.attrs.update({"placeholder": "Create your password"})
        self.fields['password2'].widget.attrs.update({"placeholder": "Repeat your password"})
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})

class UserLoginForm(AuthenticationForm):
    """
    Authorization form on the site
    """

    def __init__(self, *args, **kwargs):
        """
        Updating login form styles
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'User login'
        self.fields['password'].widget.attrs['placeholder'] = 'User password'
        self.fields['username'].label = 'Login'
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    recaptcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ['username', 'password', 'recaptcha']

    def __init__(self, *args, **kwargs):
        """
        Updating Registration Form Styles
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'User login'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'User password'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Login'