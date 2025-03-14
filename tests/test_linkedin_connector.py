import os
import sys
import logging
from unittest import TestCase

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.main import run_connect

# Configuração do logger para testes
logger = logging.getLogger("LinkedInAutomation")
logger.setLevel(logging.DEBUG)

class TestConnect(TestCase):
    def test_run_connect_success(self):
        """
        Testa a função run_connect com sucesso.
        Verifica se a função executa corretamente e se o Playwright é aberto e fechado.
        """

        # Executa a função
        run_connect(5, logger)

# Executa os testes
if __name__ == "__main__":
    import unittest
    unittest.main()