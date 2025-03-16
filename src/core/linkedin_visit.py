import random
import json
import os
from src.utils.logger_config import setup_logger  # Importando o logger configurado
from src.config import config  # Importa as configurações
from src.core.extract_profiles import extract_profiles_to_visit
from src.utils.library import get_current_time

logger = setup_logger()

def visit_to_profiles(browser, number_profiles):
    """Visita os perfis do LinkedIn conforme o número especificado e exibe os logs."""
    
    # Log do início da execução
    logger.info("Starting the LinkedIn visits process.")
    
    try:
        # Obtém a página já aberta no navegador
        page = browser.pages[0]
        logger.info("Successfully opened browser, accessing LinkedIn homepage.")
        
        page.goto('https://www.linkedin.com')
        page.wait_for_timeout(timeout=3000)
        logger.info("LinkedIn home page loaded.")

        new_profiles = extract_profiles_to_visit(browser, number_profiles)
        profiles = new_profiles

        # processed_profiles = []
        counter = 0
        waiting_time = 0
        
        for profile in profiles:

            waiting_time += random.randint(1000, 3000)
            page.wait_for_timeout(timeout=waiting_time)
            
            name = profile['name']
            logger.info(f"Visiting {name} profiles.")
            link = profile['profile_link']
            page.goto(link)
            profile['timestamp'] = get_current_time()
       
            # page.go_back()
            counter += 1
            logger.info(f"Profile {counter} visited.")

            if counter >= number_profiles:
                break

        # Caminho do diretório de dados (como string)
        data_dir = config['data']['dir']

        # Garante que o diretório existe
        os.makedirs(data_dir, exist_ok=True)

        # Caminho para o arquivo JSON
        file_path = os.path.join(data_dir, "visited.json")

        # Carregar o conteúdo atual do arquivo, se ele existir
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_profiles = json.load(f)
        except FileNotFoundError:
            # Se o arquivo não existir, iniciar uma lista vazia
            existing_profiles = []

        # Adicionar os novos perfis à lista existente
        existing_profiles.extend(profiles)

        # Salvar a lista atualizada no arquivo
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_profiles, f, ensure_ascii=False, indent=4)

        return profiles

    except Exception as e:
        # Log de erro
        logger.error(f"Error while running LinkedIn Visit: {e}")
        return None  # Retorna None em caso de erro
