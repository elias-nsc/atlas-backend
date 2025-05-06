import os
import importlib
import app.orchestration.recommendation_api.swagger_client as swagger_client 
from dotenv import load_dotenv
from app.orchestration.recommendation_api.swagger_client import SwaggerClient
from app.orchestration.recommendation_api.ollama_analyzer import OllamaAnalyzer
from app.orchestration.recommendation_api.endpoint_extractor import EndpointExtractor
from app.orchestration.recommendation_api.endpoint_finder import EndpointDetailsFinder
from app.orchestration.recommendation_api.api_requester import ApiRequester
importlib.reload(swagger_client)
load_dotenv()

LLM = os.getenv("LLM")
SWAGGER = os.getenv("PET_SWAGGER")
SWAGGER_URL = os.getenv("PET_SWAGGER_URL")

class Orchestrator:
    
    @staticmethod
    def analyze_swagger(model_name: str, user_query: str) -> dict:
        print(model_name)
        print(user_query)
        analyzer = OllamaAnalyzer(LLM, model_name)
        swagger = SwaggerClient(SWAGGER)

        endpoints, swagger_data = swagger.get_endpoints()
        if not endpoints:
            return {"error": "Nenhum endpoint encontrado no Swagger"}
        
        llm_response = analyzer.analyze(endpoints, user_query, "", "few_shot")
        raw_options = EndpointExtractor.extract_recommended_endpoints(llm_response)

        formatted_response = ""
        menu_options = []
        
        if not raw_options:
            print("Nenhum endpoint recomendado encontrado.")
            return
        print("\nEscolha a opção que melhor atende a sua necessidade:")
        for idx, endpoint in enumerate(raw_options, 1):
            formatted_response += f"**Opção{idx} - {endpoint['path']} - {endpoint['description']}"
            menu_options.append(f"**Opção{idx} - {endpoint['path']} - {endpoint['description']}")
        
        return {
            "llm_response": llm_response + formatted_response,
            "options":menu_options
         }
    

    @staticmethod
    def get_required_params(selected_option: str, options: list[str]) -> dict:
        try:
            option_number = int(selected_option.replace("Opção", "").strip()) - 1
            if not (0 <= option_number < len(options)):
                return {"error": "Opção inválida."}
            
            selected_option_str = options[option_number]
            path_start = selected_option_str.find(" - ") + 3
            path_end = selected_option_str.find(" - ", path_start)
            if path_end == -1:
                path_end = len(selected_option_str)
            chosen_path = selected_option_str[path_start:path_end].strip()

            swagger = SwaggerClient(SWAGGER)
            _, swagger_data = swagger.get_endpoints()
            endpoint_details = EndpointDetailsFinder.find_endpoint_details(swagger_data, chosen_path)
            if not endpoint_details:
                return {"error": "Detalhes do endpoint não encontrados."}

            # Aqui extraímos apenas os campos necessários
            return {
                "path": chosen_path,
                "method": endpoint_details["method"],
                "required_params": {
                    "path": endpoint_details.get("path_params", []),
                    "query": endpoint_details.get("query_params", []),
                    "body": endpoint_details.get("request_body", {}),
                }
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def execute_endpoint_with_params(chosen_path: str, params: dict) -> dict: 
        try:
            swagger = SwaggerClient(SWAGGER)
            _, swagger_data = swagger.get_endpoints()
            
            endpoint_details = EndpointDetailsFinder.find_endpoint_details(swagger_data, chosen_path)
            if not endpoint_details:
                return {"error": "Detalhes do endpoint não encontrados."}

            requester = ApiRequester(SWAGGER_URL)
            response = requester.make_request(endpoint_details, params)
            return {
                "path": chosen_path,
                "api_response": response
            }

        except Exception as e:
            return {"error": f"Erro ao executar endpoint: {str(e)}"}