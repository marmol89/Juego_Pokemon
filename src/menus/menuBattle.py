import os
import time
import json

class menuBattle:
    def __init__(self , room):
        self.room = room
        os.system('cls')
    
    def inicio(self, user, enemy):
        print(f"{'='*70}")
        print(f"{'¡LA BATALLA COMIENZA!':^70}")
        print(f"{'='*70}")
        print(f"\n{user.username:^30} {'VS':^10} {enemy.username:^30}\n")
        print(f"{'='*70}")
        time.sleep(2)

    def presentacionPokemons(self, user, enemy, userTeam, enemyTeam):
        os.system('cls')
        print(f"{'='*70}")
        print(f"{'PRESENTACIÓN DE EQUIPOS':^70}")
        print(f"{'='*70}\n")
        print(f" {user.username:^30} {'':^10} {enemy.username:^30}")
        print(f" {'-'*30:^30} {'':^10} {'-'*30:^30} ")
        
        for userTeamObj, enemyTeamObj in zip(userTeam, enemyTeam):
            u_name = userTeamObj.pokemon().nombre.upper()
            e_name = enemyTeamObj.pokemon().nombre.upper()
            print(f" {u_name:^30} {'vs':^10} {e_name:^30} ")
        
        print(f"\n{'='*70}")
        time.sleep(3)

    def combate(self, user, enemy , userTeam, enemyTeam, items_used=0):
        os.system('cls')
        userPokemon = self.room.getMyActivePokemon(user.id)
        enemyPokemon = self.room.getTheirActivePokemon(user.id)
            
        activeUserTeam = next((t for t in userTeam if t.active), userTeam[0])
        activeEnemyTeam = next((t for t in enemyTeam if t.active), enemyTeam[0])
        userVida = max(0, activeUserTeam.vida)
        enemyVida = max(0, activeEnemyTeam.vida)
        
        print(f"{'='*70}")
        print(f"{userPokemon.nombre:^30} {'VS':^10} {enemyPokemon.nombre:^30}")
        
        hp_user_str = f"HP: {userVida}/{userPokemon.puntos_de_salud}"
        hp_enemy_str = f"HP: {enemyVida}/{enemyPokemon.puntos_de_salud}"
        print(f"{hp_user_str:^30} {'':^10} {hp_enemy_str:^30}")
        
        bar_user = '[' + '#' * (int(userVida / userPokemon.puntos_de_salud * 10)) + ' ' * (10 - int(userVida / userPokemon.puntos_de_salud * 10)) + ']'
        bar_enemy = '[' + '#' * (int(enemyVida / enemyPokemon.puntos_de_salud * 10)) + ' ' * (10 - int(enemyVida / enemyPokemon.puntos_de_salud * 10)) + ']'
        print(f"{bar_user:^30} {'':^10} {bar_enemy:^30}")
        print(f"{'='*70}")
        
        print("\n  ¿Qué movimiento quieres usar?\n")
        movimientos = userPokemon.movimientos
            
        for i, mov in enumerate(movimientos):
            print(f"   [{i+1}] {mov['nombre'][:15]:<15} (Poder: {mov['poder']:>3} | Tipo: {mov['tipo']})")
        
        status_mochila = f"({items_used}/5)"
        if items_used >= 5:
            print(f"   [5] MOCHILA {status_mochila} [LÍMITE ALCANZADO]")
        else:
            print(f"   [5] MOCHILA {status_mochila}")
        
        print()
        while True:
            try:
                opcion = int(input("  Elige una opción: "))
                if 1 <= opcion <= len(movimientos):
                    return movimientos[opcion - 1]
                if opcion == 5:
                    if items_used >= 5:
                        print("  [!] Ya has usado el máximo de 5 objetos en esta batalla.")
                        time.sleep(1.5)
                        return self.combate(user, enemy, userTeam, enemyTeam, items_used)
                    return {"tipo_accion": "item"}
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
            print(f"{'='*70}")
            print(f"{'¡TU POKÉMON HA SIDO DEBILITADO!':^70}")
            print(f"{'='*70}\n")
            print("  Elige a tu siguiente compañero:\n")
            for i, t in enumerate(vivos):
                pokemon = t.pokemon()
                print(f"   [{i+1}] {pokemon.nombre:<15} (HP: {t.vida}/{pokemon.puntos_de_salud})")
                
            print(f"\n{'='*70}")
            try:
                opcion = int(input("   Elige una opción: "))
                if 1 <= opcion <= len(vivos):
                    return vivos[opcion - 1]
            except:
                pass

    def mochila(self, user_id, items_used=0):
        from src.database.items import items
        inventory = items().getUserItems(user_id)
        
        while True:
            os.system('cls')
            print(f"{'='*70}")
            print(f"{'MOCHILA ' + f'({items_used}/5)':^70}")
            print(f"{'='*70}\n")
            
            if not inventory:
                print("    (No tienes objetos disponibles)")
                time.sleep(1.5)
                return None
            
            for i, inv in enumerate(inventory):
                it = inv['item']
                print(f"   [{i+1}] {it.nombre:<15} x{inv['cantidad']} - {it.descripcion}")
            
            print(f"\n   [0] VOLVER")
            print(f"\n{'='*70}")
            
            try:
                choice = int(input("   Elige un objeto: "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(inventory):
                    return inventory[choice - 1]['item']
            except:
                pass