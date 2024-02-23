import yaml

def load_test_data(path):
    with open(path, 'r') as file:
        return yaml.safe_load(file)
