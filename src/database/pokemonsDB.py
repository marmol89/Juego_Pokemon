from src.database.db import db
from src.models.pokemon import pokemon
from src.cache.pokemon import PokemonCache

pokemon_cache = PokemonCache()


class pokemonDB:

    def __init__(self):
        self.dbp = db().get_connection()
    
    def getPokemons(self):
        if not self.dbp: return []
        data = self.dbp.table("pokemons").select("*").execute()
        datas = []
        for row in data.data:
            pokemon_obj = pokemon(int(row['id']), row['nombre'], row['tipos'], row['movimientos'], row['EVs'], int(row['puntos_de_salud']))
            datas.append(pokemon_obj)
        return datas

    def emptyTable(self):
        if not self.dbp: return
        self.dbp.table("pokemons").delete().neq("id", -1).execute()

    def insertPokemons(self, data_list):
        if not self.dbp: return
        self.dbp.table("pokemons").insert(data_list).execute()

    def getPokemon(self, id: int):
        # Cache first
        cached = pokemon_cache.get(id)
        if cached is not None:
            return cached
        # DB on miss
        if not self.dbp: return None
        data = self.dbp.table("pokemons").select("*").eq("id", id).execute()
        if len(data.data) == 0:
            return None
        row = data.data[0]
        pokemon_obj = pokemon(
            int(row['id']), row['nombre'], row['tipos'],
            row['movimientos'], row['EVs'], int(row['puntos_de_salud'])
        )
        pokemon_cache.set(id, pokemon_obj)
        return pokemon_obj

    def setPokemon(self, pokemon_obj: pokemon):
        if not self.dbp: return False
        data_list = [{
            'id': pokemon_obj.id,
            'nombre': pokemon_obj.nombre,
            'tipos': pokemon_obj.tipos,
            'movimientos': pokemon_obj.movimientos,
            'EVs': pokemon_obj.EVs,
            'puntos_de_salud': pokemon_obj.puntos_de_salud
        }]
        res = self.dbp.table("pokemons").update(data_list).eq("id", pokemon_obj.id).execute()
        # Invalidate cache after update
        pokemon_cache.invalidate(pokemon_obj.id)
        return len(res.data) > 0