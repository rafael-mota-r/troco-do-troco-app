from decimal import Decimal

class ProductRecipe:
    def __init__(self, recipe_id:str, product_id:str , ratio : Decimal = Decimal("1")):
        if ratio <= 0:
            raise ValueError("ratio must be greater than 0")

        self.recipe_id = recipe_id
        self.product_id = product_id
        self.ratio = ratio