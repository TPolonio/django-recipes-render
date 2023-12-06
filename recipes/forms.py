from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'description', 'duration','difficulty']
        labels = {
            'ingredients': 'Ingredients* (Please separate ingredients with commas)',  # Change the label here
            'duration': 'Duration* (Please enter duration in minutes)'
        }

class RecipeSearchForm(forms.Form):
    search_term = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Search for recipes'}),
        label=False,
    )