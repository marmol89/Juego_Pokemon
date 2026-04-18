class pokemon:
    def __init__(self, id , nombre, tipos, movimientos, EVs, puntos_de_salud):
        self._id = id
        self._nombre = nombre
        self._tipos = tipos
        self._movimientos = movimientos
        self._ataque = EVs['ataque']
        self._defensa = EVs['defensa']
        self._velocidad = EVs['velocidad']
        self._puntos_de_salud = puntos_de_salud
    
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