import json

class pokemon:
    def __init__(self, id , nombre, tipos, movimientos, EVs, puntos_de_salud):
        self._id = id
        self._nombre = nombre
        
        # Robust parsing for JSON fields
        if isinstance(tipos, str):
            try: tipos = json.loads(tipos)
            except: tipos = []
        if isinstance(movimientos, str):
            try: movimientos = json.loads(movimientos)
            except: movimientos = []
        if isinstance(EVs, str):
            try: EVs = json.loads(EVs)
            except: EVs = {"ataque": 50, "defensa": 50, "velocidad": 50}
            
        self._tipos = tipos
        self._movimientos = movimientos
        self._ataque = EVs.get('ataque', 50)
        self._defensa = EVs.get('defensa', 50)
        self._velocidad = EVs.get('velocidad', 50)
        self._puntos_de_salud = puntos_de_salud
    
    @property
    def id(self):
        return self._id
        
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def tipos(self):
        return self._tipos
    
    @property
    def movimientos(self):
        return self._movimientos
    
    @property
    def ataque(self):
        return self._ataque
    
    @property
    def defensa(self):
        return self._defensa
    
    @property
    def velocidad(self):
        return self._velocidad
    
    @property
    def puntos_de_salud(self):
        if self._puntos_de_salud <= 0:
            self._puntos_de_salud = 0
        return self._puntos_de_salud