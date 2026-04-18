import json

class item:
    def __init__(self, id, nombre, descripcion, precio, efecto):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        # efecto suele ser un dict: {"cura": 50}
        if isinstance(efecto, str):
            self.efecto = json.loads(efecto)
        else:
            self.efecto = efecto
