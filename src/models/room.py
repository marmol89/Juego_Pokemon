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
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def estado(self):
        return self._estado
    
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
