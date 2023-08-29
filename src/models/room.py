from src.database.users import users

class room:

    #Estados 1->Abirto, 2->cargando, 3->Cerrado, 4->Finalizado,

    def __init__(self, id , user_id, enemigo_id, nombre, estado):
        self.id = id
        self.user_id = user_id
        self.enemigo_id = enemigo_id
        self.nombre = nombre
        self.estado = estado
    
    def id(self):
        return self.id
    
    def user_id(self):
        return self.user_id
    
    def enemigo_id(self):
        return self.enemigo_id
    
    def nombre(self):
        return self.nombre
    
    def estado(self):
        return self.estado
    
    def getUser(self):
        userdb = users()
        return userdb.getUser(self.user_id)
    
    def getEnemigo(self):
        userdb = users()
        return userdb.getUser(self.enemigo_id)
