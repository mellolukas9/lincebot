import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from .colors import BLUE, WHITE
from src.config import config
from src.main import run_update_connections
from src.utils.logger_config import setup_logger
from src.utils.library import read_json_file

logger = setup_logger()

def show_dashboard(right_frame, content_title, task_manager):
    content_title.config(text="Dashboard")

    link = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'

    # Função para iniciar a atualização de conexções
    def update_connections():
        # Desabilita o botão de conexão enquanto a tarefa está em execução
        update_connections_button.config(state=tk.DISABLED)

        # Obtém a fila de logs do TaskManager
        log_queue = task_manager.log_queue

        # Executa a tarefa usando o TaskManager
        task_manager.run_task(run_update_connections, link, logger, log_queue, button=update_connections_button)

    # Botão de conexão
    update_connections_button = tk.Button(right_frame, text="Update Dashboard", font=("Arial", 12), bg=BLUE, fg=WHITE,
                               command=update_connections, relief="raised", width=20) 
    update_connections_button.pack(pady=10)

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

        # Ler os dados de número de pedido de conexão
        connected_file_path = os.path.join(data_path, "connected.json")
        connected = len(read_json_file(connected_file_path))

        # Ler os dados de conexões
        connections_file_path = os.path.join(data_path, "connections.json")
        connections = len(read_json_file(connections_file_path))

        # Criar um DataFrame com os dados
        data = {
            'Type': ['Visits', 'Request sent', "Connections"],
            'Quantity': [visits, connected, connections]
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