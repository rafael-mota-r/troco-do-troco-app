from decimal import Decimal
from typing import List, Optional
from ...domain.recipe import Recipe, RecipeItem
from ...domain.ingredient import Ingredient, MeasureUnit
from ..db.connection import get_connection

class RecipeRepository:
    def save(self, recipe: Recipe) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "INSERT OR REPLACE INTO recipes(id) VALUES (?)",
                    (recipe.id,)
                )

                cursor.execute(
                    "DELETE FROM recipe_items WHERE recipe_id = ?",
                    (recipe.id,)
                )

                for items in recipe.items:
                    cursor.execute(
                        """
                        INSERT INTO recipe_items(
                            ingredient_id,
                            recipe_id,
                            quantity
                            ) VALUES (?, ?, ?)
                        """,
                        (
                            items.ingredient.id,
                            recipe.id,
                            str(items.quantity)
                        )
                    )

                conn.commit()

            except Exception:
                conn.rollback()
                raise

    def get_by_id(self, recipe_id: str) -> Optional[Recipe]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM recipes WHERE id = ?",
                (recipe_id,)
            )
            recipe_row = cursor.fetchone()

            if recipe_row is None:
                return None

            recipe = Recipe(id=recipe_id)

            cursor.execute(
                """
                SELECT i.id, i.name, i.unit, i.quantity, i.total_cost, ri.quantity
                FROM recipe_items ri
                JOIN ingredients i ON ri.ingredient_id = i.id
                WHERE ri.recipe_id = ?
                """,
                (recipe_id,)
            )
            
            rows = cursor.fetchall()

            for row in rows:
                ingredient = Ingredient(
                    id=row[0],
                    name=row[1],
                    unit=MeasureUnit(row[2]),
                    quantity=Decimal(row[3]),
                    total_cost = Decimal(row[4])
                )
                
                recipe.add_ingredient(
                    ingredient=ingredient,
                    quantity=Decimal(row[5])
                )
                
            return recipe
    
    def list_all(self) -> List[Recipe]:
        with get_connection() as conn:  
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM recipes"
            )
            recipe_ids = [row[0] for row in cursor.fetchall()]

            recipes = []
            for recipe_id in recipe_ids:
                recipe = self.get_by_id(recipe_id)
                if recipe:
                    recipes.append(recipe)

            return recipes