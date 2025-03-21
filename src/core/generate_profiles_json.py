import os
import json
import google.generativeai as genai
from src.config import config  # Importa as configurações

def generate_profiles_json(data):

    prompt = """
    Por favor, analise a seguinte lista de dados de perfis e converta cada perfil em um objeto JSON no seguinte formato:

    {
    "name": "Nome Completo",
    "profile_level": "Nível de Conexão (apenas o número)",
    "location": "Localização",
    "skills": ["Habilidade 1", "Habilidade 2", ...],
    "current_role": "Função Atual (pode ser null)",
    "common_connections": ["Conexão 1", "Conexão 2", ...]
    "profile_link": "https://www.linkedin.com/in/name123/"
    "timestamp": "2025-03-13 14:00:00"
    }

    Aqui está a lista de dados dos perfis:

    [LISTA_DE_DADOS]

    Observações:

    * O "Nível de Conexão" deve conter apenas o número do grau de conexão (por exemplo, "2").
    * As "Habilidades" devem ser listadas em um array de strings.
    * As "Conexões em comum" também devem ser listadas em um array de strings, incluindo a frase "e mais X conexões em comum" quando presente.
    * Se a "Função Atual" estiver ausente, use o valor `null`.
    * Mantenha a formatação exata das informações, incluindo a frase "e mais X conexões em comum".
    * Retorne um unico json contendo a lista de todos os objetos json criados.

    Retorne apenas a lista de objetos JSON, sem comentários.
    """

    # dados_perfis = [
    #     "Erik Andrade\nVer perfil de Erik Andrade\n \n• 2º\nConexão de 2º grau\nRpa | Automation Anywhere | Metodologia Ágil | Sql Server | AzureDevops | .net | Certificação | Git | Python | UiPath\nSão Paulo, SP\n\nAtual: Desenvolvedor RPA na Grupo FCamara\n\nErimateia Lima, Morganna Giovanelli e mais 3 conexões em comum",
    #     # Adicione os outros 39 perfis aqui
    # ]

    prompt = prompt.replace("[LISTA_DE_DADOS]", str(data))

    # Envie o prompt para a API do Gemini e obtenha a resposta (resposta_da_api)
    # Configure a API com sua chave de API
    google_api_key = os.getenv("GEMINI_API_KEY")  # Pega a variável do ambiente
    genai.configure(api_key=google_api_key)

    # Crie uma instância do modelo Gemini
    ai_version = config['ai']['gemini']
    model = genai.GenerativeModel(ai_version)

    # Gere o conteúdo
    response = model.generate_content(prompt)
    json_string = response.text
    # json_string = json_string.strip('```json\n')
    json_string = json_string.replace("```json\n", "").replace("```", "").strip()

    profile_json = json.loads(json_string)

    return profile_json
