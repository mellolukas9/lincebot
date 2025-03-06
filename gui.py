import tkinter as tk
from tkinter import messagebox
import threading
import logging
from playwright_manager import start_playwright, close_playwright
from linkedin_connector import connect_to_profiles

# Configuração do logger
logger = logging.getLogger("LinkedInAutomation")
logger.setLevel(logging.DEBUG)

# Handler para o log que aparece na interface gráfica
class TkinterHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_message = self.format(record)
        self.text_widget.insert(tk.END, log_message + "\n")
        self.text_widget.yview(tk.END)
        window.update()

# Função de validação do número de perfis
def validate_number_input(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Função que será chamada ao clicar no botão
def visit():
    try:
        number_profiles = entry_profiles.get()  # Obter o número de perfis

        if not validate_number_input(number_profiles):
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        # Log no console e na interface gráfica
        logger.info("Starting the Playwright process...")

        # Inicia o Playwright
        browser, playwright = start_playwright()
        if not browser:
            messagebox.showerror("Error", "Failed to start Playwright.")
            return

        logger.info("Playwright started successfully.")

        # Conecta aos perfis do LinkedIn
        profile_json = connect_to_profiles(browser, number_profiles)

        # Exibe o resultado
        if profile_json:
            logger.info(f"Successfully sent connection requests to {int(number_profiles)} profiles!")
        else:
            logger.error("An error occurred during the process.")

        # Espera o usuário pressionar "Enter" antes de fechar
        # input("Press Enter to close the browser...")

        # Fecha o navegador após terminar
        browser.close()
        close_playwright(playwright)

    except Exception as e:
        messagebox.showerror("Error", f"Error while visiting profiles: {e}")
        logger.error(f"Error during execution: {e}")

# Função para executar a função visit em uma nova thread
def start_visit():
    threading.Thread(target=visit, daemon=True).start()

# Criar a janela principal
window = tk.Tk()
window.title("LinkedIn Automation")

# Ajustar o tamanho da janela e a cor de fundo
window.geometry("500x400")
window.config(bg="#f2f2f2")

# Título e estilização do título
title = tk.Label(window, text="LinkedIn Automation", font=("Arial", 18, "bold"), fg="#0e76a8", bg="#f2f2f2")
title.pack(pady=20)

# Layout da interface
label_profiles = tk.Label(window, text="Number of Profiles:", font=("Arial", 12), bg="#f2f2f2")
label_profiles.pack(pady=10)

# Input numérico com borda arredondada
entry_profiles = tk.Entry(window, font=("Arial", 12), validate="key", bd=2, relief="groove")
entry_profiles.pack(pady=10)

# Botão Connect
button_connect = tk.Button(window, text="Connect", font=("Arial", 12), bg="#0e76a8", fg="white", command=start_visit, relief="raised", width=20)
button_connect.pack(pady=10)

# Área de log
log_text = tk.Text(window, height=10, wrap=tk.WORD, font=("Arial", 10), bg="#f7f7f7", state=tk.NORMAL)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=20)

log_scrollbar = tk.Scrollbar(window, command=log_text.yview)
log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

log_text.config(yscrollcommand=log_scrollbar.set)

# Configurando o handler de logs para a interface gráfica
tk_handler = TkinterHandler(log_text)
tk_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
tk_handler.setFormatter(formatter)

# Adicionando o handler ao logger
logger.addHandler(tk_handler)

# Criando o handler para gravar os logs em arquivo
file_handler = logging.FileHandler("linkedin_automation.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Rodar a interface
window.mainloop()
