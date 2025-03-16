import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from .colors import DARK_BLUE, BLUE
from src.config import config

# Caminho do arquivo JSON para armazenar os links
data_path = config['data']['dir']
links_file_path = os.path.join(data_path, "links.json")

# Função para carregar os links salvos
def load_links():
    if os.path.exists(links_file_path):
        with open(links_file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Função para salvar os links
def save_links(links):
    with open(links_file_path, "w", encoding="utf-8") as file:
        json.dump(links, file, indent=4)

def manage_links_ui(right_frame, content_title):
    """Cria a interface para gerenciar links."""
    content_title.config(text="Manage Links")

    links_title = tk.Label(right_frame, text="Manage Links", font=("Arial", 16, "bold"), fg=DARK_BLUE, bg="white")
    links_title.pack(pady=12)

    description = "Add, view, and remove links to be used in other processes."
    links_description = tk.Label(
        right_frame,
        text=description,
        font=("Arial", 11),
        bg="white",
        wraplength=350,
        justify="center"
    )
    links_description.pack(pady=10)

    table_frame = tk.Frame(right_frame, bg="white")
    table_frame.pack(pady=10, padx=10, fill="both", expand=True)

    columns = ("Name", "Link")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
    
    tree.heading("Name", text="Name")
    tree.heading("Link", text="Link")
    
    tree.column("Name", width=150, anchor="w")
    tree.column("Link", width=300, anchor="w")
    
    tree.pack(fill="both", expand=True)

    # Carregar links salvos
    links = load_links()
    for link in links:
        tree.insert("", "end", values=(link["name"], link["link"]))
    
    def add_link():
        """Adiciona um novo link."""
        name = name_entry.get().strip()
        link = link_entry.get().strip()
        
        if not name or not link:
            messagebox.showerror("Error", "All fields must be filled!")
            return
        
        links.append({"name": name, "link": link})
        save_links(links)
        tree.insert("", "end", values=(name, link))
        
        name_entry.delete(0, tk.END)
        link_entry.delete(0, tk.END)
        
    def remove_link():
        """Remove o link selecionado."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No link selected!")
            return
        
        values = tree.item(selected_item, "values")
        for link in links:
            if link["name"] == values[0] and link["link"] == values[1]:
                links.remove(link)
                break
        
        save_links(links)
        tree.delete(selected_item)
        
    form_frame = tk.Frame(right_frame, bg="white")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Name:", bg="white").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(form_frame, width=41)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Link:", bg="white").grid(row=1, column=0, sticky="w")
    link_entry = tk.Entry(form_frame, width=41)
    link_entry.grid(row=1, column=1, padx=5, pady=5)

    button_frame = tk.Frame(right_frame, bg="white")
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="Add Link", font=("Arial", 12), bg=BLUE, fg="white", command=add_link, relief="raised", width=15)
    add_button.grid(row=0, column=0, padx=5)

    remove_button = tk.Button(button_frame, text="Remove Selected", font=("Arial", 12), bg="red", fg="white", command=remove_link, relief="raised", width=15)
    remove_button.grid(row=0, column=1, padx=5)