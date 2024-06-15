import configparser

CONFIG_FILE = "./config.ini"

def read_config_generator(config_file=CONFIG_FILE):
    config = configparser.ConfigParser()
    config.read(config_file)

    # Retrieve values
    line: int = int(config.get("maze", "line"))
    column: int = int(config.get("maze", "column"))

    return line, column

def read_config_schematic(config_file=CONFIG_FILE):
    config = configparser.ConfigParser()
    config.read(config_file)

    # Retrieve values
    height: int = int(config.get("schematic", "height"))
    thickness_path: int = int(config.get("schematic", "thickness_path"))
    thickness_wall: int = int(config.get("schematic", "thickness_wall"))

    return height, thickness_path, thickness_wall