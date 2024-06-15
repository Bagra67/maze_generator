import mcschematic
from config import read_config_schematic

def create():
    height, thickness_path, thickness_wall = read_config_schematic()

    schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
    schem.setBlock(  (0, -1, 0), "minecraft:stone"  )
    schem.save("schematics", "test", mcschematic.Version.JE_1_18_2)
