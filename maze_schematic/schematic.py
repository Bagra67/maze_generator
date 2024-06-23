from typing import Tuple
import mcschematic
from config import read_config_schematic


WALL = '⬜'
PATH = '🟦'
ENTRY = '🟩'
EXIT = '🟥'

def print_char(char: str, shem:  mcschematic.MCSchematic, coord: Tuple[int]) -> str:
    c ,h ,l = coord
    if char == ENTRY:
        pass
    elif char == EXIT:
        block = 'minecraft:red_stained_glass'
    
    return block

def apply_thickness(line, thickness) -> list[str]:
    transform_line = []
    for char in line: 
        for _ in range(thickness):
            transform_line.append(char)

    return transform_line

def create():
    height, thickness = read_config_schematic()

    schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
    pylon = mcschematic.MCSchematic = mcschematic.MCSchematic('./schematics/pylon.schem')
    with open('./output.txt', 'r', encoding='utf-8') as template:
        content = template.readlines()

        for l, line in enumerate(content):
            for c, char in enumerate(line):
                if char == WALL:
                    schem.placeSchematic(pylon,(c*thickness,0,l*thickness))
         
                   
        schem.save("schematics", "test", mcschematic.Version.JE_1_21)
