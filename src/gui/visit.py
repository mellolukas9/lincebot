import tkinter as tk
from tkinter import messagebox
import logging
from .colors import DARK_BLUE, WHITE, BLUE
from src.main import start_process  # Importa a função start_visit

logger = logging.getLogger("LinkedInAutomation")

# def show_visit(right_frame, content_title, content_label=None):
def show_visit(right_frame, content_title):
    content_title.config(text="Visit")
    # content_label.config(text="Visit Content")

    # # Título da tela de Connect
    visit_title = tk.Label(right_frame, text="Visit to Profiles", font=("Arial", 16, "bold"), fg=DARK_BLUE, bg=WHITE)
    visit_title.pack(pady=12)

    description = "Boost your visibility by visiting LinkedIn profiles! Engage with professionals, increase your exposure, and attract new connections effortlessly."

    visit_description = tk.Label(
        right_frame, 
        text=description, 
        font=("Arial", 11), 
        bg=WHITE,
        wraplength=350,  # Define a largura máxima antes de quebrar a linha
        justify="center"  # Centraliza o texto
    )
    visit_description.pack(pady=10)

    # Campo de entrada para número de perfis
    # visit_label = tk.Label(right_frame, text="Number of Profiles:", font=("Arial", 12), bg=WHITE)
    # visit_label.pack(pady=5)

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

    # Botão para iniciar a conexão
    def start_visit():
        num_profiles = visit_entry.get()
        if not num_profiles.isdigit():
            messagebox.showerror("Erro", "Por favor, insira um número válido.")
            return
        logger.info(f"Starting visit to {num_profiles} profiles.")
        start_process(int(num_profiles), logger, process="visit")  # Chama a função start_visit

    connect_button = tk.Button(right_frame, text="Visit", font=("Arial", 12), bg=BLUE, fg="white",
                               command=start_visit, relief="raised", width=20)
    connect_button.pack(pady=10)