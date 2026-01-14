from typing import List, Optional
from decimal import Decimal
from ...domain.product import Product
from  ..db.connection import get_connection

class ProductRepository:

    def save(self, product: Product) -> None:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO products (
                id,
                name,
                type,
                price
                ) VALUES (?, ?, ?, ?)
                """,
                (product.id, product.name, product.type, str(product.price))
            )
            connection.commit()

    def get_by_id(self, product_id: str) -> Optional[Product]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
            "SELECT id, name, type, price FROM products WHERE id = ?",
            (product_id,)
            )

            row = cursor.fetchone()

            if not row:
                return None

            return Product(id=row[0], name=row[1], type=row[2], price=Decimal(row[3]))

    def list_all(self) -> List[Product]:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, name, type, price FROM products",
            )

            rows = cursor.fetchall()

            return [
                Product(id=row[0], name=row[1], type=row[2], price=Decimal(row[3]))
                for row in rows
            ]