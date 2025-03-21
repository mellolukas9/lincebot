from playwright.sync_api import sync_playwright
from src.config import config  # Import configurations

def start_playwright():
    """
    Inicia o Playwright e retorna a instância do navegador.
    Usa um contexto persistente para manter o perfil do usuário.
    """
    playwright = None
    browser = None

    try:
        playwright = sync_playwright().start()  # Manually start Playwright

        # Usa as configurações do config.yaml
        browser = playwright.chromium.launch_persistent_context(
            headless=config["settings"]["headless"],         # Headless mode
            user_data_dir=config["paths"]["user_data_dir"],  # Profile directory
            executable_path=config["paths"]["executable_path"]  # Chrome path
        )
        return browser, playwright
    except Exception as e:
        # Em caso de erro, fecha o navegador e o Playwright antes de relançar a exceção
        if browser:
            try:
                browser.close()
            except Exception as close_error:
                print(f"Error closing the browser: {close_error}")
        if playwright:
            try:
                playwright.stop()
            except Exception as stop_error:
                print(f"Error stopping Playwright: {stop_error}")
        raise Exception(f"Error starting Playwright: {e}")
    
def close_playwright(browser, playwright):
    """
    Fecha o navegador e o Playwright de maneira controlada.
    """
    try:
        if browser:
            print("Closing the browser...")
            browser.close()  # Close the browser
            print("Browser closed successfully.")
    except Exception as e:
        print(f"Error closing the browser: {e}")

    try:
        if playwright:
            print("Stopping Playwright...")
            playwright.stop()  # Stop Playwright
            print("Playwright stopped successfully.")
    except Exception as e:
        print(f"Error stopping Playwright: {e}")
