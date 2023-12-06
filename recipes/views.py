from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User  
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from .models import Recipe
from .forms import RecipeForm, RecipeSearchForm
from django.db.models import Q
import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.shortcuts import get_object_or_404


# Using Class Based Views
# Django already has List, Detailed, Create, Update, Delete.... Views 

class RecipeListView(ListView):
    model = Recipe 
    form_class = RecipeSearchForm
    template_name = 'recipes/home.html' #Change the template Django looks for 
    context_object_name = 'recipes' #Without this, Django looks for "object" 
    ordering = ['-published_at'] #Order from latest to oldest
    paginate_by = 6 #4 recipes per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Create an instance of the search form
        return context

class RecipeAuthorListView(ListView):
    model = Recipe 
    form_class = RecipeSearchForm
    template_name = 'recipes/home.html' #Change the template Django looks for 
    context_object_name = 'recipes' #Without this, Django looks for "object" 
    ordering = ['-published_at'] #Order from latest to oldest
    paginate_by = 4 #4 recipes per page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Create an instance of the search form
        return context
    
    def get_queryset(self):
        # Get the username from the URL parameter
        author_username = self.kwargs['author']

        # Get the User instance with the matching username
        user = User.objects.get(username=author_username)

        # Filter recipes based on the username
        queryset = Recipe.objects.filter(author=user)

        return queryset


class RecipeDetailView(DetailView):
    model = Recipe 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredients = context['object'].ingredients.split(',')
        context['ingredients'] = [ingredient.strip() for ingredient in ingredients]
        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self): #checks if logged user is author of recipe
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        else: 
            return False

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/'


    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        else: 
            return False

class RecipeSearchView(ListView):
    model = Recipe
    form_class = RecipeSearchForm
    template_name = 'recipes/recipe_search.html'
    context_object_name = 'recipes'
    ordering = ['-published_at'] #Order from latest to oldest
    paginate_by = 4 #4 recipes per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()  # Create an instance of the search form
        return context


    def get_queryset(self):
        search_term = self.request.GET.get('search_term')
        if search_term:
            return Recipe.objects.filter(title__icontains=search_term)
        return Recipe.objects.none()
    

def generate_recipe_pdf(request, recipe_id):

    recipe = Recipe.objects.get(pk=recipe_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{recipe.title}.pdf"'

    # Use the default portrait page size (letter)
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Define the widths, margin and fontsize
    left_margin = 50
    text_width = 150
    font_size = 12  # Adjust as needed

    # Create a story to hold the content
    story = []

    # Create a custom style with the desired font size
    custom_style = ParagraphStyle(name="CustomStyle", parent=getSampleStyleSheet()["Normal"])
    custom_style.fontSize = font_size

   # Title and author
    title_text = f"<b>Title:</b> {recipe.title}"
    author_text = f"<b>Author</b>: {recipe.author.username}"
    story.append(Paragraph(title_text, custom_style))
    story.append(Paragraph(author_text, custom_style))
    story.append(Spacer(1, 12))  # Add space between lines

    # Duration and Difficulty
    duration_text = f"<b>Duration</b>: {recipe.duration} minutes"
    # Capitalize the first letter of difficulty
    difficulty_text = f"<b>Difficulty</b>: {recipe.difficulty.capitalize()}"
    story.append(Paragraph(duration_text, custom_style))
    story.append(Paragraph(difficulty_text, custom_style))
    story.append(Spacer(1, 12))

    # Ingredients (multiline)
    ingredients_text = f"<b>Ingredients</b>: {recipe.ingredients}"
    ingredients_lines = ingredients_text.splitlines()
    for line in ingredients_lines:
        story.append(Paragraph(line, custom_style))
    story.append(Spacer(1, 12))

    # Description (multiline, wraps to new line)
    description_text = f"<b>Description</b>: {recipe.description}"
    story.append(Paragraph(description_text, custom_style))

    # Build the PDF document
    doc.build(story)
    return response