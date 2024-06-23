import mcschematic


def create():
    schem: mcschematic.MCSchematic = mcschematic.MCSchematic()
    
    for h in range(17):
        for i in range(5):
            for j in range(5):
                if h in [0,1,2,16,15,14]:
                    block = 'minecraft:chiseled_tuff_bricks'
                elif h == 8:
                    block = 'minecraft:chiseled_tuff'
                else: 
                    block = 'minecraft:tuff_bricks'
                schem.setBlock((i, h, j), block)
                   
    schem.save("schematics", "pylon", mcschematic.Version.JE_1_21)




create()