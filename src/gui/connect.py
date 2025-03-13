import tkinter as tk
from tkinter import messagebox
import logging
from .colors import DARK_BLUE, WHITE, BLUE
from src.main import start_process  # Importa a função start_process

logger = logging.getLogger("LinkedInAutomation")

def show_connect(right_frame, content_title):
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

    # Campo de entrada para número de perfis
    # connect_label = tk.Label(right_frame, text="Number of Profiles:", font=("Arial", 12), bg=WHITE)
    # connect_label.pack(pady=5)

    # Placeholder funcional
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

    # Função para iniciar a conexão
    def start_connect():
        num_profiles = connect_entry.get().strip()
        if not num_profiles.isdigit():
            messagebox.showerror("Error", "Please enter a valid number.")
            return
        logger.info(f"Starting connection with {num_profiles} profiles.")
        start_process(int(num_profiles), logger, process="connect")

    # Botão de conexão
    connect_button = tk.Button(right_frame, text="Connect", font=("Arial", 12), bg=BLUE, fg="white",
                               command=start_connect, relief="raised", width=20)
    connect_button.pack(pady=10)
