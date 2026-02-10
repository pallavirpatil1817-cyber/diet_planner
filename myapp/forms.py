from django import forms
from .models import HealthGoal, MealPlan, Recipe


class HealthGoalForm(forms.ModelForm):
    allergies = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter allergies (comma-separated)',
            'rows': 3
        }),
        required=False
    )
    dislikes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter foods you dislike (comma-separated)',
            'rows': 3
        }),
        required=False
    )

    class Meta:
        model = HealthGoal
        fields = ['user_name', 'goal', 'diet_type', 'daily_calories', 'allergies', 'dislikes']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name'
            }),
            'goal': forms.Select(attrs={'class': 'form-control'}),
            'diet_type': forms.Select(attrs={'class': 'form-control'}),
            'daily_calories': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1000',
                'max': '5000'
            }),
        }


class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Comma-separated ingredients',
            'rows': 3
        })
    )
    instructions = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Step-by-step cooking instructions',
            'rows': 5
        })
    )
    diet_types = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., vegan, keto (comma-separated)'
        }),
        required=False
    )

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'calories', 'protein_g', 'carbs_g', 'fat_g',
                  'prep_time_min', 'ingredients', 'instructions', 'diet_types', 'meal_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein_g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'carbs_g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'fat_g': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'prep_time_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
        }
