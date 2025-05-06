from langchain_ollama import ChatOllama
from app.orchestration.recommendation_api.prompt_engineer import PromptEngineer
import json
import os  # Adicionado para manipulação de arquivos

class OllamaAnalyzer:
    def __init__(self, ollama_url, model):
        self.ollama_url = ollama_url
        self.model = model

    def analyze(self, endpoints, user_input, system_context, prompt_method):
        """
        Envia os endpoints e a mensagem do usuário ao Ollama.
        Se falhar, lê a resposta simulada de 'response_llm.txt'.
        """
        endpoints_json = json.dumps(endpoints, indent=4)
        llm = ChatOllama(model=self.model, temperature=0, base_url=self.ollama_url)
        
        prompt_engineer = PromptEngineer()
        prompt = getattr(prompt_engineer, prompt_method)(endpoints, user_input)
        messages = [("system", prompt), ("human", prompt)]
        
        try:
            stream = llm.stream(messages)
            full_response = ""
            for chunk in stream:
                full_response += chunk.content
            return full_response
        except Exception as e:
            # Caminho para o arquivo de resposta simulada
            simulated_response_path = os.path.join(
                os.path.dirname(__file__),  # Pasta do script atual
                r"C:\Users\elias\Desktop\Atlas\atlas-backend\app\orchestration\recommendation_api\response_llm.txt"
            )
            
            try:
                with open(simulated_response_path, "r", encoding="utf-8") as file:
                    return file.read()
            except FileNotFoundError:
                print("Erro: Arquivo 'response_llm.txt' não encontrado.")
                return "Não foi possível gerar uma resposta."