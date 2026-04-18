from src.database.users import users
from src.Consultas.roomCS import roomCS
class room:

    #Estados 1->Abirto, 2->cargando, 3->Cerrado, 4->Finalizado,

    def __init__(self, id , user_id, enemigo_id, nombre, estado):
        self._id = id
        self._user_id = user_id
        self._enemigo_id = enemigo_id
        self._nombre = nombre
        self._estado = estado
    
    @property
    def id(self):
        return self._id
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def enemigo_id(self):
        return self._enemigo_id
    
    @enemigo_id.setter
    def enemigo_id(self, value):
        self._enemigo_id = value
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, value):
        self._estado = value
    
    def getUser(self):
        userdb = users()
        return userdb.getUser(self._user_id)
    
    def getEnemigo(self):
        userdb = users()
        return userdb.getUser(self._enemigo_id)
    
    def getBattle(self):
        roomsdb = roomCS()
        return roomsdb.getBattle(self._id)
    
    def getUserTeam(self):
        roomsdb = roomCS()
        return roomsdb.getUserTeam(self._id, self._user_id)
    
    def getEnemigoTeam(self):
        roomsdb = roomCS()
        return roomsdb.getUserTeam(self._id, self._enemigo_id)
    
    def isVidaTeamUser(self):
        roomsdb = roomCS()
        return roomsdb.isTodosConVida(self._id, self._user_id)
    
    def isVidaTeamEnemigo(self):
        roomsdb = roomCS()
        return roomsdb.isTodosConVida(self._id, self._enemigo_id)
    
    def pokemonActivoUser(self):
        roomsdb = roomCS()
        return roomsdb.pokemonActivo(self._id, self._user_id)
    
    def pokemonActivoEnemigo(self):
        roomsdb = roomCS()
        return roomsdb.pokemonActivo(self._id, self._enemigo_id)

    def getMyTeam(self, current_user_id):
        return self.getUserTeam() if current_user_id == self._user_id else self.getEnemigoTeam()
        
    def getTheirTeam(self, current_user_id):
        return self.getEnemigoTeam() if current_user_id == self._user_id else self.getUserTeam()
        
    def getTheirUser(self, current_user_id):
        return self.getEnemigo() if current_user_id == self._user_id else self.getUser()

    def getMyActivePokemon(self, current_user_id):
        return self.pokemonActivoUser() if current_user_id == self._user_id else self.pokemonActivoEnemigo()
        
    def getTheirActivePokemon(self, current_user_id):
        return self.pokemonActivoEnemigo() if current_user_id == self._user_id else self.pokemonActivoUser()
