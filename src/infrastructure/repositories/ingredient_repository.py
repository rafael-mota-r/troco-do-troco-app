from decimal import Decimal
from typing import List, Optional
from ...domain.ingredient import Ingredient, MeasureUnit
from ..db.connection import get_connection


class IngredientRepository:

    def save(self, ingredient: Ingredient) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO ingredients (
                    id, name, unit, quantity, total_cost
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    ingredient.id,
                    ingredient.name,
                    ingredient.unit.value,
                    str(ingredient.quantity),
                    str(ingredient.total_cost),
                )
            )

    def get_by_id(self, ingredient_id: str) -> Optional[Ingredient]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, unit, quantity, total_cost FROM ingredients WHERE id = ?",
                (ingredient_id,)
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return Ingredient(
            id=row[0],
            name=row[1],
            unit=MeasureUnit(row[2]),
            quantity=Decimal(row[3]),
            total_cost=Decimal(row[4]),
        )

    def list_all(self) -> List[Ingredient]:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, unit, quantity, total_cost FROM ingredients"
            )
            rows = cursor.fetchall()

        return [
            Ingredient(
                id=row[0],
                name=row[1],
                unit=MeasureUnit(row[2]),
                quantity=Decimal(row[3]),
                total_cost=Decimal(row[4])
            )
            for row in rows
        ]
