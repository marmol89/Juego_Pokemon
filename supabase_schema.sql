-- Corre esto en el Editor SQL de Supabase para inicializar tu base de datos

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(600) NOT NULL
);

CREATE TABLE pokemons (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipos JSONB NOT NULL,
    movimientos JSONB NOT NULL,
    "EVs" JSONB NOT NULL,
    puntos_de_salud INT NOT NULL
);

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    enemigo_id INT REFERENCES users(id) ON DELETE CASCADE,
    nombre VARCHAR(255) NOT NULL,
    estado INT DEFAULT 0
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    room_id INT REFERENCES rooms(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    pokemon_id INT REFERENCES pokemons(id) ON DELETE CASCADE,
    active BOOLEAN DEFAULT false,
    vida INT,
    efecto VARCHAR(255)
);

CREATE TABLE battles (
    id SERIAL PRIMARY KEY,
    room_id INT UNIQUE REFERENCES rooms(id) ON DELETE CASCADE,
    winner_id INT REFERENCES users(id) ON DELETE CASCADE,
    loser_id INT REFERENCES users(id) ON DELETE CASCADE,
    user_team_ids JSONB,
    enemy_team_ids JSONB
);

CREATE TABLE movements (
    id SERIAL PRIMARY KEY,
    room_id INT REFERENCES rooms(id) ON DELETE CASCADE,
    pokemon_id INT REFERENCES pokemons(id) ON DELETE CASCADE,
    nombre VARCHAR(255) NOT NULL,
    efecto VARCHAR(255) NOT NULL
);

-- Desactivar Row Level Security (RLS) para permitir lectura/escritura libre desde Python
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE pokemons DISABLE ROW LEVEL SECURITY;
ALTER TABLE rooms DISABLE ROW LEVEL SECURITY;
ALTER TABLE teams DISABLE ROW LEVEL SECURITY;
ALTER TABLE battles DISABLE ROW LEVEL SECURITY;
ALTER TABLE movements DISABLE ROW LEVEL SECURITY;

-- Insertar Pokemons Iniciales
INSERT INTO pokemons (nombre, tipos, movimientos, "EVs", puntos_de_salud) VALUES 
('Charizard', '["FUEGO", "VOLADOR"]', '[{"nombre": "Ascuas", "tipo": "FUEGO", "poder": 25, "PP": 40, "Prec": 100}, {"nombre": "Onda ígnea", "tipo": "FUEGO", "poder": 10, "PP": 95, "Prec": 90}]', '{"ataque": 84, "defensa": 78, "velocidad": 100}', 78),
('Venusaur', '["PLANTA", "VENENO"]', '[{"nombre": "Hoja afilada", "tipo": "PLANTA", "poder": 25, "PP": 55, "Prec": 95}, {"nombre": "Placaje", "tipo": "NORMAL", "poder": 35, "PP": 50, "Prec": 100}]', '{"ataque": 82, "defensa": 83, "velocidad": 80}', 80);
