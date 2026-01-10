from decimal import Decimal
from typing import List
import uuid
from .ingredient import Ingredient

class RecipeItem:
    def __init__(
        self,
        ingredient: Ingredient,
        quantity: Decimal
    ):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("ingredient must be an Ingredient instance")
        if quantity <= 0:
            raise ValueError(f'Quantity {quantity} is not valid')

        self.ingredient = ingredient
        self.quantity = quantity

    def calculate_cost(self) -> Decimal:
        return self.ingredient.calculate_cost(self.quantity)

class Recipe:
    def __init__(self, id: str = None):
        self.id = id or str(uuid.uuid4())
        self._items: List[RecipeItem] = []

    @property
    def items(self):
        return tuple(self._items)

    def add_ingredient(self, ingredient: Ingredient, quantity: Decimal):
        if not isinstance(ingredient, Ingredient):
            raise TypeError("ingredient must be an Ingredient instance")
        if quantity <= 0:
            raise ValueError(f"Quantity {quantity} is not valid")

        for item in self._items:
            if item.ingredient.id == ingredient.id:
                item.quantity += quantity
                return

        self._items.append(RecipeItem(ingredient, quantity))

    def remove_ingredient(self, ingredient_id: str):
        self._items = [
            item for item in self._items
            if item.ingredient.id != ingredient_id
        ]

    def calculate_total_cost(self) -> Decimal:
        total_cost = Decimal("0")
        for item in self._items:
            total_cost += item.calculate_cost()
        return total_cost

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "items": [
                {
                    "ingredient": item.ingredient.to_dict(),
                    "quantity": str(item.quantity)
                }
                for item in self._items
            ]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Recipe":
        recipe = cls(id=data["id"])

        for item_data in data.get("items", []):
            ingredient = Ingredient.from_dict(item_data["ingredient"])
            quantity = Decimal(item_data["quantity"])
            recipe.add_ingredient(ingredient, quantity)

        return recipe
