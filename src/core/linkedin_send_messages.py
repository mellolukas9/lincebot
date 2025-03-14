import random
import json
import os
import logging
from src.utils.logger_config import logger  # Importando o logger configurado
from src.config import config  # Importa as configurações
from src.utils.library import get_current_time, type_slowly
from src.core.custom_message import evaluate_profile_and_respond

logger = logging.getLogger("LinkedInAutomation")

def send_messages_to_profiles(browser, profiles):
    """Visita os perfis do LinkedIn conforme o número especificado e exibe os logs."""
    
    # Log do início da execução
    logger.info("Starting the process of sending messages on LinkedIn.")
    
    try:
        # Obtém a página já aberta no navegador
        page = browser.pages[0]
        logger.info("Successfully opened browser, accessing LinkedIn homepage.")
        
        page.goto('https://www.linkedin.com')
        page.wait_for_timeout(timeout=3000)
        logger.info("LinkedIn home page loaded.")

        counter = 0
        waiting_time = 0

        for profile in profiles:

            waiting_time += random.randint(1000, 3000)
            page.wait_for_timeout(timeout=waiting_time)

            page.goto(profile['profile_link'])
            page.wait_for_timeout(timeout=2000)
            text_about = page.locator('div.display-flex.ph5.pv3').first.inner_text()
            name = profile['name']
            response = evaluate_profile_and_respond(name, text_about)
            # response = 'Teste'

            page.locator('use[href="#compose-small"]').click()
            input_search_name = page.locator('input[placeholder="Insira um ou mais nomes"]')
            type_slowly(input_search_name, name)
            page.wait_for_timeout(timeout=3000)
            page.keyboard.press('Enter')

            input_message = page.locator('div[aria-label="Escreva uma mensagem"]')
            type_slowly(input_message, response)
            page.wait_for_timeout(timeout=2000)
            page.locator('button[type="submit"]:has-text("Enviar")').click()
            profile['timestamp'] = get_current_time()
       
            # page.go_back()
            counter += 1
            logger.info(f"Profile {counter} visited.")

        # Caminho do diretório de dados (como string)
        data_dir = config['data']['dir']

        # Garante que o diretório existe
        os.makedirs(data_dir, exist_ok=True)

        # Caminho para o arquivo JSON
        file_path = os.path.join(data_dir, "sent_messages.json")

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
        return None  # Retorna None em caso de erroevaluate profile and respond
