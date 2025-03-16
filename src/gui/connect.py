import tkinter as tk
from tkinter import messagebox
import logging
import threading
import queue
from .colors import DARK_BLUE, WHITE, BLUE
from src.main import run_connect  # Importa a função run_connect

logger = logging.getLogger("LinkedInAutomation")

def show_connect(right_frame, content_title, window, log_text, add_thread):
    """Cria a interface de conexão no LinkedIn dentro do right_frame."""

    # Atualiza o título da aba
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

    # Função para iniciar a conexão
    def start_connect():
        num_profiles = connect_entry.get().strip()
        if not num_profiles.isdigit():
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        # Desabilita o botão de conexão enquanto a tarefa está em execução
        connect_button.config(state=tk.DISABLED)

        # Função para reabilitar o botão após a execução (sucesso ou erro)
        def reenable_button():
            connect_button.config(state=tk.NORMAL)

        # Função para executar a tarefa em uma thread
        def run_connect_task():
            try:
                run_connect(int(num_profiles), logger, log_queue)
            except Exception as e:
                logger.error(f"Error during connection: {e}")
                log_queue.put(f"Error during connection: {e}")
            finally:
                # Reabilita o botão após a execução (sucesso ou erro)
                window.after(0, reenable_button)

        # Cria e inicia a thread
        thread = threading.Thread(
            target=run_connect_task,
            daemon=True
        )
        thread.start()
        add_thread(thread)  # Registra a thread

        # Verifica a queue periodicamente para atualizar a interface
        check_queue()

    # Botão de conexão
    connect_button = tk.Button(right_frame, text="Connect", font=("Arial", 12), bg=BLUE, fg="white",
                               command=start_connect, relief="raised", width=20)
    connect_button.pack(pady=10)