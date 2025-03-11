import random
from src.utils.logger_config import logger  # Importando o logger configurado
from src.config import config  # Importa as configurações
from src.core.generate_profiles_json import generate_profiles_json

def connect_to_profiles(browser, number_profiles, log_window=None):
    """Conecta aos perfis do LinkedIn conforme o número especificado e exibe os logs."""
    
    # Log do início da execução
    logger.info("Iniciando o processo de conexão com o LinkedIn.")
    
    try:
        # Obtém a página já aberta no navegador
        page = browser.pages[0]
        logger.info("Navegador aberto com sucesso, acessando a página inicial do LinkedIn.")
        
        page.goto('https://www.linkedin.com')
        page.wait_for_timeout(timeout=3000)
        logger.info("Página inicial do LinkedIn carregada.")
        
        connect_url = config['search_links']['connect']
        page.goto(connect_url)
        logger.info("Acessando a página de busca de pessoas no LinkedIn.")
        
        temp = f'{config['data']['dir']}temp.txt'

        try:
            with open(temp, 'r') as file:
                raw_profiles = eval(file.read())
        except:
            raw_profiles = []
            
        # raw_profiles = []
        counter = 0
        waiting_time = 0

        while counter < int(number_profiles):
            logger.info(f"Buscando {number_profiles} perfis, {counter} já conectados.")
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

                    profile_text = profile.locator('div.pt3.pb3.t-12.t-black--light').inner_text()
                    profile_url = profile.locator('a').first.get_attribute("href")
                    profile_url = profile_url.split('?mini')[0]
                    profile_text = profile_text + '\n' + profile_url
                    raw_profiles.append(profile_text)
                    name = profile_text.split('\n')[0]

                    # Incrementa o contador
                    counter += 1
                    logger.info(f"Conectando ao perfil {counter} | {name}.")

                    if counter >= int(number_profiles):
                        logger.info(f"Conectado a {counter} perfis, atingido o limite.")
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
        profile_json = generate_profiles_json(data=raw_profiles, action="connected")
        logger.info(f"Processados {counter} perfis, gerando o JSON.")

        # Log de sucesso
        logger.info(f"Conexão bem-sucedida com {counter} perfis!")

        # Criar ou sobrescrever o arquivo, deixando-o vazio
        with open(temp, 'w') as file:
            pass  # Não escreve nada, apenas mantém o arquivo vazio

        # Retorna os perfis conectados
        return profile_json

    except Exception as e:
        # Log de erro
        logger.error(f"Erro durante a execução do LinkedIn Connector: {e}")

        with open(temp, 'w') as file:
            file.write(str(raw_profiles))

        return None  # Retorna None em caso de erro