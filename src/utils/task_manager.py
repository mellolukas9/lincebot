import tkinter as tk
import threading
import queue
import logging

logger = logging.getLogger("LinkedInAutomation")

class TaskManager:
    def __init__(self, log_text_widget, window):
        """
        Inicializa o gerenciador de tarefas.

        :param log_text_widget: Widget de texto do Tkinter para exibir logs.
        :param window: Janela principal do Tkinter.
        """
        self.log_text_widget = log_text_widget
        self.window = window
        self.log_queue = queue.Queue()
        self.active_threads = []

    def run_task(self, task, *args, button=None):
        """
        Executa uma tarefa em uma thread separada.

        :param task: Função que será executada.
        :param args: Argumentos para a função task.
        :param button: Botão que será reabilitado após a execução da tarefa.
        """
        # Função para reabilitar o botão após a execução (sucesso ou erro)
        def reenable_button(button):
            if button and self.window.winfo_exists():  # Verifica se a janela ainda existe
                logger.info("Reenabling button...")
                button.config(state=tk.NORMAL)

        # Função para executar a tarefa em uma thread
        def run_task_in_thread(button):
            try:
                task(*args)
            except Exception as e:
                logger.error(f"Error during task execution: {e}")
                self.log_queue.put(f"Error during task execution: {e}")
            finally:
                # Reabilita o botão após a execução (sucesso ou erro)
                if button:
                    self.window.after(0, reenable_button, button)

        # Cria e inicia a thread
        thread = threading.Thread(
            target=run_task_in_thread,
            args=(button,),  # Passa o botão como argumento
            daemon=True  # Define a thread como daemon
        )
        thread.start()
        self.active_threads.append(thread)

    def check_queue(self):
        """
        Verifica a queue e atualiza o widget de texto com as mensagens de log.
        """
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text_widget.config(state=tk.NORMAL)
                self.log_text_widget.insert(tk.END, message + "\n")
                self.log_text_widget.config(state=tk.DISABLED)
                self.log_text_widget.yview(tk.END)
        except queue.Empty:
            pass

        # Verifica a queue novamente após 100ms
        self.window.after(100, self.check_queue)

    def on_closing(self):
        """
        Função chamada ao fechar a janela. Encerra todas as threads ativas.
        """
        logger.info("Closing application and terminating threads...")

        # Lista todas as threads ativas
        for thread in threading.enumerate():
            logger.info(f"Active thread: {thread.name} (daemon={thread.daemon})")

        # Finaliza as threads do TaskManager
        for thread in self.active_threads:
            if thread.is_alive():
                logger.info(f"Terminating thread: {thread.name}")
                thread.join(timeout=1)  # Aguarda a finalização da thread por 1 segundo
                if thread.is_alive():
                    logger.warning(f"Thread {thread.name} did not finish gracefully.")

        logger.info("All threads terminated. Closing window...")
        self.window.quit()  # Finaliza o loop de eventos do Tkinter
        self.window.destroy()  # Fecha a janela