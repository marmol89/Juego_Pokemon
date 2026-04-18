class user:
    def __init__(self, id, username, password):
        self._id = id
        self._username = username
        self._password = password
    
    @property
    def id(self):
        return self._id
    
    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password