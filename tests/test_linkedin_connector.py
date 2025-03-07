import unittest
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.utils.logger_config import logger  # Importando o logger configurado

from src.main import start_visit\

class TestMain(unittest.TestCase):
    def test_main(self):
        """Testa a função main e verifica se os logs aparecem."""

        start_visit(number_profiles=5, logger=logger)

if __name__ == "__main__":
    unittest.main()
