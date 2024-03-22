import yaml


# The load_data function is used to load data from a YAML file.
def load_data(path):
    with open(path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
