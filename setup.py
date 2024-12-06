import sys
import os
from cx_Freeze import setup, Executable

# Check if minecraft.ttf exists
if os.path.exists("minecraft.ttf"):
    font_file = "minecraft.ttf"
else:
    font_file = None

# Dependencias
build_exe_options = {
    "packages": ["pygame", "cv2", "numpy"],
    "include_files": [
        "level_select.py",
        "level.py",
        "player.py",
        "solver.py",
        "img_buttons/",
        "img_box/",
        "img_celebration/",
        "img_inicio/",
        "img_levels/",
        "img_player/",
        "sounds/",
        "playita.mp4"
    ]
}

# Add minecraft.ttf to include_files if it exists
if font_file:
    build_exe_options["include_files"].append(font_file)

# Ejecutable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Sokoban",
    version="1.0",
    description="Juego Sokoban",
    options={"build_exe": build_exe_options},
    executables=[Executable("game.py", base=base)]
)

# Ejecutable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Sokoban",
    version="1.0",
    description="Juego Sokoban",
    options={"build_exe": build_exe_options},
    executables=[Executable("game.py", base=base)]
)