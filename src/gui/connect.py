import tkinter as tk
from tkinter import ttk, messagebox
import logging
import json
import os
from .colors import DARK_BLUE, WHITE, BLUE
from src.main import run_connect  # Importa a função run_connect
from src.config import config

logger = logging.getLogger("LinkedInAutomation")

data_path = config['paths']['data']
links_file_path = os.path.join(data_path, "links.json")

def load_links():
    """Carrega os links salvos."""
    if os.path.exists(links_file_path):
        try:
            with open(links_file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            logger.error("Erro ao carregar links.json: Formato inválido.")
            return []
    return []

def show_connect(right_frame, content_title, task_manager):
    """Cria a interface de conexão no LinkedIn dentro do right_frame."""

    content_title.config(text="Connect")

    # Título da tela de conexão
    connect_title = tk.Label(right_frame, text="Connect to Profiles", font=("Arial", 16, "bold"), fg=DARK_BLUE, bg=WHITE)
    connect_title.pack(pady=12)

    # Descrição com quebra de linha e centralização
    description = "Expand your network effortlessly! Connect with new professionals and boost your LinkedIn presence."
    connect_description = tk.Label(
        right_frame, 
        text=description, 
        font=("Arial", 11), 
        bg=WHITE, 
        wraplength=350, 
        justify="center"
    )
    connect_description.pack(pady=10)

    # Carregar links salvos
    links = load_links()
    link_options = [link["name"] for link in links]

    # Variável para armazenar a seleção do usuário
    link_var = tk.StringVar(value="Select a link" if not link_options else link_options[0])

    # Dropdown para selecionar o link
    tk.Label(right_frame, text="Select Link:", font=("Arial", 12), bg=WHITE).pack(pady=5)
    link_dropdown = ttk.Combobox(right_frame, textvariable=link_var, values=link_options, state="readonly")
    link_dropdown.pack(pady=5)

    # Se houver links, seleciona o primeiro automaticamente
    if link_options:
        link_dropdown.current(0)

    # Campo de entrada para número de perfis
    placeholder_text = "Number of profiles..."
    
    def on_entry_click(event):
        """Remove o placeholder quando o usuário clica no campo."""
        if connect_entry.get() == placeholder_text:
            connect_entry.delete(0, "end")
            connect_entry.config(fg="black")

    def on_focus_out(event):
        """Restaura o placeholder se o campo estiver vazio."""
        if not connect_entry.get().strip():
            connect_entry.insert(0, placeholder_text)
            connect_entry.config(fg="gray")

    # Criando o campo de entrada
    connect_entry = tk.Entry(right_frame, font=("Arial", 12), bd=2, relief="groove", fg="gray")
    connect_entry.insert(0, placeholder_text)
    connect_entry.bind("<FocusIn>", on_entry_click)
    connect_entry.bind("<FocusOut>", on_focus_out)
    connect_entry.pack(pady=5)

    # Label de status para feedback
    status_label = tk.Label(right_frame, text="", font=("Arial", 10), bg=WHITE, fg="green")
    status_label.pack(pady=5)

    # Função para iniciar a conexão
    def start_connect():
        num_profiles = connect_entry.get().strip()
        selected_link_name = link_var.get()
        selected_link = next((link["link"] for link in links if link["name"] == selected_link_name), None)

        if not num_profiles.isdigit():
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        if not selected_link:
            messagebox.showerror("Error", "Please select a valid link.")
            return

        # Desabilita o botão de conexão enquanto a tarefa está em execução
        connect_button.config(state=tk.DISABLED)

        # Obtém a fila de logs do TaskManager
        log_queue = task_manager.log_queue

        # Executa a tarefa usando o TaskManager
        task_manager.run_task(run_connect, int(num_profiles), selected_link, logger, log_queue, button=connect_button)

    # Botão de conexão
    connect_button = tk.Button(right_frame, text="Connect", font=("Arial", 12), bg=BLUE, fg="white",
                               command=start_connect, relief="raised", width=20) 
    connect_button.pack(pady=10)
