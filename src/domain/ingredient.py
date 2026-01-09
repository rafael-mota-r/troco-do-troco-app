from decimal import Decimal
from enum import Enum
import uuid

#Unidades pra teste, o ideal é o usuário inserir de maneira customizada.
class MeasureUnit(Enum):
    KG = 'kg'
    G = 'g'
    L = 'l'
    ML = 'ml'
    UNIT = 'unit'

class Ingredient:
    def __init__(
            self,
            name:str,
            unit:MeasureUnit,
            quantity:Decimal,
            total_cost:Decimal,
            id:str=None
    ):
        #Validações - Ingrediente
        if not name or name.strip() == '':
            raise ValueError('Ingredient name cannot be empty')
        if unit is None:
            raise ValueError(f'Unit {unit} is not valid')
        if quantity < 0:
            raise ValueError(f'Quantity {quantity} is not valid')
        if total_cost < 0:
            raise ValueError(f'Cost per unit {total_cost} is not valid')
        if id is None:
            id = str(uuid.uuid4())

        self.id = id
        self.name = name
        self.unit = unit
        self.quantity = quantity
        self.total_cost = total_cost
        self.cost_per_unit = total_cost / quantity

    def calculate_cost(self, quantity_used):
        #Calcula o custo por cada unidade utilizada na receita.
        return self.cost_per_unit*quantity_used

    def to_dict(self) -> dict:
    # Converte pra um dict para salvar no DB
        return {
            "id" : self.id,
            "name" : self.name,
            "unit" : self.unit.value,
            "quantity" : str(self.quantity),
            "total_cost" : str(self.total_cost)
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Ingredient':
        #Carrega objetos a partir de um dict
        return cls(
            id = data['id'],
            name = data['name'],
            unit = MeasureUnit(data['unit']),
            quantity = Decimal(data['quantity']),
            total_cost = Decimal(data['total_cost'])
        )
