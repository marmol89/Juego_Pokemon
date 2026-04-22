import time
import json
from src.utils.clear_screen import clear_screen
from src.utils.realtime import BattleRealtime

class menuBattle:
    def __init__(self , room):
        self.room = room
        clear_screen()
    
    def inicio(self, user, enemy):
        print(f"{'='*70}")
        print(f"{'¡LA BATALLA COMIENZA!':^70}")
        print(f"{'='*70}")
        print(f"\n{user.username:^30} {'VS':^10} {enemy.username:^30}\n")
        print(f"{'='*70}")
        time.sleep(2)

    def presentacionPokemons(self, user, enemy, userTeam, enemyTeam):
        clear_screen()
        print(f"{'='*70}")
        print(f"{'PRESENTACIÓN DE EQUIPOS':^70}")
        print(f"{'='*70}\n")

        # Header row con nombres
        username_width = 28
        print(f"  {user.username:<{username_width}}               {enemy.username:>{username_width}}")

        # Encabezados de columnas
        sep = "  " + "-"*username_width + "         " + "-"*username_width
        print(sep)

        for userTeamObj, enemyTeamObj in zip(userTeam, enemyTeam):
            u_name = userTeamObj.pokemon().nombre.upper()
            e_name = enemyTeamObj.pokemon().nombre.upper()
            print(f"  {u_name:<{username_width}}    vs    {e_name:>{username_width}}")

        print()
        print(f"{'='*70}")
        time.sleep(3)

    def combate(self, user, enemy, userTeam, enemyTeam, items_used=0):
        clear_screen()
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
        print("   [6] RENDIRSE")
        
        print()
        from src.utils.visuals import get_key_timeout
        from src.Consultas.movementCS import movementCS
        movCS = movementCS()
        
        # Setup Realtime handlers
        battle_realtime = BattleRealtime()
        opponent_surrendered = False
        
        def on_opponent_action(event):
            """Handle opponent surrender signal."""
            nonlocal opponent_surrendered
            payload = event.get('payload', {})
            try:
                efecto = payload.get('efecto', '{}')
                opp_move = json.loads(efecto) if isinstance(efecto, str) else efecto
                if opp_move.get("tipo_accion") == "surrender":
                    opponent_surrendered = True
            except:
                pass
        
        # Subscribe to realtime (with fallback to polling)
        battle_id = getattr(self.room, 'id', None)
        if battle_id:
            battle_realtime.subscribe(battle_id, {
                'on_player_action': lambda e: None,
                'on_opponent_action': on_opponent_action,
                'on_battle_end': lambda e: None
            })
        
        while True:
            # Check for opponent surrender via realtime or polling
            if opponent_surrendered or battle_realtime.is_connected():
                if opponent_surrendered:
                    battle_realtime.unsubscribe()
                    return {"tipo_accion": "opponent_surrender"}
            else:
                # Fallback polling for opponent surrender when realtime not connected
                opp_poke = self.room.getTheirActivePokemon(user.id)
                if opp_poke:
                    opp_move_row = movCS.getMovement(self.room.id, opp_poke.id)
                    if opp_move_row:
                        try:
                            opp_move = json.loads(opp_move_row['efecto'])
                            if opp_move.get("tipo_accion") == "surrender":
                                battle_realtime.unsubscribe()
                                return {"tipo_accion": "opponent_surrender"}
                        except:
                            pass

            opcion_str = get_key_timeout(timeout=0.5)
            if opcion_str is None:
                continue

            try:
                opcion = int(opcion_str)
                if 1 <= opcion <= len(movimientos):
                    battle_realtime.unsubscribe()
                    return movimientos[opcion - 1]
                if opcion == 5:
                    if items_used >= 5:
                        print("\n  [!] Ya has usado el máximo de 5 objetos en esta batalla.")
                        time.sleep(1.5)
                        battle_realtime.unsubscribe()
                        return self.combate(user, enemy, userTeam, enemyTeam, items_used)
                    battle_realtime.unsubscribe()
                    return {"tipo_accion": "item"}
                if opcion == 6:
                    print("\n  ¿Estás REALMENTE SEGURO de que quieres rendirte? [S/N]")
                    confirm = None
                    while confirm not in ['s', 'n']:
                        confirm = get_key_timeout(timeout=0.5)
                    if confirm == 's':
                        battle_realtime.unsubscribe()
                        return {"tipo_accion": "surrender", "nombre": "Rendición"}
                    else:
                        print("  [!] Sabia decisión. ¡Sigue luchando!")
                        time.sleep(1.5)
                        battle_realtime.unsubscribe()
                        return self.combate(user, enemy, userTeam, enemyTeam, items_used)
            except:
                pass
    
    def vida(self, user, enemy, userTeam, enemyTeam):
        clear_screen()
        print("------------------------")
        time.sleep(5)
    
    def victoria(self, user, enemy, userTeam, enemyTeam):
        clear_screen()
        print(f"¡{user.username} ha ganado la batalla!")
        time.sleep(2)

    def derrota(self, user, enemy, userTeam, enemyTeam):
        clear_screen()
        print(f"{user.username} ha sido derrotado por {enemy.username}.")
        time.sleep(2)

    def cambiarPokemon(self, teamList):
        from src.utils.visuals import get_key_timeout
        vivos = [t for t in teamList if t.vida > 0]
        if not vivos: return None

        while True:
            clear_screen()
            print(f"{'='*70}")
            print(f"{'¡TU POKÉMON HA SIDO DEBILITADO!':^70}")
            print(f"{'='*70}\n")
            print("  Elige a tu siguiente compañero:\n")
            for i, t in enumerate(vivos):
                pokemon = t.pokemon()
                print(f"   [{i+1}] {pokemon.nombre:<15} (HP: {t.vida}/{pokemon.puntos_de_salud})")

            print(f"\n{'='*70}")

            # Leer opción de múltiples dígitos
            choice = ""
            print("\n  > ", end="", flush=True)
            while True:
                ch = get_key_timeout(timeout=0.5)
                if ch is None:
                    # Check for surrender
                    battle = self.room.getBattle()
                    if battle and battle.winner_id:
                        return None
                    continue
                if ch == '\r' or ch == '\n':
                    print()
                    break
                if ch.isdigit():
                    choice += ch
                    print(ch, end="", flush=True)

            try:
                choice_int = int(choice)
                if 1 <= choice_int <= len(vivos):
                    return vivos[choice_int - 1]
            except:
                pass

    def mochila(self, user_id, items_used=0):
        from src.database.items import items
        from src.utils.visuals import get_key_timeout
        inventory = items().getUserItems(user_id)

        while True:
            clear_screen()
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

            # Leer opción de múltiples dígitos
            choice = ""
            print("\n  > ", end="", flush=True)
            while True:
                ch = get_key_timeout(timeout=0.5)
                if ch is None:
                    # Check for surrender
                    battle = self.room.getBattle()
                    if battle and battle.get('winner_id'):
                        return None
                    continue
                if ch == '\r' or ch == '\n':
                    print()
                    break
                if ch == '0' and len(choice) == 0:
                    choice = '0'
                    print("0")
                    break
                if ch.isdigit():
                    choice += ch
                    print(ch, end="", flush=True)

            try:
                choice_int = int(choice)
                if choice_int == 0:
                    return None
                if 1 <= choice_int <= len(inventory):
                    return inventory[choice_int - 1]['item']
            except:
                pass