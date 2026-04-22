from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Usuario',
        validators=[MinLengthValidator(3)],
        widget=forms.TextInput(attrs={'placeholder': 'Mínimo 3 caracteres'})
    )
    email = forms.EmailField(label='Email', required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
