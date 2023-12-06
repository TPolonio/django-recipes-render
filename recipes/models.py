from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

DIFICULTY_CHOICES = (
    ('easy','Easy'),
    ('medium', 'Medium'),
    ('hard','Hard'),
)

class Recipe(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()
    published_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.CharField(max_length=200)
    duration = models.IntegerField()
    difficulty = models.CharField(max_length=6, choices=DIFICULTY_CHOICES, default='easy')   

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipe-detail', kwargs={'pk': self.pk})
    
    #redirect redirects you to specific route
    #reverse returns the url to the route as string


""" class RecipeIngredient(models.Model):
     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)     
     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)     
     quantity = models.DecimalField(max_digits=10, decimal_places=2)  # Para armazenar a quantidade    
     units = models.CharField(max_length=20)  # Para armazenar as unidades de medida   

     class Meta:         
        unique_together = ('recipe', 'ingredient')  # Combinação única de receita e ingrediente """


"""     unique_together = ('recipe', 'ingredient'): Esta linha dentro da classe Meta do modelo especifica que a combinação da recipe (receita) e ingredient (ingrediente) deve ser única. Significa que uma receita não pode ter o mesmo ingrediente registrado mais de uma vez.

Por exemplo, suponha que tenhamos a receita "Bolo de Chocolate" (RecipeID 1) e o ingrediente "Farinha" (IngredientID 10). Com a restrição unique_together, podemos ter apenas uma entrada para "Bolo de Chocolate" e "Farinha" na tabela RecipeIngredient. Se tentarmos adicionar outra entrada para "Bolo de Chocolate" e "Farinha", o Django irá impedir e gerar um erro, garantindo a unicidade da combinação. """