# orchestrator.py
from app.orchestration.recommendation_api.examples_selector import ExamplesSelector
from app.orchestration.recommendation_api.exemple_data import examples
from app.orchestration.recommendation_api.ollama_analyzer import OllamaAnalyzer
from app.orchestration.recommendation_api.endpoint_extractor import EndpointExtractor

import os
from dotenv import load_dotenv
load_dotenv()
LLM = os.getenv("LLM")


class Orchestrator:
    @staticmethod
    def analyze_swagger(model_name: str, user_query: str) -> dict:

        selector = ExamplesSelector(base_url=LLM, embed_model_name="nomic-embed-text", examples=examples, k=5, mmr=False)
        selected_examples = selector.select_examples(user_query)

        print(selected_examples)

        analyzer = OllamaAnalyzer(LLM, model_name)
        llm_response = analyzer.analyze(selected_examples)  # Agora só usa os exemplos selecionados

        raw_options = EndpointExtractor.extract_recommended_endpoints(llm_response)

        if not raw_options:
            print("Nenhum endpoint recomendado encontrado.")
            return

        formatted_response = ""
        menu_options = []
        for idx, endpoint in enumerate(raw_options, 1):
            formatted_response += f"**Opção{idx} - {endpoint['path']} - {endpoint['description']}"
            menu_options.append(f"**Opção{idx} - {endpoint['path']} - {endpoint['description']}")

        return {
            "llm_response": llm_response + formatted_response,
            "options": menu_options
        }
