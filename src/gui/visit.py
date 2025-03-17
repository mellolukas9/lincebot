import tkinter as tk
from tkinter import ttk, messagebox
from .colors import DARK_BLUE, WHITE, BLUE
from src.utils.logger_config import setup_logger
from src.main import run_visit  # Importa a função run_visit
import json
import os
from src.config import config  # Importa a configuração para carregar os links

logger = setup_logger()

# Caminho do arquivo de links
data_path = config['paths']['data']
links_file_path = os.path.join(data_path, "links.json")

def load_links():
    """Carrega os links salvos."""
    if os.path.exists(links_file_path):
        with open(links_file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def show_visit(right_frame, content_title, task_manager):
    """Cria a interface de visita a perfis no LinkedIn dentro do right_frame."""

    # Atualiza o título da aba
    content_title.config(text="Visit")

    # Título da tela de Visit
    visit_title = tk.Label(right_frame, text="Visit to Profiles", font=("Arial", 16, "bold"), fg=DARK_BLUE, bg=WHITE)
    visit_title.pack(pady=12)

    # Descrição com quebra de linha e centralização
    description = "Boost your visibility by visiting LinkedIn profiles! Engage with professionals, increase your exposure, and attract new connections effortlessly."
    visit_description = tk.Label(
        right_frame, 
        text=description, 
        font=("Arial", 11), 
        bg=WHITE, 
        wraplength=350, 
        justify="center"
    )
    visit_description.pack(pady=10)

    # Carregar links salvos
    links = load_links()
    link_options = [link["name"] for link in links]

    # Dropdown para selecionar o link
    tk.Label(right_frame, text="Select Link:", font=("Arial", 12), bg=WHITE).pack(pady=5)
    link_var = tk.StringVar()
    link_dropdown = ttk.Combobox(right_frame, textvariable=link_var, values=link_options, state="readonly")
    link_dropdown.pack(pady=5)

    # Placeholder funcional
    placeholder_text = "Number of profiles..."
    
    def on_entry_click(event):
        """Remove o placeholder quando o usuário clica no campo."""
        if visit_entry.get() == placeholder_text:
            visit_entry.delete(0, "end")
            visit_entry.config(fg="black")

    def on_focus_out(event):
        """Restaura o placeholder se o campo estiver vazio."""
        if not visit_entry.get().strip():
            visit_entry.insert(0, placeholder_text)
            visit_entry.config(fg="gray")

    # Criando o campo de entrada
    visit_entry = tk.Entry(right_frame, font=("Arial", 12), bd=2, relief="groove", fg="gray")
    visit_entry.insert(0, placeholder_text)
    visit_entry.bind("<FocusIn>", on_entry_click)
    visit_entry.bind("<FocusOut>", on_focus_out)
    visit_entry.pack(pady=5)

    def start_visit():
        num_profiles = visit_entry.get().strip()
        selected_link_name = link_var.get()
        selected_link = next((link["link"] for link in links if link["name"] == selected_link_name), None)

        if not num_profiles.isdigit():
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        if not selected_link:
            messagebox.showerror("Error", "Please select a valid link.")
            return

        # Desabilita o botão de visita enquanto a tarefa está em execução
        visit_button.config(state=tk.DISABLED)

        # Obtém a fila de logs do TaskManager
        log_queue = task_manager.log_queue

        # Executa a tarefa usando o TaskManager
        task_manager.run_task(run_visit, int(num_profiles), selected_link, logger, log_queue, button=visit_button)

    # Botão de visita
    visit_button = tk.Button(right_frame, text="Visit", font=("Arial", 12), bg=BLUE, fg="white",
                             command=start_visit, relief="raised", width=20)
    visit_button.pack(pady=10)
