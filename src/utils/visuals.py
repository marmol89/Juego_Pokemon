import sys
import time
import os
import random

def type_text(text, delay=0.03):
    """Efecto de máquina de escribir para el texto."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def get_hp_bar_string(hp, max_hp, width=20):
    """Genera la cadena de la barra de vida."""
    percent = max(0, min(1, hp / max_hp))
    filled = int(percent * width)
    bar = '[' + '#' * filled + ' ' * (width - filled) + ']'
    return f"{bar} {hp}/{max_hp} HP"

def animate_hp_bar(old_hp, new_hp, max_hp, prefix="", width=20):
    """Anima la barra de vida bajando o subiendo."""
    step = 1 if new_hp > old_hp else -1
    current = old_hp
    
    while current != new_hp:
        current += step
        if (step == 1 and current > new_hp) or (step == -1 and current < new_hp):
            current = new_hp
            
        bar = get_hp_bar_string(current, max_hp, width)
        sys.stdout.write(f"\r{prefix}{bar}")
        sys.stdout.flush()
        time.sleep(0.02)
    print()

def shake_screen(intensity=2, duration=0.5):
    """Efecto de parpadeo para simular impacto."""
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write("\033[?25l") # Esconder cursor
        sys.stdout.flush()
        time.sleep(0.05)
        sys.stdout.write("\033[?25h") # Mostrar cursor
        sys.stdout.flush()
        time.sleep(0.05)

def get_key():
    """Detecta la pulsación de una tecla sin necesidad de Enter (Multiplataforma)."""
    try:
        # Windows
        import msvcrt
        char = msvcrt.getch()
        if char in [b'\x00', b'\xe0']: # Teclas especiales
            msvcrt.getch()
            return None
        try:
            return char.decode('utf-8').lower()
        except:
            return char
    except ImportError:
        # Linux/Mac
        try:
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch.lower()
        except:
            # Fallback último
            return sys.stdin.read(1).lower()
