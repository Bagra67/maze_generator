import mcschematic
from config import read_config_schematic


WALL = '⬜'
PATH = '🟦'
ENTRY = '🟩'
EXIT = '🟥'


def create():
    height, thickness_path, thickness_wall = read_config_schematic()

    schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
    with open('./output.txt', 'r', encoding='utf-8') as template:
        content = template.readlines()

        for l, line in enumerate(content):
            for c, char in enumerate(line):
                block = 'minecraft:air'
                if char == WALL:
                    block = 'minecraft:stone'
                elif char == ENTRY:
                    block = 'minecraft:green_stained_glass'
                elif char == EXIT:
                    block = 'minecraft:red_stained_glass'

                for h in range(height):
                    schem.setBlock((c, h, l), block)
    schem.save("schematics", "test", mcschematic.Version.JE_1_18_2)
