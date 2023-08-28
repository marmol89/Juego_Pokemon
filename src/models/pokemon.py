class pokemon:
    def __init__(self, id , nombre, tipos, movimientos, EVs, puntos_de_salud):
        self.id = id
        self.nombre = nombre
        self.tipos = tipos
        self.movimientos = movimientos
        self.ataque = EVs['ataque']
        self.defensa = EVs['defensa']
        self.velocidad = EVs['velocidad']
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
    
    def velocidad(self):
        return self.velocidad
    
    def puntos_de_salud(self):
        return self.puntos_de_salud