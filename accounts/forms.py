from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import User

class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('email', 'first_name',  'password1', 'password2')
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        self.instance.username = user.email

        if commit:
            user.save()
        return user

class UpdateProfileForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'avatar')



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='email')