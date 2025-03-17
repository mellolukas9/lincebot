import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from src.config import config
from src.utils.library import read_json_file

def show_dashboard(right_frame, content_title):
    content_title.config(text="Dashboard")

    # Função para formatar o texto no gráfico de pizza
    def format_pct(pct, allvals):
        absolute = int(round(pct / 100. * sum(allvals)))
        return f"{pct:.1f}% ({absolute})"

    # Função para atualizar as estatísticas
    def refresh_stats():
        data_path = config['paths']['data']

        # Ler os dados de visitas
        visits_file_path = os.path.join(data_path, "visited.json")
        visits = len(read_json_file(visits_file_path))

        # Ler os dados de conexões
        connections_file_path = os.path.join(data_path, "connected.json")
        connections = len(read_json_file(connections_file_path))

        # Criar um DataFrame com os dados
        data = {
            'Type': ['Visits', 'Connections'],
            'Quantity': [visits, connections]
        }
        df = pd.DataFrame(data)

        # Criar o gráfico de pizza
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(df['Quantity'], labels=df['Type'], 
               autopct=lambda pct: format_pct(pct, df['Quantity']),  # Formatação personalizada
               startangle=90, colors=sns.color_palette('pastel'))
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Exibir o gráfico no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=right_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    # Atualizar as estatísticas ao carregar o dashboard
    refresh_stats()