import tkinter as tk
from tkinter import ttk
import sys
import threading
from .dashboard import show_dashboard
from .visit import show_visit
from .connect import show_connect
from .messages import show_messages
from .links import manage_links_ui
from src.utils.logger_config import setup_logger

# Configuração da janela principal
window = tk.Tk()
window.title("LinceBot Automation")
window.geometry("800x600")

# Lista para armazenar threads ativas
active_threads = []

# Função para fechar a aplicação corretamente
def on_closing():
    """Função chamada ao fechar a janela."""
    # Encerra todas as threads ativas
    for thread in active_threads:
        if thread.is_alive():
            thread.join()  # Aguarda a finalização da thread

    # Fecha a janela do Tkinter
    window.destroy()

    # Encerra o programa
    sys.exit()

# Vincular a função ao evento de fechamento da janela
window.protocol("WM_DELETE_WINDOW", on_closing)

# Coluna da esquerda (menu)
left_frame = tk.Frame(window, bg="#003366", width=200)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Nome do usuário
user_label = tk.Label(left_frame, text="Lucas Almeida", font=("Arial", 14), bg="#003366", fg="white")
user_label.pack(pady=20)

# Coluna da direita (conteúdo)
right_frame = tk.Frame(window, bg="white")
right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Título do conteúdo
content_title = tk.Label(right_frame, text="Dashboard", font=("Arial", 18), bg="white", fg="#003366")
content_title.pack(pady=20)

# Área de log com scrollbar (renderizada por último)
log_frame = tk.Frame(window, bg="white")
log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, pady=10, padx=10)

log_text = tk.Text(log_frame, height=15, wrap=tk.WORD, font=("Arial", 10), bg="#e0e0e0", state=tk.DISABLED)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

log_scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=log_scrollbar.set)

# Configurar o logger com o widget de texto do Tkinter
logger = setup_logger(log_text_widget=log_text)

# Função para limpar o conteúdo da coluna da direita
def clear_content(hide_log=False):
    for widget in right_frame.winfo_children():
        if widget != content_title:
            widget.destroy()
    if hide_log:
        log_frame.pack_forget()  # Oculta o log_frame
    else:
        log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, pady=10, padx=10)  # Mostra o log_frame

# Função para carregar o Dashboard inicialmente
def load_dashboard():
    clear_content(hide_log=True)  # Oculta o log_frame no Dashboard
    show_dashboard(right_frame, content_title)

# Função para adicionar uma thread à lista de threads ativas
def add_thread(thread):
    active_threads.append(thread)

# Menu de navegação
menu_items = [
    ("Dashboard", lambda: load_dashboard()),
    ("Manage Links", lambda: [clear_content(hide_log=True), manage_links_ui(right_frame, content_title)]),
    ("Visit", lambda: [clear_content(hide_log=False), show_visit(right_frame, content_title, window, log_text, add_thread)]),
    ("Connect", lambda: [clear_content(hide_log=False), show_connect(right_frame, content_title, window, log_text, add_thread)]),
    ("Messages", lambda: [clear_content(hide_log=True), show_messages(right_frame, content_title, window, log_text, add_thread)]),
]

for item, command in menu_items:
    button = tk.Button(left_frame, text=item, font=("Arial", 12), bg="#0066cc", fg="white", bd=0,
                       command=command, width=20, anchor="w")
    button.pack(pady=5, padx=10)

# Carregar o Dashboard inicialmente
load_dashboard()

# Iniciar interface gráfica
window.mainloop()