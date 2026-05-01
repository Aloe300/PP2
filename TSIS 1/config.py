from configparser import ConfigParser
import os


def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(base_dir, filename),
        filename,
        os.path.join(base_dir, 'practice 7', 'database.ini'),
        os.path.join(base_dir, 'Practice7', 'database.ini'),
    ]

    read_files = parser.read(possible_paths)

    if parser.has_section(section):
        return dict(parser.items(section))

    raise Exception(
        f'Section {section} not found. Checked: {possible_paths}. Read files: {read_files}'
    )


if __name__ == '__main__':
    config = load_config()
    print(config)
