from playwright.sync_api import sync_playwright

def start_playwright():
    """Inicia o Playwright e retorna a instância do navegador sem depender do 'with'."""
    playwright = sync_playwright().start()  # Inicia o Playwright manualmente
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=r'C:\\Users\\Lucas\\AppData\\Local\\Google\\Chrome\\User Data',  # Diretório do perfil
        headless=False,  # Não headless para visualizar o navegador
        executable_path=r'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'  # Caminho do Chrome
    )
    return browser, playwright  # Retorna tanto o browser quanto o playwright

def close_playwright(playwright):
    """Fecha o Playwright e o navegador de maneira controlada."""
    playwright.stop()  # Para o Playwright explicitamente
