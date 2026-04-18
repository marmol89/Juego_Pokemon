from src.database.db import db
from src.models.battle import battle
from src.models.team import team
from src.models.pokemon import pokemon

class roomCS:
    def __init__(self):
        self.dbp = db().get_connection()
    
    def getBattle(self, room_id):
        if not self.dbp: return None
        data = self.dbp.table("battles").select("*").eq("room_id", room_id).execute()
        if len(data.data) == 0: return None
        row = data.data[0]
        return battle(row['id'], row['room_id'], row['winner_id'], row['loser_id'], row['user_team_ids'], row['enemy_team_ids'])
    
    def getUserTeam(self, room_id, user_id):
        if not self.dbp: return []
        data = self.dbp.table("teams").select("*").eq("room_id", room_id).eq("user_id", user_id).execute()
        teams = []
        for row in data.data:
            teams.append(team(row['id'], row['room_id'], row['user_id'], row['pokemon_id'], row['active'], row['vida'], row['efecto']))
        return teams
    
    def isTodosConVida(self, room_id, user_id):
        if not self.dbp: return False
        data = self.dbp.table("teams").select("*").eq("room_id", room_id).eq("user_id", user_id).gt("vida", 0).execute()
        return len(data.data) > 0 # Al menos un pokemon con vida

    def pokemonActivo(self, room_id, user_id):
        if not self.dbp: return False
        data = self.dbp.table("teams").select("*").eq("room_id", room_id).eq("user_id", user_id).eq("active", True).execute()
        if not data.data: return False
        pokemon_id = data.data[0]['pokemon_id']
        pokemon_data = self.dbp.table("pokemons").select("*").eq("id", pokemon_id).execute()
        if not pokemon_data.data: return False
        row = pokemon_data.data[0]
        return pokemon(int(row['id']), row['nombre'], row['tipos'], row['movimientos'], row['EVs'], int(row['puntos_de_salud']))