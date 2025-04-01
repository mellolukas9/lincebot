import os
import google.generativeai as genai
from src.config import config  # Importa as configurações

def evaluate_profile_and_respond(name_to_profile, text):

    prompt = """
    Com base no meu perfil do LinkedIn e no perfil da pessoa com quem desejo me conectar, gere uma mensagem personalizada que destaque nossas similaridades e crie uma conexão genuína. A mensagem deve ser profissional, amigável e mostrar interesse em estabelecer uma relação profissional. Aqui estão os inputs:

    Meu Sobre:
    Olá! Sou Lucas Almeida, um entusiasta da automação e desenvolvimento RPA, com um foco especial em Python.

    Iniciei minha jornada como analista de sistemas, destacando-me no universo do ERP RM da Totvs. Essa experiência sólida abriu portas para uma transição natural para o papel de desenvolvedor UiPath.

    Conhecer profundamente do ERP RM foi um diferencial crucial. Essa expertise permitiu-me não apenas entender os processos existentes, mas também desenvolver novos fluxos e soluções utilizando o UiPath. Agora, como desenvolvedor UiPath, concentro-me em simplificar processos e impulsionar a eficiência operacional, construindo pontes entre minha bagagem no Totvs RM e as possibilidades ilimitadas da automação.

    Sobre da Pessoa:
    [NOME DA PESSOA]: [SOBRE A PESSOA]

    Instruções Adicionais:

    Destaque pontos em comum, como experiências profissionais, habilidades, interesses ou objetivos.

    Mostre interesse genuíno na trajetória da pessoa.

    Sugira um motivo para a conexão, como trocar ideias, colaborar em projetos ou compartilhar conhecimentos.

    Mantenha a mensagem concisa e direta, com no máximo 2 parágrafos.

    Me retorne apenas a mensagem para copiar e colar.
    """

    prompt = prompt.replace("[NOME DA PESSOA]", str(name_to_profile))
    prompt = prompt.replace("[SOBRE A PESSOA]", str(text))

    # Envie o prompt para a API do Gemini e obtenha a resposta (resposta_da_api)
    # Configure a API com sua chave de API
    google_api_key = os.getenv("GOOGLE_API_KEY")  # Pega a variável do ambiente
    genai.configure(api_key=google_api_key)

    # Crie uma instância do modelo Gemini
    ai_version = config['ai']['gemini']
    model = genai.GenerativeModel(ai_version)

    # Gere o conteúdo
    response = model.generate_content(prompt)
    message = response.text

    return message
