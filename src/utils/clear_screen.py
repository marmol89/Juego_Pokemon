import os
import sys
import platform

def clear_screen() -> None:
    """Clears terminal screen cross-platform with TTY safety."""
    if not sys.stdout.isatty():
        return  # no-op for non-TTY (CI/redirected output)

    try:
        os.system('cls' if platform.system() == 'Windows' else 'clear')
    except OSError:
        # Fallback: simulate clear with newlines
        print('\n' * 50)
