def clear_screen():
    import os
    import platform
    try:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
    except Exception:
        print("\n" * 50)
