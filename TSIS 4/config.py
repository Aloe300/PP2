from configparser import ConfigParser
import os

def load_config(filename="database.ini", section="postgresql"):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    candidates = [
        os.path.join(base_dir, filename),
        filename,
        os.path.join(base_dir, "practice 7", "database.ini"),
        os.path.join(base_dir, "Practice7", "database.ini"),
        os.path.join(os.path.dirname(base_dir), "TSIS 1", "database.ini"),
        os.path.join(os.path.dirname(base_dir), "TSIS1", "database.ini"),
    ]

    parser = ConfigParser()
    read_files = parser.read(candidates)

    if not parser.has_section(section):
        raise Exception(
            f"Section {section} not found. Checked: {candidates}. Read files: {read_files}"
        )

    config = {}
    for key, value in parser.items(section):
        config[key] = value

    return config
