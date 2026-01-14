from decimal import Decimal
from typing import List
from ...domain.product_recipe import ProductRecipe
from ..db.connection import get_connection

class ProductRecipeRepository:

    def add(self, product_recipe: ProductRecipe) -> None:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO product_recipes(
                product_id, recipe_id, ratio
                ) VALUES (?, ?, ?)
                """,
                (
                    product_recipe.product_id,
                    product_recipe.recipe_id,
                    str(product_recipe.ratio)
                )
            )
            connection.commit()

    def list_by_product_id(self, product_id: str) -> List[ProductRecipe]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT product_id, recipe_id, ratio
                FROM product_recipes
                WHERE product_id = ?
                """,
                (product_id,)
            )

            rows = cursor.fetchall()

            return [
                ProductRecipe(
                    product_id = row[0],
                    recipe_id= row[1],
                    ratio= Decimal(row[2])
                )
                for row in rows
            ]

    def remove(self, product_id: str, recipe_id: str) -> None:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                DELETE FROM product_recipes
                WHERE product_id = ? AND recipe_id = ?
                """,
                (product_id, recipe_id)
            )
            connection.commit()