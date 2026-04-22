-- Migration: 000_init_schema
-- Run this FIRST to create all base tables
-- This migration is idempotent: uses CREATE TABLE IF NOT EXISTS

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(600) NOT NULL,
    puntos INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS pokemons (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipos JSONB NOT NULL,
    movimientos JSONB NOT NULL,
    "EVs" JSONB NOT NULL,
    puntos_de_salud INT NOT NULL
);

CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    enemigo_id INT REFERENCES users(id) ON DELETE CASCADE,
    nombre VARCHAR(255) NOT NULL,
    estado INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS teams (
    id SERIAL PRIMARY KEY,
    room_id INT REFERENCES rooms(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    pokemon_id INT REFERENCES pokemons(id) ON DELETE CASCADE,
    active BOOLEAN DEFAULT false,
    vida INT,
    efecto VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS battles (
    id SERIAL PRIMARY KEY,
    room_id INT UNIQUE REFERENCES rooms(id) ON DELETE CASCADE,
    winner_id INT REFERENCES users(id) ON DELETE CASCADE,
    loser_id INT REFERENCES users(id) ON DELETE CASCADE,
    user_team_ids JSONB,
    enemy_team_ids JSONB
);

CREATE TABLE IF NOT EXISTS movements (
    id SERIAL PRIMARY KEY,
    room_id INT REFERENCES rooms(id) ON DELETE CASCADE,
    pokemon_id INT REFERENCES pokemons(id) ON DELETE CASCADE,
    nombre VARCHAR(255) NOT NULL,
    efecto VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio INTEGER DEFAULT 100,
    efecto JSONB
);

CREATE TABLE IF NOT EXISTS user_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    cantidad INTEGER DEFAULT 1
);

-- Disable Row Level Security for free read/write from Python
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE pokemons DISABLE ROW LEVEL SECURITY;
ALTER TABLE rooms DISABLE ROW LEVEL SECURITY;
ALTER TABLE teams DISABLE ROW LEVEL SECURITY;
ALTER TABLE battles DISABLE ROW LEVEL SECURITY;
ALTER TABLE movements DISABLE ROW LEVEL SECURITY;
ALTER TABLE items DISABLE ROW LEVEL SECURITY;
ALTER TABLE user_items DISABLE ROW LEVEL SECURITY;