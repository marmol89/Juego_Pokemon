class pokemon:
    def __init__(self, nombre, tipos, movimientos, EVs, puntos_de_salud):
        self.nombre = nombre
        self.tipos = tipos
        self.movimientos = movimientos
        self.ataque = EVs['ataque']
        self.defensa = EVs['defensa']
        self.puntos_de_salud = puntos_de_salud
    
    def nombre(self):
        return self.nombre
    
    def tipos(self):
        return self.tipos
    
    def movimientos(self):
        return self.movimientos
    
    def ataque(self):
        return self.ataque
    
    def defensa(self):
        return self.defensa
    
    def puntos_de_salud(self):
        return self.puntos_de_salud