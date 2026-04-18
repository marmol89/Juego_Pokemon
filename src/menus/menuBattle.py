import os
import time
import json

class menuBattle:
    def __init__(self , room):
        self.room = room
        os.system('cls')
    
    def inicio(self, user, enemy):
        print("Inicio battalla")
        print(user.username + " vs " + enemy.username)
        time.sleep(2)

    def presentacionPokemons(self, user, enemy, userTeam, enemyTeam):
        os.system('cls')
        print(f"═══{'-'*len(user.username)}───Pokemon───{'-'*len(enemy.username)}═══")
        print(f" {user.username:^{len(user.username)+21}} vs {enemy.username:^{len(enemy.username)+21}} ")
        print(f" {'':^{len(user.username)+21}} {'':^{len(enemy.username)+21}} ")
        
        for userPokemon, enemyPokemon in zip(userTeam, enemyTeam):
            print(f" {userPokemon.pokemon().nombre:^{len(user.username)+21}} vs {enemyPokemon.pokemon().nombre:^{len(enemy.username)+21}} ")
        
        print(f"══{'-'*len(user.username)}───Pokemon───{'-'*len(enemy.username)}═══")
        time.sleep(2)

    def combate(self, user, enemy , userTeam, enemyTeam):
        os.system('cls')
        userPokemon = self.room.pokemonActivoUser()
        enemyPokemon = self.room.pokemonActivoEnemigo()
        activeUserTeam = next((t for t in userTeam if t.active), userTeam[0])
        activeEnemyTeam = next((t for t in enemyTeam if t.active), enemyTeam[0])
        userVida = max(0, activeUserTeam.vida)
        enemyVida = max(0, activeEnemyTeam.vida)
        
        print(f"{'='*30} Pokémon {'='*30}")
        print(f"{userPokemon.nombre:^30} {'vs':^10} {enemyPokemon.nombre:^30}")
        print(f"{'':^30} {'':^10} {'':^30}")
        print(f"HP: {userVida}/{userPokemon.puntos_de_salud} {'':^10} HP: {enemyVida}/{enemyPokemon.puntos_de_salud}")
        print(f"[{'#' * (int(userVida / userPokemon.puntos_de_salud * 10)):<10}] {'':^10} [{'#' * (int(enemyVida / enemyPokemon.puntos_de_salud * 10)):<10}]")
        print(f"{'='*30}{'='*10}{'='*30}")
        
        print("\n¿Qué movimiento quieres usar?")
        movimientos = userPokemon.movimientos
        if isinstance(movimientos, str):
            movimientos = json.loads(movimientos)
            
        for i, mov in enumerate(movimientos):
            print(f"{i+1} - {mov['nombre']} (Poder: {mov['poder']} | Tipo: {mov['tipo']})")
        
        while True:
            try:
                opcion = int(input("Option: "))
                if 1 <= opcion <= len(movimientos):
                    return movimientos[opcion - 1]
            except:
                pass
    

    def vida(self, user, enemy , userTeam, enemyTeam):
        os.system('cls')
        print("------------------------")
        time.sleep(5)
    
    def victoria(self, user, enemy , userTeam, enemyTeam):
        os.system('cls')
        print(f"¡{user.username} ha ganado la batalla!")
        time.sleep(2)

    def derrota(self, user, enemy , userTeam, enemyTeam):
        os.system('cls')
        print(f"{user.username} ha sido derrotado por {enemy.username}.")
        time.sleep(2)

    def cambiarPokemon(self, teamList):
        vivos = [t for t in teamList if t.vida > 0]
        if not vivos: return None
        
        while True:
            os.system('cls')
            print("¡Tu Pokémon ha sido debilitado! Elige a tu siguiente Pokémon:")
            for i, t in enumerate(vivos):
                pokemon = t.pokemon()
                print(f"{i+1} - {pokemon.nombre} (HP: {t.vida}/{pokemon.puntos_de_salud})")
                
            try:
                opcion = int(input("Option: "))
                if 1 <= opcion <= len(vivos):
                    return vivos[opcion - 1]
            except:
                pass