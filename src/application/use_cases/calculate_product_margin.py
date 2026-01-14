from decimal import Decimal

class CalculateProductMargin:
    def __init__(
            self,
            product_repository,
            recipe_repository,
            productrecipe_repository
    ):
        self.product_repository = product_repository
        self.recipe_repository = recipe_repository
        self.productrecipe_repository = productrecipe_repository

    def calculate(self, product_id: str) -> dict:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        relations = self.productrecipe_repository.list_by_product_id(product.id)

        total_cost = Decimal("0")

        for relation in relations:
            recipe = self.recipe_repository.get_by_id(relation.recipe_id)
            if not recipe:
                continue

            recipe_cost = recipe.calculate_total_cost()
            total_cost += recipe_cost * relation.ratio

        margin = product.price - total_cost

        return {
            "product_id": product.id,
            "price": product.price,
            "total_cost": total_cost,
            "margin": margin
        }