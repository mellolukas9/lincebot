import random
import json
import os
from datetime import datetime
from src.config import config  # Importa as configurações
from src.core.generate_profiles_json import generate_profiles_json
from src.utils.library import get_current_time
from src.utils.logger_config import setup_logger

logger = setup_logger()

def connect_to_profiles(browser, number_profiles, link):
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
        # connect_url = config['search_links']['connect']
        page.goto(link)

        # Caminho do diretório de dados (como string)
        data_path = config['paths']['data']

        # Garante que o diretório existe
        os.makedirs(data_path, exist_ok=True)
        
        temp = os.path.join(data_path, "temp.txt")

        try:
            with open(temp, 'r') as file:
                raw_profiles = eval(file.read())
        except:
            raw_profiles = []
            
        # raw_profiles = []
        counter = 0
        waiting_time = 0

        while counter < int(number_profiles):
            logger.info(f"Searching {number_profiles} profiles, {counter} already connected.")
            page.wait_for_timeout(timeout=3000)
            profiles = page.locator('div[data-view-name="search-entity-result-universal-template"]').all()

            for profile in profiles:
                profile.scroll_into_view_if_needed()
                connect_button = profile.locator('button[class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]')

                if connect_button.inner_text() == 'Conectar':  # Verifica o botão "Conectar"
                    waiting_time += random.randint(1000, 3000)
                    page.wait_for_timeout(timeout=waiting_time)

                    connect_button.click()
                    page.wait_for_timeout(timeout=2000)
                    page.locator('button[aria-label="Enviar sem nota"]').click()  # Enviar sem nota
                    page.wait_for_timeout(timeout=2000)

                    profile_text = profile.locator('div.pt3.pb3.t-12.t-black--light').inner_text()
                    profile_url = profile.locator('a').first.get_attribute("href")
                    profile_url = profile_url.split('?mini')[0]
                    profile_text = profile_text + '\n' + profile_url
                    profile_text = profile_text + '\n' + get_current_time()
                    raw_profiles.append(profile_text)
                    name = profile_text.split('\n')[0]

                    # Incrementa o contador
                    counter += 1
                    logger.info(f"Connected profile {counter} | {name}.")

                    if counter >= int(number_profiles):
                        logger.info(f"Connect to {counter} profiles, limit reached.")
                        break

            if counter < int(number_profiles):  # Caso o contador de perfis não tenha sido atingido
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                logger.info("Scrolling the page to load more profiles.")

                # Espera o botão "Avançar" aparecer e clica nele
                try:
                    next_button = page.locator('button[aria-label="Avançar"]')  # Botão "Avançar"
                    next_button.wait_for(state="visible", timeout=5000)
                    next_button.click()
                    logger.info("Clicking the 'Next' button.")
                except:
                    logger.error("Unable to click 'Next' button.")  # Log de erro
                    break  # Se o botão "Avançar" não for encontrado, encerre o loop.

        # Processa os perfis encontrados
        profile_json = generate_profiles_json(data=raw_profiles)
        logger.info(f"Processed {counter} profiles, generating JSON.")

        # Log de sucesso
        logger.info(f"Successful connection with {counter} profiles!")

        # Caminho para o arquivo JSON
        file_path = os.path.join(data_path, "connected.json")

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
        logger.error(f"Error while running LinkedIn Connector: {e}")

        with open(temp, 'w') as file:
            file.write(str(raw_profiles))

        return None  # Retorna None em caso de erro