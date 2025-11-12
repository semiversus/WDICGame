import pygame
from pathlib import Path

def time():
    return pygame.time.get_ticks() / 1000.0

def get_asset_path(filename: Path) -> Path:
    return Path(__file__).parent / f"../../assets/{filename}"