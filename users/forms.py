from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinLengthValidator
from .models import User

class EmailUserCreationForm(UserCreationForm):
    """Registro pidiendo email, username y password."""
    username = forms.CharField(
        label='Usuario',
        validators=[MinLengthValidator(3)],
        widget=forms.TextInput(attrs={'placeholder': 'Mínimo 3 caracteres'})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'email@ejemplo.com'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # username ya se asigna automáticamente por UserCreationForm
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    """Login usando email como identificador."""
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'email@ejemplo.com'})
    )

    def clean_username(self):
        """El campo username contiene el email para autenticación."""
        return self.cleaned_data['username']

