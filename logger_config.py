# logger_config.py
import logging

# Criando e configurando o logger
logger = logging.getLogger("LinkedInAutomation")
logger.setLevel(logging.DEBUG)

# Configuração do formato de log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Adicionando um handler para imprimir os logs no console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Adicionando um handler para gravar os logs em um arquivo
file_handler = logging.FileHandler("linkedin_automation.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Agora, o logger está configurado e pode ser importado em outros arquivos
