import logging
import threading
from src.core.playwright_manager import start_playwright, close_playwright
from src.core.linkedin_connector import connect_to_profiles
from src.core.linkedin_visit import visit_to_profiles

# Configuração do logger
logger = logging.getLogger("LinkedInAutomation")
logger.setLevel(logging.DEBUG)

# Função de validação do número de perfis
def validate_number_input(value):
    try:
        num = int(value)
        if num > 0:
            return True
        return False
    except ValueError:
        return False

# Função que será chamada ao clicar no botão
def connect(number_profiles, logger, event):
    try:
        logger.info("Starting visit function.")
        if not validate_number_input(number_profiles):
            raise ValueError("Please enter a valid positive number of profiles.")

        # Log no console e na interface gráfica
        logger.info("Starting the Playwright process...")

        # Inicia o Playwright
        browser, playwright = start_playwright()
        if not browser:
            raise RuntimeError("Failed to start Playwright.")

        logger.info("Playwright started successfully.")

        # Conecta aos perfis do LinkedIn
        profile_json = connect_to_profiles(browser, number_profiles)

        # Exibe o resultado
        if profile_json:
            logger.info(f"Successfully sent connection requests to {int(number_profiles)} profiles!")
        else:
            logger.error("An error occurred during the process.")

    except Exception as e:
        logger.error(f"Error during execution: {e}")
        raise

    finally:
        # Fecha o navegador após terminar
        close_playwright(browser, playwright)
        logger.info("Visit function completed.")
        event.set()

# Função que será chamada ao clicar no botão
def visit(number_profiles, logger, event):
    try:
        logger.info("Starting visit function.")
        if not validate_number_input(number_profiles):
            raise ValueError("Please enter a valid positive number of profiles.")

        # Log no console e na interface gráfica
        logger.info("Starting the Playwright process...")

        # Inicia o Playwright
        browser, playwright = start_playwright()
        if not browser:
            raise RuntimeError("Failed to start Playwright.")

        logger.info("Playwright started successfully.")

        # Conecta aos perfis do LinkedIn
        profile_json = visit_to_profiles(browser, number_profiles)

        # Exibe o resultado
        if profile_json:
            logger.info(f"Successfully visit requests to {int(number_profiles)} profiles!")
        else:
            logger.error("An error occurred during the process.")

    except Exception as e:
        logger.error(f"Error during execution: {e}")
        raise

    finally:
        # Fecha o navegador após terminar
        close_playwright(browser, playwright)
        logger.info("Visit function completed.")
        event.set()

# Função para executar a função visit em uma nova thread
def start_process(number_profiles, logger, process):
    # Cria o evento
    event = threading.Event()
    
    # Cria a thread para executar a função visit
    if process == 'connect':
        thread = threading.Thread(target=connect, args=(number_profiles, logger, event), daemon=True)
    elif process == 'visit':
        thread = threading.Thread(target=visit, args=(number_profiles, logger, event), daemon=True)
    
    # Inicia a thread
    thread.start()
    
    # Retorna o evento para garantir que a execução foi completada
    return event

# Função principal
# def main():
#     """Função principal que inicia o processo de conexão."""
#     number_profiles = 5  # Número de perfis a serem conectados
#     event = start_visit(number_profiles, logger)
#     event.wait()  # Aguarda a execução da thread terminar

# if __name__ == "__main__":
#     main()
