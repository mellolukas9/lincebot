import random
import json
import os
from src.utils.logger_config import setup_logger  # Importando o logger configurado
from src.config import config  # Importa as configurações
from src.core.generate_profiles_json import generate_profiles_json
from src.utils.library import is_name_in_json

logger = setup_logger()

def extract_profiles_to_process(browser, number_profiles, link, file_path):
    """Extrai os dados dos perfis do LinkedIn conforme o número especificado."""
    
    # Log do início da execução
    logger.info("Starting the LinkedIn extracted process.")
    
    try:
        # Obtém a página já aberta no navegador
        page = browser.pages[0]
        # logger.info("Successfully opened browser, accessing LinkedIn homepage.")
        
        page.goto('https://www.linkedin.com')
        page.wait_for_timeout(timeout=3000)
        logger.info("LinkedIn home page loaded.")
        
        logger.info("Accessing the profile search.")
        page.goto(link)
        
        raw_profiles = []
        counter = 0
        waiting_time = 0

        while counter < int(number_profiles):
            logger.info(f"Extracting {number_profiles} profiles, {counter} already extracted.")
            page.wait_for_timeout(timeout=3000)
            profiles = page.locator('div[data-view-name="search-entity-result-universal-template"]').all()

            if not profiles:
                profiles = page.locator('div[data-view-name="connections-list"] div div a[data-view-name="connections-profile"]').all()

            for profile in profiles:
                page.wait_for_timeout(timeout=2000)
                profile.scroll_into_view_if_needed()

                if profile.locator('div.pt3.pb3.t-12.t-black--light').is_visible():
                    profile_text = profile.locator('div.pt3.pb3.t-12.t-black--light').inner_text()
                else:
                    profile_text = profile.inner_text()
                    
                name = profile_text.split('\n')[0]

                if not is_name_in_json(name, file_path):
                    # waiting_time += random.randint(500, 1500)
                    # page.wait_for_timeout(timeout=waiting_time)

                    profile_url = profile.locator('a').first.get_attribute("href")
                    profile_url = profile_url.split('?mini')[0]
                    profile_text = profile_text + '\n' + profile_url
                    
                    profile_text = profile_text + '\n' + page.url
                    raw_profiles.append(profile_text)
                    
                    counter += 1
                    logger.info(f"Profile {counter} extracted.")

                    if counter >= int(number_profiles):
                        logger.info(f"{counter} profiles extracted, limit reached.")
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
        # logger.info(f"Processados {counter} perfis, gerando o JSON.")

        # Retorna os perfis
        return profile_json

    except Exception as e:
        # Log de erro
        logger.error(f"Error while running Extract Profiles: {e}")
        return None  # Retorna None em caso de erro