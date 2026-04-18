# 🎮 Pokémon Multiplayer Terminal 🚀

![Status](https://github.com/marmol89/Juego_Pokemon/actions/workflows/build.yml/badge.svg)
![Version](https://img.shields.io/badge/version-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-yellow)

### Una experiencia de combate Pokémon competitiva, sincronizada en tiempo real y optimizada para terminales modernos.

---

## ✨ Características Principales

- **🛰️ Multijugador Real-Time**: Sincronización instantánea mediante Supabase Realtime.
- **⚡ Control One-Touch**: Navegación rápida mediante hotkeys (sin necesidad de Enter).
- **📟 Estética RPG Retro**: Interfaz ASCII premium diseñada para la terminal.
- **📱 Multiplataforma**: Soporte nativo y optimizado para **Windows, Linux y macOS**.
- **💥 Sistema de Combate Avanzado**:
  - Stats reales de la Gen 1 (PokeAPI).
  - Sistema de rendición sincronizado sin bloqueos.
  - Gestión de mochila e inventario.
  - Sistema de Ranking y Puntuación.

## 🛠️ Tecnologías Utilizadas

- **Backend**: [Supabase](https://supabase.com/) (Database & Realtime).
- **Data Source**: [PokeAPI](https://pokeapi.co/).
- **Engine**: Python 3.
- **Build System**: [PyInstaller](https://pyinstaller.org/) & GitHub Actions.

## 🚀 Instalación Rápida

### 1. Clonar el repositorio
```bash
git clone https://github.com/marmol89/Juego_Pokemon.git
cd Juego_Pokemon
```

### 2. Configurar el entorno
Crea un archivo `.env` en la raíz con tus credenciales de Supabase:
```env
SUPABASE_URL=tu_url_aqui
SUPABASE_KEY=tu_key_aqui
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Inicializar base de datos (Opcional)
```bash
python dbInicio.py
```

### 5. ¡Jugar!
```bash
python app.py
```

## 📦 Descargas (Ejecutables)

¿No tienes Python instalado? ¡No hay problema! Puedes descargar la versión ejecutable directamente desde la sección de **[Releases](https://github.com/marmol89/Juego_Pokemon/releases)**.

- **JuegoPokemon-windows.exe**: Solo descarga y ejecuta.
- **JuegoPokemon-linux**: Binario para distribuciones Linux.
- **JuegoPokemon-macos**: Versión para sistemas Apple.

---

## 📸 Screenshots (Próximamente)

> _Desarrollado con ❤️ por marmol89
