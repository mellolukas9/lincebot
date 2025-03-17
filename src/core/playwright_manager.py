from playwright.sync_api import sync_playwright
from src.config import config  # Importa as configurações

def start_playwright():
    """
    Inicia o Playwright e retorna a instância do navegador.
    Usa um contexto persistente para manter o perfil do usuário.
    """
    playwright = None
    browser = None

    try:
        playwright = sync_playwright().start()  # Inicia o Playwright manualmente

        # Usa as configurações do config.yaml
        browser = playwright.chromium.launch_persistent_context(
            headless=config["settings"]["headless"],         # Modo headless
            user_data_dir=config["paths"]["user_data_dir"],  # Diretório do perfil
            executable_path=config["paths"]["executable_path"]  # Caminho do Chrome
        )
        return browser, playwright
    except Exception as e:
        # Em caso de erro, fecha o navegador e o Playwright antes de relançar a exceção
        if browser:
            try:
                browser.close()
            except Exception as close_error:
                print(f"Erro ao fechar o navegador: {close_error}")
        if playwright:
            try:
                playwright.stop()
            except Exception as stop_error:
                print(f"Erro ao parar o Playwright: {stop_error}")
        raise Exception(f"Erro ao iniciar o Playwright: {e}")
    
def close_playwright(browser, playwright):
    """
    Fecha o navegador e o Playwright de maneira controlada.
    """
    try:
        if browser:
            print("Fechando o navegador...")
            browser.close()  # Fecha o navegador
            print("Navegador fechado com sucesso.")
    except Exception as e:
        print(f"Erro ao fechar o navegador: {e}")

    try:
        if playwright:
            print("Parando o Playwright...")
            playwright.stop()  # Para o Playwright
            print("Playwright parado com sucesso.")
    except Exception as e:
        print(f"Erro ao parar o Playwright: {e}")