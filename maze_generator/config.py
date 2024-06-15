import configparser


def read_config(config_file="./config"):
    config = configparser.ConfigParser()
    config.read(config_file)

    # Retrieve values
    line: int = int(config.get("maze", "line"))
    column: int = int(config.get("maze", "column"))

    return line, column
