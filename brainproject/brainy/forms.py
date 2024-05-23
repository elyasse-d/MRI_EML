from django.contrib.auth.forms import UserCreationForm , AuthenticationForm , UsernameField , PasswordChangeForm , SetPasswordForm, PasswordResetForm ,UserChangeForm, PasswordChangeForm
from .models import CustomUser ,Profile
from django.core.validators import RegexValidator
from django import forms
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus ':'True','class':'text-iwhite w-full px-4 py-2 bg-iblack  border-b-2 border-b-gray-500 focus:outline-none font-helvetica-ultra-light','placeholder':'password'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'text-iwhite w-full px-4 py-2 bg-iblack  border-b-2 border-b-gray-500 focus:outline-none font-helvetica-ultra-light','placeholder':'password'}))


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^(?:(?:(?:\+|00)212[\s]?(?:[\s]?\(0\)[\s]?)?)|0){1}(?:5[\s.-]?[2-3]|6[\s.-]?[13-9]){1}[0-9]{1}(?:[\s.-]?\d{2}){3}$',
                message="Phone number must be entered in the format: '+212 5x xx xx xx' or '00 212 5x xx xx xx'. Up to 20 digits allowed."
            )
        ]
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password1', 'password2']

GENDER=(
    ("Male","M",),
    ("Female","F"),
)
class ProfileEditForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'file-input'
    }), required=False)
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'
    }))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'
    }))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'
    }))
    birthdate = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date',
        'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'
    }), required=False)
    gender = forms.ChoiceField(choices=GENDER, required=False, widget=forms.Select(attrs={
        'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500'
    }))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500',
        'rows': 4  # Adjust the number of rows as needed
    }))

    class Meta:
        model = Profile
        fields = ['profile_picture', 'birthdate', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'gender', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['phone_number'].initial = user.phone_number
            self.fields['birthdate'].initial = user.profile.birthdate
            self.fields['gender'].initial = user.profile.gender
            self.fields['description'].initial = user.profile.description

            # Setting placeholders with initial values
            self.fields['first_name'].widget.attrs['placeholder'] = user.first_name or ''
            self.fields['last_name'].widget.attrs['placeholder'] = user.last_name or ''
            self.fields['email'].widget.attrs['placeholder'] = user.email or ''
            self.fields['phone_number'].widget.attrs['placeholder'] = user.phone_number or ''
            self.fields['birthdate'].widget.attrs['placeholder'] = user.profile.birthdate or ''
            self.fields['description'].widget.attrs['placeholder'] = user.profile.description or ''
        
        self.fields['password'].widget = forms.PasswordInput()

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user

        # Update user fields only if new values are provided
        if self.cleaned_data.get('first_name'):
            user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data.get('last_name'):
            user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data.get('email'):
            user.email = self.cleaned_data['email']
        if self.cleaned_data.get('phone_number'):
            user.phone_number = self.cleaned_data['phone_number']
        
        # Update profile fields only if new values are provided
        if self.cleaned_data.get('birthdate'):
            profile.birthdate = self.cleaned_data['birthdate']
        if self.cleaned_data.get('gender'):
            profile.gender = self.cleaned_data['gender']
        if self.cleaned_data.get('description'):
            profile.description = self.cleaned_data['description']
        if self.cleaned_data.get('profile_picture'):
            profile.profile_picture = self.cleaned_data['profile_picture']

        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])

        user.save()

        if commit:
            profile.save()
        return profile


