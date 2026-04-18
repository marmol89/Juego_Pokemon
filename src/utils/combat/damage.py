def calculate_damage(attacker, defender, move_power):
    """
    Calcula el daño infligido basándose en las estadísticas del atacante y defensor.
    Fórmula: max(1, int((Atk / Def) * Poder * 0.5))
    """
    if defender.defensa <= 0:
        # Evitar división por cero
        return max(1, int(attacker.ataque * move_power * 0.5))
        
    dmg = int((attacker.ataque / defender.defensa) * move_power * 0.5)
    return max(1, dmg)
