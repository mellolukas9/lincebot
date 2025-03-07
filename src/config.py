import os
import yaml

def load_config():
    # Caminho para o arquivo config.yaml
    config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    
    # Carrega o arquivo YAML
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    
    return config

# Carrega as configurações ao importar o módulo
config = load_config()