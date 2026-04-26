"""
Accounts Forms — Registration and Login
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# Bangladesh districts for dropdown
DISTRICTS = [
    ('', 'Select District'),
    ('Dhaka', 'Dhaka'), ('Chittagong', 'Chittagong'), ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'), ('Barisal', 'Barisal'), ('Sylhet', 'Sylhet'),
    ('Rangpur', 'Rangpur'), ('Mymensingh', 'Mymensingh'), ('Comilla', 'Comilla'),
    ('Gazipur', 'Gazipur'), ('Narayanganj', 'Narayanganj'), ('Bogra', 'Bogra'),
    ('Jessore', 'Jessore'), ('Dinajpur', 'Dinajpur'), ('Tangail', 'Tangail'),
    ('Faridpur', 'Faridpur'), ('Narsingdi', 'Narsingdi'), ('Noakhali', 'Noakhali'),
    ('Brahmanbaria', 'Brahmanbaria'), ('Kushtia', 'Kushtia'),
    ('Cox\'s Bazar', 'Cox\'s Bazar'), ('Pabna', 'Pabna'),
    ('Jamalpur', 'Jamalpur'), ('Netrokona', 'Netrokona'),
    ('Satkhira', 'Satkhira'), ('Chapainawabganj', 'Chapainawabganj'),
    ('Moulvibazar', 'Moulvibazar'), ('Habiganj', 'Habiganj'),
    ('Sunamganj', 'Sunamganj'), ('Sherpur', 'Sherpur'),
]


class RegisterForm(UserCreationForm):
    """User registration form with role selection."""

    role = forms.ChoiceField(
        choices=[('farmer', 'Farmer'), ('exporter', 'Exporter')],
        widget=forms.RadioSelect(attrs={'class': 'role-radio'}),
        initial='farmer',
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First Name',
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last Name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email Address',
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Phone Number',
        })
    )
    district = forms.ChoiceField(
        choices=DISTRICTS,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone', 'district', 'role', 'password1', 'password2',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Username',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm Password',
        })


class LoginForm(AuthenticationForm):
    """Styled login form."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
        })
    )


class ProfileForm(forms.ModelForm):
    """User profile update form."""

    district = forms.ChoiceField(
        choices=DISTRICTS,
        widget=forms.Select(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'district', 'address', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
