import tkinter as tk
from tkinter import messagebox
import logging
import threading
import queue
from .colors import DARK_BLUE, WHITE, BLUE
from src.main import run_visit  # Importa a função run_visit

logger = logging.getLogger("LinkedInAutomation")

def show_visit(right_frame, content_title, window, log_text, add_thread):
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

    # Queue para comunicação entre threads
    log_queue = queue.Queue()

    # Função para verificar a queue e atualizar a interface
    def check_queue():
        try:
            while True:
                message = log_queue.get_nowait()
                log_text.config(state=tk.NORMAL)
                log_text.insert(tk.END, message + "\n")
                log_text.config(state=tk.DISABLED)
                log_text.yview(tk.END)
        except queue.Empty:
            pass

        # Verifica a queue novamente após 100ms
        window.after(100, check_queue)

    # Função para iniciar a visita
    def start_visit():
        num_profiles = visit_entry.get().strip()
        if not num_profiles.isdigit():
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        # Desabilita o botão de visita enquanto a tarefa está em execução
        visit_button.config(state=tk.DISABLED)

        # Função para reabilitar o botão após a execução (sucesso ou erro)
        def reenable_button():
            visit_button.config(state=tk.NORMAL)

        # Função para executar a tarefa em uma thread
        def run_visit_task():
            try:
                run_visit(int(num_profiles), logger, log_queue)
            except Exception as e:
                logger.error(f"Error during visit: {e}")
                log_queue.put(f"Error during visit: {e}")
            finally:
                # Reabilita o botão após a execução (sucesso ou erro)
                window.after(0, reenable_button)

        # Cria e inicia a thread
        thread = threading.Thread(
            target=run_visit_task,
            daemon=True
        )
        thread.start()
        add_thread(thread)  # Registra a thread

        # Verifica a queue periodicamente para atualizar a interface
        check_queue()

    # Botão de visita
    visit_button = tk.Button(right_frame, text="Visit", font=("Arial", 12), bg=BLUE, fg="white",
                             command=start_visit, relief="raised", width=20)
    visit_button.pack(pady=10)