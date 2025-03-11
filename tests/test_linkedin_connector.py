import sys
import os

# Adiciona o diretório src ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.main import test  # Agora a importação deve funcionar

import unittest

class TestMain(unittest.TestCase):
    def test_main(self):
        """Testa a função main."""
        test(number_profiles=5, process='connect')  # Chama a função test

if __name__ == "__main__":
    unittest.main()
