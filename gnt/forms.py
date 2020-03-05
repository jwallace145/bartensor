from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, User_drink, Ingredient, Instruction


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'image',
            'bio'
        ]


class CreateUserDrinkForm(forms.ModelForm):
    class Meta:
        model = User_drink
        fields = [
            'name',
            'description'
        ]


class CreateUserDrinkIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            'name',
            'quantity'
        ]


class CreateUserDrinkInstructionForm(forms.ModelForm):
    class Meta:
        model = Instruction
        fields = [
            'instruction'
        ]
