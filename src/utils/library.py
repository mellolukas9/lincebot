import os
import glob

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

import json

def filter_profiles(new_profiles, ignored_profiles):
    """
    Filtra perfis já visitados.

    :param new_profiles: Lista de dicionários contendo perfis coletados.
    :param ignored_profiles: Lista de dicionários contendo perfis já visitados.
    :return: Lista de perfis ainda não visitados.
    """
    ignored_names = {profile["name"] for profile in ignored_profiles if "name" in profile}
    return [profile for profile in new_profiles if profile["name"] not in ignored_names]
