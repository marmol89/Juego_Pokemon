import pytest
from src.models.pokemon import pokemon
from src.utils.combat.damage import calculate_damage

def test_damage_basic():
    # Atk = 100, Def = 100, Power = 100 -> dmg = (100/100) * 100 * 0.5 = 50
    atk_poke = pokemon(1, "atk", [], [], {"ataque": 100}, 100)
    def_poke = pokemon(2, "def", [], [], {"defensa": 100}, 100)
    
    dmg = calculate_damage(atk_poke, def_poke, 100)
    assert dmg == 50

def test_damage_min():
    # Very low attack vs very high defense
    atk_poke = pokemon(1, "atk", [], [], {"ataque": 1}, 100)
    def_poke = pokemon(2, "def", [], [], {"defensa": 999}, 100)
    
    dmg = calculate_damage(atk_poke, def_poke, 10)
    assert dmg == 1 # Minimum damage is 1

def test_damage_zero_defense_protection():
    # Protection against division by zero
    atk_poke = pokemon(1, "atk", [], [], {"ataque": 100}, 100)
    def_poke = pokemon(2, "def", [], [], {"defensa": 0}, 100)
    
    dmg = calculate_damage(atk_poke, def_poke, 100)
    assert dmg == 5000 # (100 * 100 * 0.5)
