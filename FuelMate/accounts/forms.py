from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        help_text="*Maksymalnie 150 znaków. Można używać liter, cyfr oraz znaków @/./+/-/_",
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Dodano form-control
    )
    password1 = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),  # Dodano form-control
        help_text="*Hasło musi mieć conajmniej 8 znaków, zawierać dużą literę oraz znak specjalny."
    )
    password2 = forms.CharField(
        label='Powtórz hasło',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})  # Dodano form-control
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})  # Dodano form-control
    )
    first_name = forms.CharField(
        max_length=30,
        label="Imię",
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Dodano form-control
    )
    last_name = forms.CharField(
        max_length=150,
        label="Nazwisko",
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Dodano form-control
    )
    city = forms.CharField(
        max_length=100,
        label="Miasto",
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Dodano form-control
    )
    postal_code = forms.CharField(
        max_length=6,
        help_text="*Format: XX-XXX",
        validators=[
            RegexValidator(
                regex=r'^\d{2}-\d{3}$',
                message="Zły kod pocztowy! Kod musi mieć format XX-XXX, np. 01-234.",
                code='invalid_postal_code'
            )
        ],
        label="Kod Pocztowy",
        widget=forms.TextInput(attrs={'class': 'form-control'})  # Dodano form-control
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1)
        if len(password1) < 8:
            raise ValidationError("Hasło musi mieć conajmniej 8 znaków.")
        if len(password1) > 32:
            raise ValidationError("Hasło musi być krótsze niż 32 znaki.")
        if not any(char.isupper() for char in password1):
            raise ValidationError("Hasło musi zawierać conajmniej jedną dużą literę.")
        if not any(char in '!@#$%^&*()_+-=[]{}|;:\'",.<>?/' for char in password1):
            raise ValidationError("Hasło musi zawierać conajmniej jeden znak specjalny.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Podane hasła nie są takie same.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            user.profile.city = self.cleaned_data['city']
            user.profile.postal_code = self.cleaned_data['postal_code']
            user.profile.save()
        return user
