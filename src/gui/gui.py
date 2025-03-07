import tkinter as tk
from tkinter import messagebox
import logging
import sys
import os

# Adiciona a pasta 'src' ao path do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.main import start_visit  # Agora deve funcionar

# Configuração da janela principal
window = tk.Tk()
window.title("LinkedIn Automation")
window.geometry("500x400")
window.config(bg="#f2f2f2")

# Título
title = tk.Label(window, text="LinkedIn Automation", font=("Arial", 18, "bold"), fg="#0e76a8", bg="#f2f2f2")
title.pack(pady=20)

# Campo de entrada para número de perfis
label_profiles = tk.Label(window, text="Number of Profiles:", font=("Arial", 12), bg="#f2f2f2")
label_profiles.pack(pady=5)

entry_profiles = tk.Entry(window, font=("Arial", 12), validate="key", bd=2, relief="groove")
entry_profiles.pack(pady=5)

# Função do botão Connect
def on_connect():
    num_profiles = entry_profiles.get()
    if not num_profiles.isdigit():
        messagebox.showerror("Erro", "Por favor, insira um número válido.")
        return
    logger.info(f"Iniciando visita para {num_profiles} perfis.")
    start_visit(int(num_profiles), logger)

# Botão Connect
button_connect = tk.Button(window, text="Connect", font=("Arial", 12), bg="#0e76a8", fg="white",
                           command=on_connect, relief="raised", width=20)
button_connect.pack(pady=10)

# Área de log com scrollbar
frame_log = tk.Frame(window)
frame_log.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

log_text = tk.Text(frame_log, height=10, wrap=tk.WORD, font=("Arial", 10), bg="#f7f7f7", state=tk.DISABLED)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

log_scrollbar = tk.Scrollbar(frame_log, command=log_text.yview)
log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=log_scrollbar.set)

# Handler para exibir logs na interface gráfica
class TkinterHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_message = self.format(record)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, log_message + "\n")
        self.text_widget.config(state=tk.DISABLED)
        self.text_widget.yview(tk.END)
        self.text_widget.update_idletasks()

# Configuração do logger
logger = logging.getLogger("LinkedInAutomation")
logger.setLevel(logging.DEBUG)

# Log na interface
tk_handler = TkinterHandler(log_text)
tk_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
tk_handler.setFormatter(formatter)
logger.addHandler(tk_handler)

# Log em arquivo
file_handler = logging.FileHandler("linkedin_automation.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# # Função do botão Connect
# def on_connect():
#     num_profiles = entry_profiles.get()
#     if not num_profiles.isdigit():
#         messagebox.showerror("Erro", "Por favor, insira um número válido.")
#         return
#     logger.info(f"Iniciando visita para {num_profiles} perfis.")
#     start_visit(int(num_profiles), logger)

# # Botão Connect
# button_connect = tk.Button(window, text="Connect", font=("Arial", 12), bg="#0e76a8", fg="white",
#                            command=on_connect, relief="raised", width=20)
# button_connect.pack(pady=10)

# Iniciar interface gráfica
window.mainloop()
