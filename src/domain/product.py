import uuid
from decimal import Decimal
from typing import List
from .product_recipe import ProductRecipe

class Product:
    def __init__(
            self,
            name: str,
            price: Decimal,
            type: str = "Item",
            id: str = None
    ):
        #Validações - Produto
        if not name or name.strip() == '':
            raise ValueError('Product name cannot be empty')
        if not type or type.strip() == '':
            raise ValueError('Product type cannot be empty')
        if price < 0:
            raise ValueError('Product price cannot be negative')
        if id is None:
            id = str(uuid.uuid4())

        self.id = id
        self.name = name
        self.type = type
        self.price = price
        self._recipes: List[ProductRecipe] = []

    @property
    def recipes(self):
        return tuple(self._recipes)

    def add_recipe(self, recipe: "Recipe", ratio: Decimal = Decimal("1")):
        self._recipes.append(ProductRecipe(recipe, ratio))

    def calculate_cost(self) -> Decimal:
        total = Decimal("0")
        for pr in self._recipes:
            total += pr.recipe.calculate_total_cost() * pr.ratio
        return total

    def calculate_margin(self) -> Decimal:
        return self.price - self.calculate_cost()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            "sale_price": str(self.price),
            "recipes": [
                {
                    "recipe": pr.recipe.to_dict(),
                    "factor": str(pr.ratio)
                }
                for pr in self._recipes
            ]
        }

    @classmethod
    def from_dict(cls, data):
        from .recipe import Recipe

        product = cls(
            id = data['id'],
            name = data['name'],
            type = data['type'],
            price = Decimal(data['sale_price'])
        )

        for r in data.get("recipes", []):
            recipe = Recipe.from_dict(r["recipe"])
            factor = Decimal(r["factor"])
            product.add_recipe(recipe, factor)

        return product