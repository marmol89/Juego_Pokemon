class user:
    def __init__(self, id, username, password, puntos=0):
        self._id = id
        self._username = username
        self._password = password
        self._puntos = puntos
    
    @property
    def id(self):
        return self._id
    
    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password

    @property
    def puntos(self):
        return self._puntos