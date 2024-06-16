import configparser

CONFIG_FILE = "./config.ini"

def read_config_generator(config_file=CONFIG_FILE):
    config = configparser.ConfigParser()
    config.read(config_file)

    # Retrieve values
    line: int = int(config.get("maze", "line"))
    column: int = int(config.get("maze", "column"))

    
    
    entry_column: int = int(config.get("maze", "entry_column"))
    entry_line: int = int(config.get("maze", "entry_line"))

    if (entry_column != 0 and entry_column != column - 1) and (entry_line != 0 and entry_line != line - 1):
        raise ValueError("Your entry point must be on edge of the maze")

    return line, column, entry_column, entry_line

def read_config_schematic(config_file=CONFIG_FILE):
    config = configparser.ConfigParser()
    config.read(config_file)

    # Retrieve values
    height: int = int(config.get("schematic", "height"))
    thickness: int = int(config.get("schematic", "thickness"))

    return height, thickness