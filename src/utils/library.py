import os
import glob
import json
import re
import time
from datetime import datetime

def get_last_created_file(directory, prefix):
    """
    Retorna o caminho do arquivo mais recente que começa com um prefixo específico, baseado na data de criação.

    :param directory: Caminho da pasta onde os arquivos estão.
    :param prefix: Prefixo do nome do arquivo (ex: "teste").
    :return: Caminho do último arquivo criado ou None se não encontrar.
    """
    files = glob.glob(os.path.join(directory, f"{prefix}*"))
    
    if not files:
        return None  # Retorna None se nenhum arquivo for encontrado
    
    # Retorna o arquivo mais recente com base na data de criação
    return max(files, key=os.path.getctime)

def read_json_file(file_path):
    """
    Lê um arquivo JSON e retorna os dados como um dicionário ou lista.

    :param file_path: Caminho do arquivo JSON.
    :return: Dados do JSON carregados.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Carrega o conteúdo do JSON
        return data

    except FileNotFoundError:
        # Se o arquivo não existir, retornar False
        print(f"File {file_path} not found.")
        return False

def filter_profiles(new_profiles, ignored_profiles):
    """
    Filtra perfis já visitados.

    :param new_profiles: Lista de dicionários contendo perfis coletados.
    :param ignored_profiles: Lista de dicionários contendo perfis já visitados.
    :return: Lista de perfis ainda não visitados.
    """
    ignored_names = {profile["name"] for profile in ignored_profiles if "name" in profile}
    return [profile for profile in new_profiles if profile["name"] not in ignored_names]

def filter_processed_profiles(all_profiles, processed_profiles):
    """
    Filtra perfis que já foram processados com sucesso.

    :param all_profiles: Lista de dicionários contendo todos os perfis.
    :param processed_profiles: Lista de dicionários contendo perfis que já passaram pelo processo com sucesso.
    :return: Lista de perfis que ainda não foram processados.
    """
    processed_names = {profile["name"] for profile in processed_profiles if "name" in profile}
    return [profile for profile in all_profiles if profile["name"] not in processed_names]

def is_name_in_json(name, file_path):
    """
    Verifica se um nome está presente no arquivo JSON na chave 'name'.

    :param name: O nome a ser verificado.
    :param filename: O nome do arquivo JSON onde os perfis estão armazenados.
    :return: True se o nome estiver presente no arquivo, False caso contrário.
    """
    # Carregar o conteúdo do arquivo JSON
    profiles = read_json_file(file_path)

    # Verificar se o nome está presente na chave 'name' de qualquer objeto no JSON
    for profile in profiles:
        if 'name' in profile and profile['name'] == name:
            return True

    return False

def get_current_time():
    """
    Retorna a data e hora atual no formato 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def remove_numbers_and_emojis(text):
    # Remove números e emojis, mantendo apenas letras e espaços
    return re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text)

def type_slowly(element, text, delay=0.1):
    # Limpa o campo de entrada antes de digitar devagar
    element.clear()
    time.sleep(0.5)  # Aguarda meio segundo após limpar o campo
    
    # Digita devagar no campo de entrada
    for char in text:
        element.type(char)
        time.sleep(delay)