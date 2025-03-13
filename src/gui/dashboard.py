import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from .colors import WHITE, BLUE
from src.config import config
from src.utils.library import read_json_file

def show_dashboard(right_frame, content_title):
    content_title.config(text="Dashboard")

    # Adicione outros widgets específicos do Dashboard aqui
    # welcome_label = tk.Label(right_frame, text="Bem-vindo ao Dashboard!", font=("Arial", 12), bg=WHITE)
    # welcome_label.pack(pady=10)

    # stats_label = tk.Label(right_frame, text="Estatísticas:", font=("Arial", 12), bg=WHITE)
    # stats_label.pack(pady=5)

    # Exemplo de widget adicional (um botão)
    def refresh_stats():
        data_dir = config['data']['dir']

        visits_file_path = os.path.join(data_dir, "visited.json")
        visits = len(read_json_file(visits_file_path))

        connections_file_path = os.path.join(data_dir, "connected.json")
        connections = len(read_json_file(connections_file_path))

        data = {
            'Type': ['Visits', 'Connections'],
            'Quantity': [visits, connections]
        }
        df = pd.DataFrame(data)

        # Criando o gráfico de pizza
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(df['Quantity'], labels=df['Type'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Exibindo o gráfico no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        # stats_label.config(text="Estatísticas atualizadas!")

    # refresh_button = tk.Button(right_frame, text="Atualizar", font=("Arial", 12), bg=BLUE, fg="white",
    #                            command=refresh_stats, relief="raised", width=20)
    # refresh_button.pack(pady=10)

    # # Inicializa o gráfico com os dados iniciais
    refresh_stats()