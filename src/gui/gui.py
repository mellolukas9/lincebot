import tkinter as tk
import logging
from .colors import BACKGROUND_COLOR_LIGHT, DARK_BLUE, WHITE, MEDIUM_BLUE, BACKGROUND_LOG
from .dashboard import show_dashboard
from .connect import show_connect      # Importa a função do Connect
# from message import show_message      # Importa a função do Message

# Configuração da janela principal
window = tk.Tk()
window.title("LinceBot Automation")
window.geometry("800x600")
window.config(bg=BACKGROUND_COLOR_LIGHT)

# Coluna da esquerda (menu)
left_frame = tk.Frame(window, bg=DARK_BLUE, width=200)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

# Nome do usuário
user_label = tk.Label(left_frame, text="Lucas Almeida", font=("Arial", 14), bg=DARK_BLUE, fg="white")
user_label.pack(pady=20)

# Coluna da direita (conteúdo)
right_frame = tk.Frame(window, bg=WHITE)
right_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Título do conteúdo
content_title = tk.Label(right_frame, text="Dashboard", font=("Arial", 18), bg=WHITE, fg=DARK_BLUE)
content_title.pack(pady=20)

# Conteúdo dinâmico
content_label = tk.Label(right_frame, text="Dashboard Content", font=("Arial", 14), bg=WHITE, fg=MEDIUM_BLUE)
content_label.pack(pady=20)

# Função para limpar o conteúdo da coluna da direita
def clear_content():
    for widget in right_frame.winfo_children():
        if widget not in (content_title, content_label):
        # if widget not in (content_title):
            widget.destroy()

# Função para carregar o Dashboard inicialmente
def load_dashboard():
    clear_content()
    show_dashboard(right_frame, content_title, content_label)

# Menu de navegação
menu_items = [
    ("Dashboard", lambda: load_dashboard()),
    ("Connect", lambda: [clear_content(), show_connect(right_frame, content_title, content_label)]),
    # ("Message", lambda: [clear_content(), show_message(right_frame, content_title, content_label)]),
]

for item, command in menu_items:
    button = tk.Button(left_frame, text=item, font=("Arial", 12), bg=MEDIUM_BLUE, fg="white", bd=0,
                       command=command, width=20, anchor="w")
    button.pack(pady=5, padx=10)

# Área de log com scrollbar (renderizada por último)
log_frame = tk.Frame(window, bg=WHITE)
log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False, pady=10, padx=10)

log_text = tk.Text(log_frame, height=15, wrap=tk.WORD, font=("Arial", 10), bg=BACKGROUND_LOG, state=tk.DISABLED)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

log_scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
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

# Carregar o Dashboard inicialmente
load_dashboard()

# Iniciar interface gráfica
window.mainloop()