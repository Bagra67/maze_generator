import mcschematic
from config import read_config_schematic


WALL = '⬜'
PATH = '🟦'
ENTRY = '🟩'
EXIT = '🟥'

def selected_block(char: str) -> str:
    block = 'minecraft:air'
    if char == WALL:
        block = 'minecraft:stone'
    elif char == ENTRY:
        block = 'minecraft:green_stained_glass'
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
    with open('./output.txt', 'r', encoding='utf-8') as template:
        content = template.readlines()

        for l, line in enumerate(content):
            # Print line by line

            # Transform each character of the line by its thickness
            transform_line = apply_thickness(line, thickness)
                
            #Loop to have the height we want
            for h in range(height):
                for c, char in enumerate(transform_line):
                    for t in range(thickness):
                        block = selected_block(char)
                        schem.setBlock((c, h, l*thickness + t), block)
                   
    schem.save("schematics", "test", mcschematic.Version.JE_1_18_2)
