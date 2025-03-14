import os
import sys
import logging
from unittest import TestCase

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.main import run_send_messages

# Configuração do logger para testes
logger = logging.getLogger("LinkedInAutomation")
logger.setLevel(logging.DEBUG)

class TestConnect(TestCase):
    def test_run_send_messages_success(self):
        """
        Testa a função run_send_messages com sucesso.
        Verifica se a função executa corretamente e se o Playwright é aberto e fechado.
        """

        profiles = [
            {
                "name": "Julio Cesar",
                "profile_level": "1",
                "location": "Rio de Janeiro, RJ",
                "skills": ["Desenvolvedor UiPath"],
                "current_role": "Tech Lead",
                "common_connections": [],
                "profile_link": "https://www.linkedin.com/in/julio-cesar-s-m-junior-a94658b0/",
                "day_visited": "2025-03-13 14:00:00"
            },
        ]

        # Executa a função
        run_send_messages(profiles, logger)

# Executa os testes
if __name__ == "__main__":
    import unittest
    unittest.main()
