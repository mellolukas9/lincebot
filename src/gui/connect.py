import tkinter as tk
from tkinter import messagebox
import logging
from .colors import DARK_BLUE, WHITE, BLUE
from src.main import start_visit  # Importa a função start_visit

logger = logging.getLogger("LinkedInAutomation")

def show_connect(right_frame, content_title, content_label=None):
    content_title.config(text="Connect")
    content_label.config(text="Connect Content")

    # # Título da tela de Connect
    connect_title = tk.Label(right_frame, text="Connect to Profiles", font=("Arial", 16, "bold"), fg=DARK_BLUE, bg=WHITE)
    connect_title.pack(pady=20)

    # Campo de entrada para número de perfis
    connect_label = tk.Label(right_frame, text="Number of Profiles to Connect:", font=("Arial", 12), bg=WHITE)
    connect_label.pack(pady=5)

    connect_entry = tk.Entry(right_frame, font=("Arial", 12), bd=2, relief="groove")
    connect_entry.pack(pady=5)

    # Botão para iniciar a conexão
    def start_connect():
        num_profiles = connect_entry.get()
        if not num_profiles.isdigit():
            messagebox.showerror("Erro", "Por favor, insira um número válido.")
            return
        logger.info(f"Iniciando conexão para {num_profiles} perfis.")
        start_visit(int(num_profiles), logger)  # Chama a função start_visit

    connect_button = tk.Button(right_frame, text="Start Connect", font=("Arial", 12), bg=BLUE, fg="white",
                               command=start_connect, relief="raised", width=20)
    connect_button.pack(pady=10)