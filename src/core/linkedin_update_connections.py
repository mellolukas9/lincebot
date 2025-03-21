import random
import json
import os
from datetime import datetime
from src.config import config  # Importa as configurações
from src.core.generate_profiles_json import generate_profiles_json
from src.utils.library import get_current_time, extract_numbers
from src.utils.logger_config import setup_logger

logger = setup_logger()

def update_connections_on_linkedin(browser, link):
    """Conecta aos perfis do LinkedIn conforme o número especificado."""
    
    # Log do início da execução
    logger.info("Starting the LinkedIn connection process.")
    
    try:
        # Obtém a página já aberta no navegador
        page = browser.pages[0]
        logger.info("Successfully opened browser, accessing LinkedIn homepage.")
        
        page.goto('https://www.linkedin.com')
        page.wait_for_timeout(timeout=3000)
        logger.info("LinkedIn home page loaded.")
        
        logger.info("Accessing the profile search.")
        page.goto(link)

        # Caminho do diretório de dados (como string)
        data_path = config['paths']['data']

        # Garante que o diretório existe
        os.makedirs(data_path, exist_ok=True)

        logger.info("Extracting connections from LinkedIn.")
        page.wait_for_timeout(timeout=5000)

        # Caminho para o arquivo JSON
        file_path = os.path.join(data_path, "connections.json")

        # Abre o arquivo JSON para leitura
        with open(file_path, 'r', encoding='utf-8') as file:
            # Usa json.load para ler o arquivo JSON
            connections_data = json.load(file)  # Corrigido: json.load em vez de json.loads

        number_connections = page.locator('p').first
        number_connections.click()
        number = extract_numbers(number_connections.inner_text())
        number = number - len(connections_data)
        number = (number * 3)

        for _ in range(number):  # Ajuste o número de repetições conforme necessário
            page.keyboard.press('ArrowDown')  # Simula o pressionamento da seta para baixo
            page.wait_for_timeout(timeout=100)

        profiles = page.locator('div[data-view-name="connections-list"] div div a[data-view-name="connections-profile"]')
        profiles = profiles.all()
        
        counter = 0
        raw_profiles = []

        for profile in profiles: 
            profile.scroll_into_view_if_needed()
            page.wait_for_timeout(timeout=800)

            # waiting_time += random.randint(1000, 3000)
            # waiting_time = random.randint(1000, 2000)
            # page.wait_for_timeout(timeout=waiting_time)
            profile.scroll_into_view_if_needed()

            profile_text = profile.inner_text()
            profile_url = profile.locator('a').first.get_attribute("href")
            profile_url = profile_url.split('?mini')[0]
            profile_text = profile_text + '\n' + profile_url
            profile_text = profile_text + '\n' + get_current_time()
            name = profile_text.split('\n')[0]

            if connections_data[0]['name'] == name:
                break

            raw_profiles.append(profile_text)

            logger.info(f"Connection {counter} | {name}.")
            # Incrementa o contador
            counter += 1

        logger.info(f'{counter} new connections')
        # Lista para armazenar os lotes
        profile_json = []
        profile_temp = []

        logger.info('Processing new profiles...')
        # Processa os registros e divide em lotes de 100
        for i, registro in enumerate(raw_profiles, start=1):
            profile_temp.append(registro)
            
            if i % 30 == 0:
                profile_json.extend(generate_profiles_json(data=profile_temp))  # Adiciona o lote completo à lista de lotes
                profile_temp = []  # Reinicia o lote
                # logger.info(f'Out of {len(raw_profiles)} profiles, {i} were processed ')

        # Adiciona os registros restantes (caso tenha menos de 100 no último lote)
        if profile_temp:
            profile_json.extend(generate_profiles_json(data=profile_temp)) 

        # Processa os perfis encontrados
        # profile_json = generate_profiles_json(data=raw_profiles)
        logger.info(f"Processed {counter} profiles, generating JSON.")

        # Log de sucesso
        logger.info(f"{counter} connections successfully extracted!")

        # Carregar o conteúdo atual do arquivo, se ele existir
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_profiles = json.load(f)
        except FileNotFoundError:
            # Se o arquivo não existir, iniciar uma lista vazia
            existing_profiles = []

        # Adicionar os novos perfis à lista existente
        existing_profiles.extend(profile_json)

        # Salvar a lista atualizada no arquivo
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_profiles, f, ensure_ascii=False, indent=4)

        # Retorna os perfis conectados
        return profile_json

    except Exception as e:
        # Log de erro
        logger.error(f"Error while running LinkedIn Update Connections: {e}")

        return None  # Retorna None em caso de erro