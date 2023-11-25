import os
import time

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
        time.sleep(5)

    def combate(self, user, enemy , userTeam, enemyTeam):
        os.system('cls')
        print(f"{'='*30} Pokémon {'='*30}")
        print(f"{self.room.pokemonActivoUser().nombre:^30} {'vs':^10} {self.room.pokemonActivoEnemigo().nombre.nombre:^30}")
        print(f"{'':^30} {'':^10} {'':^30}")
        print(f"{userPokemon.nombre} - Nivel {userPokemon.nivel} {'':^10} {enemyPokemon.nombre} - Nivel 22")
        print(f"HP: {userPokemon.hp}/{userPokemon.max_hp} {'':^10} HP: {enemyPokemon.hp}/{enemyPokemon.max_hp}")
        print(f"[{'#' * (int(userPokemon.hp / userPokemon.max_hp * 10)):<10}] {'':^10} [{'#' * (int(enemyPokemon.hp / enemyPokemon.max_hp * 10)):<10}]")
        print(f"{'='*30}{'='*10}{'='*30}")
        time.sleep(2)
    

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