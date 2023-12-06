from django.urls import path
from . import views
from .views import (RecipeListView,
                    RecipeAuthorListView,
                    RecipeDetailView, 
                    RecipeCreateView,
                    RecipeUpdateView,
                    RecipeDeleteView,
                    RecipeSearchView,
                    )

urlpatterns = [
    path("", RecipeListView.as_view(), name="home"),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'), #int:pk is primary key limited to integers
    path('recipes/<str:author>/', RecipeAuthorListView.as_view(), name="recipes-author"),
    path('recipe/new/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/update/', RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('search/', RecipeSearchView.as_view(), name='recipe-search'),
    path('generate_recipe_pdf/<int:recipe_id>/', views.generate_recipe_pdf, name='generate-recipe-pdf'),
]

