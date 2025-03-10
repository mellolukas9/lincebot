import tkinter as tk
from tkinter import messagebox
import logging
from .colors import DARK_BLUE, WHITE, BLUE
from src.main import start_process  # Importa a função start_visit

logger = logging.getLogger("LinkedInAutomation")

def show_visit(right_frame, content_title, content_label=None):
    content_title.config(text="Visit")
    content_label.config(text="Visit Content")

    # # Título da tela de Connect
    visit_title = tk.Label(right_frame, text="Visit to Profiles", font=("Arial", 16, "bold"), fg=DARK_BLUE, bg=WHITE)
    visit_title.pack(pady=20)

    # Campo de entrada para número de perfis
    visit_label = tk.Label(right_frame, text="Number of Profiles to Visit:", font=("Arial", 12), bg=WHITE)
    visit_label.pack(pady=5)

    visit_entry = tk.Entry(right_frame, font=("Arial", 12), bd=2, relief="groove")
    visit_entry.pack(pady=5)

    # Botão para iniciar a conexão
    def start_visit():
        num_profiles = visit_entry.get()
        if not num_profiles.isdigit():
            messagebox.showerror("Erro", "Por favor, insira um número válido.")
            return
        logger.info(f"Iniciando conexão para {num_profiles} perfis.")
        start_process(int(num_profiles), logger, process="visit")  # Chama a função start_visit

    connect_button = tk.Button(right_frame, text="Start Visit", font=("Arial", 12), bg=BLUE, fg="white",
                               command=start_visit, relief="raised", width=20)
    connect_button.pack(pady=10)