import pytest
from src.utils.combat.damage import calculate_damage, obtener_multiplicador

def test_damage_basic():
    # Atk = 100, Def = 100, Power = 100 -> dmg = (100/100) * 100 * 0.5 = 50
    dmg = calculate_damage(base_power=100, attack=100, defense=100)
    assert dmg == 50

def test_damage_min():
    # Very low attack vs very high defense
    dmg = calculate_damage(base_power=10, attack=1, defense=999)
    assert dmg == 1 # Minimum damage is 1

def test_damage_zero_defense_protection():
    # Protection against division by zero
    dmg = calculate_damage(base_power=100, attack=100, defense=0)
    assert dmg == 5000 # (100 * 100 * 0.5)

def test_type_effectiveness_fire_vs_grass():
    # Fire vs Grass = 2.0x
    dmg = calculate_damage(base_power=100, attack=100, defense=100, type_multiplier=2.0)
    assert dmg == 100

def test_type_effectiveness_fire_vs_water():
    # Fire vs Water = 0.5x
    dmg = calculate_damage(base_power=100, attack=100, defense=100, type_multiplier=0.5)
    assert dmg == 25

def test_stab_bonus():
    # STAB = 1.5x when attacker type matches move type
    dmg = calculate_damage(base_power=100, attack=100, defense=100, stab_bonus=1.5)
    assert dmg == 75

def test_type_and_stab_combined():
    # Fire vs Grass with STAB
    dmg = calculate_damage(base_power=100, attack=100, defense=100, type_multiplier=2.0, stab_bonus=1.5)
    assert dmg == 150
