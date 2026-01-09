import uuid


class Product:
    def __init__(
            self,
            name: str,
            type: str = "Item",
            id: str = None
    ):
        #Validações - Produto
        if not name or name.strip() == '':
            raise ValueError('Product name cannot be empty')
        if not type or type.strip() == '':
            raise ValueError('Product type cannot be empty')
        if id is None:
            id = str(uuid.uuid4())

        self.id = id
        self.name = name
        self.type = type

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            id = data['id'],
            name = data['name'],
            type = data['type']
        )