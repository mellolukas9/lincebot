import threading
from src.utils.logger_config import setup_logger
from src.core.playwright_manager import start_playwright, close_playwright
from src.core.linkedin_connector import connect_to_profiles
from src.core.linkedin_visit import visit_to_profiles
from src.core.linkedin_send_messages import send_messages_to_profiles

# Configurar o logger
logger = setup_logger()

# Configuração do logger
# logger = logging.getLogger("LinkedInAutomation")
# logger.setLevel(logging.DEBUG)

def validate_number_input(value):
    """
    Valida se o valor é um número inteiro positivo.

    :param value: Valor a ser validado.
    :return: True se for um número positivo, False caso contrário.
    """
    try:
        num = int(value)
        return num > 0
    except ValueError:
        return False

def execute_playwright_task(task, *args, logger=None, event=None, log_queue=None):
    """
    Executa uma tarefa usando o Playwright e gerencia a abertura e fechamento do navegador.

    :param task: Função que será executada com o navegador aberto.
    :param args: Argumentos para a função task.
    :param logger: Logger para registro de logs.
    :param event: Evento para sinalizar a conclusão da tarefa.
    :param log_queue: Queue para enviar logs para a interface gráfica.
    """
    browser = None
    playwright = None
    try:
        logger.info("Starting Playwright process...")
        if log_queue:
            log_queue.put("Starting Playwright process...")
        browser, playwright = start_playwright()
        if not browser:
            raise RuntimeError("Failed to start Playwright.")

        logger.info("Playwright started successfully.")
        if log_queue:
            log_queue.put("Playwright started successfully.")
        result = task(browser, *args)
        
        if result:
            logger.info(f"Task completed successfully.")
            if log_queue:
                log_queue.put(f"Task completed successfully.")
        else:
            logger.error("An error occurred during the task execution.")
            if log_queue:
                log_queue.put("An error occurred during the task execution.")

    except Exception as e:
        logger.error(f"Error during execution: {e}")
        if log_queue:
            log_queue.put(f"Error during execution: {e}")
        raise

    finally:
        if browser or playwright:
            close_playwright(browser, playwright)
        logger.info("Playwright process completed.")
        if log_queue:
            log_queue.put("Playwright process completed.")
        if event:
            event.set()

def connect(number_profiles, link, logger, event, log_queue):
    """
    Conecta a um número específico de perfis no LinkedIn.

    :param number_profiles: Número de perfis a serem conectados.
    :param logger: Logger para registro de logs.
    :param event: Evento para sinalizar a conclusão da tarefa.
    :param log_queue: Queue para enviar logs para a interface gráfica.
    """
    if not validate_number_input(number_profiles):
        raise ValueError("Please enter a valid positive number of profiles.")

    execute_playwright_task(connect_to_profiles, number_profiles, link, logger=logger, event=event, log_queue=log_queue)

def visit(number_profiles, link, logger, event, log_queue):
    """
    Visita um número específico de perfis no LinkedIn.

    :param number_profiles: Número de perfis a serem visitados.
    :param logger: Logger para registro de logs.
    :param event: Evento para sinalizar a conclusão da tarefa.
    :param log_queue: Queue para enviar logs para a interface gráfica.
    """
    if not validate_number_input(number_profiles):
        raise ValueError("Please enter a valid positive number of profiles.")

    execute_playwright_task(visit_to_profiles, number_profiles, link, logger=logger, event=event, log_queue=log_queue)

def send_messages(profiles, logger, event, log_queue):
    """
    Envia mensagens para uma lista de perfis no LinkedIn.

    :param profiles: Lista de perfis para enviar mensagens.
    :param logger: Logger para registro de logs.
    :param event: Evento para sinalizar a conclusão da tarefa.
    :param log_queue: Queue para enviar logs para a interface gráfica.
    """
    execute_playwright_task(send_messages_to_profiles, profiles, logger=logger, event=event, log_queue=log_queue)

def run_connect(number_profiles, link, logger, log_queue):
    """
    Executa a tarefa de conexão com perfis do LinkedIn.

    :param number_profiles: Número de perfis a serem conectados.
    :param logger: Logger para registro de logs.
    :param log_queue: Queue para enviar logs para a interface gráfica.
    """
    event = threading.Event()
    thread = threading.Thread(target=connect, args=(number_profiles, link, logger, event, log_queue), daemon=True)
    thread.start()
    event.wait()

def run_visit(number_profiles, link, logger, log_queue):
    """
    Executa a tarefa de visita a perfis do LinkedIn.

    :param number_profiles: Número de perfis a serem visitados.
    :param logger: Logger para registro de logs.
    :param log_queue: Queue para enviar logs para a interface gráfica.
    """
    event = threading.Event()
    thread = threading.Thread(target=visit, args=(number_profiles, link, logger, event, log_queue), daemon=True)
    thread.start()
    event.wait()

def run_send_messages(profiles, link, logger, log_queue):
    """
    Executa a tarefa de envio de mensagens a perfis do LinkedIn.

    :param profiles: Lista de perfis para enviar mensagens.
    :param logger: Logger para registro de logs.
    :param log_queue: Queue para enviar logs para a interface gráfica.
    """
    event = threading.Event()
    thread = threading.Thread(target=send_messages, args=(profiles, link, logger, event, log_queue), daemon=True)
    thread.start()
    event.wait()