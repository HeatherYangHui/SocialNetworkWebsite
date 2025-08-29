from django import forms
from .models import Profile, Post
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    """Form to update user profile details including additional user information."""
    
    class Meta:
        model = Profile
        fields = ['bio', 'picture']
        widgets = {
            'bio': forms.Textarea(attrs={'id': 'id_bio_input_text', 'rows':'3'}),
            'picture': forms.FileInput(attrs={'id':'id_profile_picture'})
        }
        labels = {
            'bio': "",
            'picture': "Upload image"
        }
    
    def clean_bio(self):
        """Validate that the bio is not too long."""
        bio = self.cleaned_data.get('bio')
        if bio and len(bio) > 500:  # Limiting bio length
            raise forms.ValidationError("Bio cannot exceed 500 characters.")
        return bio
    
class PostForm(forms.ModelForm):
    """Form to create a new post."""

    class Meta:
        model = Post
        fields = ['text']
    
    def clean_text(self):
        """Ensure posts are not empty and within a reasonable length."""
        text = self.cleaned_data.get('text')
        if not text.strip():
            raise forms.ValidationError("Post cannot be empty.")
        if len(text) > 280:  # Limiting post length like Twitter
            raise forms.ValidationError("Post cannot exceed 280 characters.")
        return text


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'id': 'id_username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'id_password'}))

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'id': 'id_password'}))
    password2 = forms.CharField(label='Confirm', widget=forms.PasswordInput(attrs={'id': 'id_confirm_password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'id': 'id_username'}),
            'email': forms.EmailInput(attrs={'id': 'id_email'}),
            'first_name': forms.TextInput(attrs={'id': 'id_first_name'}),
            'last_name': forms.TextInput(attrs={'id': 'id_last_name'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned_data
