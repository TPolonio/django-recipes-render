from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from django.utils import timezone
from .forms import RecipeForm, RecipeSearchForm

# Create your tests here.

#Create testing for views.recipe:
class RecipeViewsTest(TestCase):

    #First create dummy user and recipe
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
    # Create a test recipe
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Test description',
            author=self.user,
            ingredients='Ingredient 1, Ingredient 2',
            duration=30,
            difficulty='easy'
        )

    def test_recipe_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/home.html')

    def test_recipe_author_list_view(self):
        response = self.client.get(reverse('recipes-author', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/home.html')

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipe-detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')

    def test_recipe_create_view(self):
        response = self.client.get(reverse('recipe-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')

    def test_recipe_update_view(self):
        response = self.client.get(reverse('recipe-update', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')

    def test_recipe_delete_view(self):
        response = self.client.get(reverse('recipe-delete', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_confirm_delete.html')

    def test_recipe_search_view(self):
        response = self.client.get(reverse('recipe-search') + '?search_term=Test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_search.html')

    def test_generate_recipe_pdf_view(self):
        response = self.client.get(reverse('generate-recipe-pdf', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Disposition'), f'attachment; filename="{self.recipe.title}.pdf"')


#Create testing for models.recipe:
class RecipeModelsTest(TestCase):
    def setUp(self):
        # Create a user for the author
        self.author = User.objects.create_user(username='testuser', password='testpassword')
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='This is a test recipe',
            published_at=timezone.now(),
            author=self.author,
            ingredients='Ingredient 1, Ingredient 2',
            duration=30,
            difficulty='easy',
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.title, 'Test Recipe')
        self.assertEqual(self.recipe.description, 'This is a test recipe')
        self.assertEqual(self.recipe.author, self.author)
        self.assertEqual(self.recipe.ingredients, 'Ingredient 1, Ingredient 2')
        self.assertEqual(self.recipe.duration, 30)
        self.assertEqual(self.recipe.difficulty, 'easy')

    def test_recipe_str_method(self):
        self.assertEqual(str(self.recipe), 'Test Recipe')


#Create testing for forms.recipe:
class RecipeFormsTest(TestCase):
    def test_recipe_form_valid_data(self):
        form_data = {
            'title': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'description': 'This is a test recipe',
            'duration': 30,
            'difficulty': 'easy',
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_search_form_valid_data(self):
        form_data = {'search_term': 'Test Recipe'}
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())