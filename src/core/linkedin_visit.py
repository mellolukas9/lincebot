import random
from src.utils.logger_config import logger  # Importando o logger configurado
from src.config import config  # Importa as configurações
from src.core.generate_profiles_json import generate_profiles_json

def visit_to_profiles(browser, number_profiles):
    """Visita os perfis do LinkedIn conforme o número especificado e exibe os logs."""
    
    # Log do início da execução
    logger.info("Iniciando o processo de visitas no LinkedIn.")
    
    try:
        # Obtém a página já aberta no navegador
        page = browser.pages[0]
        logger.info("Navegador aberto com sucesso, acessando a página inicial do LinkedIn.")
        
        page.goto('https://www.linkedin.com')
        page.wait_for_timeout(timeout=3000)
        logger.info("Página inicial do LinkedIn carregada.")
        
        visit_url = config['search_links']['extract_profiles']['rpa_recruiters']
        # connect_url = connect_url = config['search_links']['visit']
        page.goto(visit_url)
        logger.info("Acessando a página de busca de pessoas no LinkedIn.")
        
        raw_profiles = []
        counter = 0
        waiting_time = 0

        while counter < int(number_profiles):
            logger.info(f"Buscando {number_profiles} perfis, {counter} já visitados.")
            page.wait_for_timeout(timeout=3000)
            profiles = page.locator('div[data-view-name="search-entity-result-universal-template"]').all()

            for profile in profiles:
                profile.scroll_into_view_if_needed()
                profile_text = profile.locator('div.pt3.pb3.t-12.t-black--light').inner_text()
                profile.click()
                
                waiting_time += random.randint(1000, 3000)
                page.wait_for_timeout(timeout=waiting_time)

                profile_text = profile_text + '\n' + page.url
                raw_profiles.append(profile_text)
                
                counter += 1
                page.go_back()

                if counter >= int(number_profiles):
                    logger.info(f"{counter} perfis visitados, atingido o limite.")
                    break

            if counter < int(number_profiles):  # Caso o contador de perfis não tenha sido atingido
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                logger.info("Rolando a página para carregar mais perfis.")

                # Espera o botão "Avançar" aparecer e clica nele
                try:
                    next_button = page.locator('button[aria-label="Avançar"]')  # Botão "Avançar"
                    next_button.wait_for(state="visible", timeout=5000)
                    next_button.click()
                    logger.info("Clicando no botão 'Avançar'.")
                except:
                    logger.error("Não foi possível clicar no botão 'Avançar'.")  # Log de erro
                    break  # Se o botão "Avançar" não for encontrado, encerre o loop.

        # Processa os perfis encontrados
        profile_json = generate_profiles_json(data=raw_profiles, action="visited")
        logger.info(f"Processados {counter} perfis, gerando o JSON.")

        # Log de sucesso
        logger.info(f"Visita bem-sucedida a {counter} perfis!")

        # Retorna os perfis
        return profile_json

    except Exception as e:
        # Log de erro
        logger.error(f"Erro durante a execução do LinkedIn Connector: {e}")
        return None  # Retorna None em caso de erro
