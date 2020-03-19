"""
Forms Module
"""

# import necessary modules
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile, UserDrink, Ingredient, Instruction


class CreateUserDrinkForm(forms.ModelForm):
    """
    Create User Drink Form
    """

    class Meta:
        model = UserDrink
        fields = [
            'name',
            'description',
            'image'
        ]


class CreateUserDrinkIngredientForm(forms.ModelForm):
    """
    Create User Drink Ingredient Form
    """

    class Meta:
        model = Ingredient
        fields = [
            'name',
            'quantity'
        ]


class CreateUserDrinkInstructionForm(forms.ModelForm):
    """
    Create User Drink Instruction Form
    """

    class Meta:
        model = Instruction
        fields = [
            'instruction'
        ]


class ProfileUpdateForm(forms.ModelForm):
    """
    Profile Update Form
    """

    class Meta:
        model = Profile
        fields = [
            'image',
            'bio'
        ]


class UserRegisterForm(UserCreationForm):
    """
    User Register Form
    """

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
    """
    User Update Form
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]
