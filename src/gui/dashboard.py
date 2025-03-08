import tkinter as tk

def show_dashboard(right_frame, content_title, content_label):
    content_title.config(text="Dashboard")
    content_label.config(text="Dashboard Content")

    # Adicione outros widgets específicos do Dashboard aqui
    welcome_label = tk.Label(right_frame, text="Bem-vindo ao Dashboard!", font=("Arial", 12), bg="#ffffff")
    welcome_label.pack(pady=10)

    stats_label = tk.Label(right_frame, text="Estatísticas:", font=("Arial", 12), bg="#ffffff")
    stats_label.pack(pady=5)

    # Exemplo de widget adicional (um botão)
    def refresh_stats():
        stats_label.config(text="Estatísticas atualizadas!")

    refresh_button = tk.Button(right_frame, text="Atualizar Estatísticas", font=("Arial", 12), bg="#0e76a8", fg="white",
                               command=refresh_stats, relief="raised", width=20)
    refresh_button.pack(pady=10)