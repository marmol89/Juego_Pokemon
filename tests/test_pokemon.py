import pytest
import json
from src.models.pokemon import pokemon

def test_pokemon_initialization():
    # Test with valid JSON strings
    pkmn = pokemon(
        id=1,
        nombre="Bulbasaur",
        tipos='["grass", "poison"]',
        movimientos='[{"nombre": "Placaje", "poder": 40}]',
        EVs='{"ataque": 49, "defensa": 49, "velocidad": 45}',
        puntos_de_salud=45
    )
    
    assert pkmn.nombre == "Bulbasaur"
    assert "grass" in pkmn.tipos
    assert pkmn.ataque == 49
    assert pkmn.defensa == 49
    assert pkmn.puntos_de_salud == 45

def test_pokemon_default_evs():
    # Test with invalid/missing EVs
    pkmn = pokemon(
        id=1,
        nombre="test",
        tipos=[],
        movimientos=[],
        EVs="invalid_json",
        puntos_de_salud=10
    )
    
    # Defaults in code: 50
    assert pkmn.ataque == 50
    assert pkmn.defensa == 50
    assert pkmn.velocidad == 50

def test_pokemon_hp_clamping():
    # Test that HP doesn't go below 0
    pkmn = pokemon(1, "test", [], [], {}, -10)
    assert pkmn.puntos_de_salud == 0
