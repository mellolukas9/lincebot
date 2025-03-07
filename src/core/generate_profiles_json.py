import os
import json
from datetime import datetime
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

    Retorne a lista de objetos JSON.
    """

    # dados_perfis = [
    #     "Erik Andrade\nVer perfil de Erik Andrade\n \n• 2º\nConexão de 2º grau\nRpa | Automation Anywhere | Metodologia Ágil | Sql Server | AzureDevops | .net | Certificação | Git | Python | UiPath\nSão Paulo, SP\n\nAtual: Desenvolvedor RPA na Grupo FCamara\n\nErimateia Lima, Morganna Giovanelli e mais 3 conexões em comum",
    #     # Adicione os outros 39 perfis aqui
    # ]

    prompt = prompt.replace("[LISTA_DE_DADOS]", str(data))

    # Envie o prompt para a API do Gemini e obtenha a resposta (resposta_da_api)
    # Configure a API com sua chave de API
    gemini_api_key = os.getenv("GEMINI_API_KEY")  # Pega a variável do ambiente
    genai.configure(api_key=gemini_api_key)

    # Crie uma instância do modelo Gemini
    model = genai.GenerativeModel('models/gemini-2.0-flash')

    # Gere o conteúdo
    response = model.generate_content(prompt)
    json_string = response.text
    json_string = json_string.strip('```json\n')
    # print(json_string)

    profile_json = json.loads(json_string)

    # Obtém a data atual
    current_date = datetime.now()

    # Formata a data no formato 'ddmmyyyy'
    formatted_date = current_date.strftime("%d%m%Y")

    # Salvando novamente o JSON no arquivo
    with open(f'{config['data']['dir']}profile_json_{formatted_date}.json', 'w') as file:
        json.dump(profile_json, file, indent=4)  # Usando indent para uma formatação legível

    # Agora, resposta_json contém a lista de objetos JSON
    # print(json_response)

    return profile_json
