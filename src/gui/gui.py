import tkinter as tk
from tkinter import ttk
from src.utils.task_manager import TaskManager  # Importa a classe TaskManager
from .colors import DARK_BLUE, BLUE, BACKGROUND_LOG, WHITE
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

# Área de log com scrollbar
log_frame = tk.Frame(window, bg=WHITE)
log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, pady=10, padx=10)

log_text = tk.Text(log_frame, height=15, wrap=tk.WORD, font=("Arial", 10), bg=BACKGROUND_LOG, state=tk.DISABLED)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

log_scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=log_scrollbar.set)

# Configurar o logger com o widget de texto do Tkinter
logger = setup_logger(log_text_widget=log_text)

# Criar o gerenciador de tarefas
task_manager = TaskManager(log_text, window)

# Vincular a função ao evento de fechamento da janela
window.protocol("WM_DELETE_WINDOW", task_manager.on_closing)

# Coluna da esquerda (menu)
left_frame = tk.Frame(window, bg=DARK_BLUE, width=200)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Nome do usuário
user_label = tk.Label(left_frame, text="Lucas Almeida", font=("Arial", 14), bg=DARK_BLUE, fg=WHITE)
user_label.pack(pady=20)

# Coluna da direita (conteúdo)
right_frame = tk.Frame(window, bg=WHITE)
right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Título do conteúdo
content_title = tk.Label(right_frame, text="Dashboard", font=("Arial", 18), bg=WHITE, fg=DARK_BLUE)
content_title.pack(pady=20)

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
    show_dashboard(right_frame, content_title, task_manager)

# Menu de navegação
menu_items = [
    ("Dashboard", lambda: load_dashboard()),
    ("Manage Links", lambda: [clear_content(hide_log=True), manage_links_ui(right_frame, content_title)]),
    ("Connect", lambda: [clear_content(hide_log=False), show_connect(right_frame, content_title, task_manager)]),
    ("Visit", lambda: [clear_content(hide_log=False), show_visit(right_frame, content_title, task_manager)]),
    ("Messages", lambda: [clear_content(hide_log=True), show_messages(right_frame, content_title, task_manager)]),
]

for item, command in menu_items:
    button = tk.Button(left_frame, text=item, font=("Arial", 12), bg=BLUE, fg=WHITE, bd=0,
                       command=command, width=20, anchor="w")
    button.pack(pady=5, padx=10)

# Carregar o Dashboard inicialmente
load_dashboard()

# Iniciar interface gráfica
window.mainloop()