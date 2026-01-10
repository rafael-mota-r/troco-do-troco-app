from decimal import Decimal
from .recipe import Recipe

class ProductRecipe:
    def __init__(self, recipe : Recipe, ratio : Decimal = Decimal("1")):
        if not isinstance(recipe, Recipe):
            raise TypeError("recipe must be an instance of Recipe")
        if ratio <= 0:
            raise ValueError("ratio must be greater than 0")

        self.recipe : Recipe = recipe
        self.ratio : Decimal = ratio