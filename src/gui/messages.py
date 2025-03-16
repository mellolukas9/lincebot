import tkinter as tk
from tkinter import ttk, messagebox
import logging
import threading
import queue
import os
from .colors import DARK_BLUE, BLUE
from src.config import config
from src.utils.library import read_json_file, remove_numbers_and_emojis
from src.main import run_send_messages

logger = logging.getLogger("LinkedInAutomation")

def show_messages(right_frame, content_title, window, log_text, add_thread):
    """Cria a interface de envio de mensagens no LinkedIn dentro do right_frame."""

    # Atualiza o título da aba
    content_title.config(text="Messages")

    # Título da tela de Messages
    messages_title = tk.Label(right_frame, text="Select Profiles to Message", font=("Arial", 16, "bold"), fg=DARK_BLUE, bg="white")
    messages_title.pack(pady=12)

    # Descrição com quebra de linha e centralização
    description = "Select profiles from the table below to send personalized messages."
    messages_description = tk.Label(
        right_frame, 
        text=description, 
        font=("Arial", 11), 
        bg="white", 
        wraplength=350, 
        justify="center"
    )
    messages_description.pack(pady=10)

    # Caminho para o arquivo de perfis visitados
    data_dir = config['data']['dir']
    visits_file_path = os.path.join(data_dir, "visited.json")
    profiles = read_json_file(visits_file_path)

    # Função para separar o nome completo em primeiro e último nome
    def split_name(full_name):
        parts = full_name.split()
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        last_name = remove_numbers_and_emojis(last_name)
        return first_name, last_name

    # Frame para a tabela de perfis
    table_frame = tk.Frame(right_frame, bg="white")
    table_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Colunas da tabela
    columns = ("Checked", "First Name", "Last Name", "Role")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")
    
    tree.heading("Checked", text="✔", command=lambda: toggle_all_selection())
    tree.heading("First Name", text="First Name")
    tree.heading("Last Name", text="Last Name")
    tree.heading("Role", text="Role")
    
    tree.column("Checked", width=50, anchor="center")
    tree.column("First Name", width=120, anchor="w")
    tree.column("Last Name", width=120, anchor="w")
    tree.column("Role", width=200, anchor="w")

    tree.pack(fill="both", expand=True)

    # Dicionário para armazenar os JSONs dos perfis, associados ao item_id da Treeview
    profile_data = {}

    # Variáveis para os checkboxes
    checkbox_vars = {}
    select_all = tk.BooleanVar(value=False)  # Controle global para selecionar/deselecionar tudo

    # Preenche a tabela com os perfis
    for profile in profiles:
        first_name, last_name = split_name(profile["name"])
        role = '' if profile["current_role"] is None else profile["current_role"].split('|')[0]

        var = tk.BooleanVar(value=False)
        checkbox_vars[first_name] = var

        # Insere a linha na Treeview e armazena o JSON correspondente
        item_id = tree.insert("", "end", values=("", first_name, last_name, role))
        profile_data[item_id] = profile  # Associa o item_id ao JSON do perfil

    # Função para alternar a seleção de um perfil
    def toggle_selection(event):
        """Ativa ou desativa os checkboxes ao clicar na linha."""
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            if values:
                first_name = values[1]
                checkbox_vars[first_name].set(not checkbox_vars[first_name].get())
                tree.set(selected_item, column="Checked", value="✔" if checkbox_vars[first_name].get() else "")

    # Função para selecionar/deselecionar todos os perfis
    def toggle_all_selection():
        """Seleciona ou desseleciona todos os checkboxes ao clicar no cabeçalho da coluna 'Checked'."""
        new_state = not select_all.get()
        select_all.set(new_state)
        
        for item in tree.get_children():
            values = tree.item(item, "values")
            first_name = values[1]
            checkbox_vars[first_name].set(new_state)
            tree.set(item, column="Checked", value="✔" if new_state else "")

    # Vincula o evento de clique à função de seleção
    tree.bind("<ButtonRelease-1>", toggle_selection)

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

    # Função para enviar mensagens aos perfis selecionados
    def send_message_to_selected():
        selected_profiles = []
        for item in tree.get_children():
            values = tree.item(item, "values")
            first_name = values[1]
            if checkbox_vars[first_name].get():
                # Recupera o JSON do perfil associado ao item_id
                profile_json = profile_data[item]
                selected_profiles.append(profile_json)  # Adiciona o JSON à lista de selecionados

        if not selected_profiles:
            messagebox.showerror("Error", "No profiles selected.")
            return

        # Desabilita o botão de envio enquanto a tarefa está em execução
        send_button.config(state=tk.DISABLED)

        # Função para reabilitar o botão após a execução (sucesso ou erro)
        def reenable_button():
            send_button.config(state=tk.NORMAL)

        # Função para executar a tarefa em uma thread
        def run_send_messages_task():
            try:
                run_send_messages(selected_profiles, logger, log_queue)
            except Exception as e:
                logger.error(f"Error during message sending: {e}")
                log_queue.put(f"Error during message sending: {e}")
            finally:
                # Reabilita o botão após a execução (sucesso ou erro)
                window.after(0, reenable_button)

        # Cria e inicia a thread
        thread = threading.Thread(
            target=run_send_messages_task,
            daemon=True
        )
        thread.start()
        add_thread(thread)  # Registra a thread

        # Verifica a queue periodicamente para atualizar a interface
        check_queue()

    # Botão para enviar mensagens
    send_button = tk.Button(right_frame, text="Send Message to Selected", font=("Arial", 12), bg=BLUE, fg="white",
                            command=send_message_to_selected, relief="raised", width=25)
    send_button.pack(pady=10)