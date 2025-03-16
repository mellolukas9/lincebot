import logging
from logging.handlers import RotatingFileHandler
import tkinter as tk

def setup_logger(log_text_widget=None):
    """
    Configura o logger para o projeto LinkedInAutomation.

    :param log_text_widget: Widget de texto do Tkinter para exibir logs na interface gráfica.
    :return: Logger configurado.
    """
    logger = logging.getLogger("LinkedInAutomation")

    # Verifica se o logger já foi configurado
    if logger.hasHandlers():
        logger.handlers.clear()  # Remove handlers existentes

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Handler para o console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # Handler para arquivo (com rotação)
    file_handler = RotatingFileHandler(
        "linkedin_automation.log",
        maxBytes=1048576,  # 1 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Handler para a interface gráfica (se fornecido)
    if log_text_widget:
        class TkinterHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget

            def emit(self, record):
                log_message = self.format(record)
                self.text_widget.config(state=tk.NORMAL)
                self.text_widget.insert(tk.END, log_message + "\n")
                self.text_widget.config(state=tk.DISABLED)
                self.text_widget.yview(tk.END)
                self.text_widget.update_idletasks()

        tkinter_handler = TkinterHandler(log_text_widget)
        tkinter_handler.setFormatter(formatter)
        tkinter_handler.setLevel(logging.INFO)
        logger.addHandler(tkinter_handler)

    return logger