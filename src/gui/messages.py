import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os
from .colors import DARK_BLUE, BLUE
from src.config import config
from src.utils.library import read_json_file, remove_numbers_and_emojis
from src.main import run_send_messages

logger = logging.getLogger("LinkedInAutomation")

def show_messages(right_frame, content_title):
    """Cria a interface de envio de mensagens no LinkedIn dentro do right_frame."""

    content_title.config(text="Messages")

    messages_title = tk.Label(right_frame, text="Select Profiles to Message", font=("Arial", 16, "bold"), fg=DARK_BLUE, bg="white")
    messages_title.pack(pady=12)

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

    data_dir = config['data']['dir']

    # Ler os dados de visitas
    visits_file_path = os.path.join(data_dir, "visited.json")
    profiles = read_json_file(visits_file_path)

    def split_name(full_name):
        parts = full_name.split()
        first_name = parts[0]
        last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        last_name = remove_numbers_and_emojis(last_name)
        return first_name, last_name

    table_frame = tk.Frame(right_frame, bg="white")
    table_frame.pack(pady=10, padx=10, fill="both", expand=True)

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

    checkbox_vars = {}
    select_all = tk.BooleanVar(value=False)  # Controle global para selecionar/deselecionar tudo

    for profile in profiles:
        first_name, last_name = split_name(profile["name"])
        role = '' if profile["current_role"] is None else profile["current_role"].split('|')[0]

        var = tk.BooleanVar(value=False)
        checkbox_vars[first_name] = var

        # Insere a linha na Treeview e armazena o JSON correspondente
        item_id = tree.insert("", "end", values=("", first_name, last_name, role))
        profile_data[item_id] = profile  # Associa o item_id ao JSON do perfil

    def toggle_selection(event):
        """Ativa ou desativa os checkboxes ao clicar na linha."""
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            if values:
                first_name = values[1]
                checkbox_vars[first_name].set(not checkbox_vars[first_name].get())
                tree.set(selected_item, column="Checked", value="✔" if checkbox_vars[first_name].get() else "")

    def toggle_all_selection():
        """Seleciona ou desseleciona todos os checkboxes ao clicar no cabeçalho da coluna 'Checked'."""
        new_state = not select_all.get()
        select_all.set(new_state)
        
        for item in tree.get_children():
            values = tree.item(item, "values")
            first_name = values[1]
            checkbox_vars[first_name].set(new_state)
            tree.set(item, column="Checked", value="✔" if new_state else "")

    tree.bind("<ButtonRelease-1>", toggle_selection)

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

        # Exibe os JSONs dos perfis selecionados (para teste)
        # for profile in selected_profiles:
        #     logger.info(f"Selected profile: {profile}")

        messagebox.showinfo("Success", f"Messages sent to {len(selected_profiles)} profiles!")
        run_send_messages(selected_profiles, logger)

    send_button = tk.Button(right_frame, text="Send Message to Selected", font=("Arial", 12), bg=BLUE, fg="white",
                            command=send_message_to_selected, relief="raised", width=25)
    send_button.pack(pady=10)