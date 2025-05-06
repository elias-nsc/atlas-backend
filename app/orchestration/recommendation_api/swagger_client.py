import requests
import json
from random import shuffle
from typing import List, Dict, Optional
class SwaggerClient:
    def __init__(self, swagger_url: str):
        self.swagger_url = swagger_url
    def get_endpoints(self) -> tuple[List[Dict], Optional[Dict]]:
        """
        Retorna:
            - Lista de módulos com endpoints no formato simplificado
            - Dados brutos do Swagger (opcional)
        """
        try:
            response = requests.get(self.swagger_url, verify=False)
            response.raise_for_status()
            swagger_data = response.json()
        except Exception as e:
            print(f"Erro ao acessar o Swagger: {e}")
            return [], None

        # Mapeia descrições dos módulos (tags)
        tag_descriptions = {
            tag["name"]: tag.get("description", "").strip()
            for tag in swagger_data.get("tags", [])
        }
        modules = {}
        for path, methods in swagger_data.get("paths", {}).items():
            for method, details in methods.items():
                tags = details.get("tags", [])
                if not tags:
                    continue
                for tag in tags:
                    if tag not in modules:
                        modules[tag] = {
                            "Modulo": tag,
                            "description_modulo": tag_descriptions.get(tag, ""),
                            "Endpoints": []
                        }
                    # Extrai properties (parâmetros ou campos do body)
                    properties = self._extract_properties(details, swagger_data)
                    # Extrai exemplo de resposta (200)
                    response_example = self._extract_response_example(details)
                    endpoint = {
                        "path": path,
                        "method": method.upper(),
                        "description": (details.get("summary", "") + " " + details.get("description", "")).strip(),
                        "properties": properties,
                        "response": response_example
                    }
                    modules[tag]["Endpoints"].append(endpoint)
        # Embaralha a lista de módulos
        modules_list = list(modules.values())
        shuffle(modules_list)
        return modules_list, swagger_data
    
    def _extract_properties(self, endpoint_details: Dict, swagger_data: Dict) -> List[Dict]:
        """Extrai properties (parâmetros ou campos do body)"""
        properties = []

        # 1. Parâmetros (GET, PUT, DELETE)
        for param in endpoint_details.get("parameters", []):
            properties.append({
                "parametro": param.get("name"),
                "description": param.get("description", ""),
                "type": param.get("schema", {}).get("type", "string"),
                "required": param.get("required", False),
                "example": param.get("example")
            })
        # 2. Campos do Body (POST, PUT)
        if "requestBody" in endpoint_details:
            content = endpoint_details["requestBody"].get("content", {})
            if content:
                schema_ref = content.get("application/json", {}).get("schema", {}).get("$ref", "")
                if schema_ref:
                    schema = self._resolve_schema_reference(schema_ref, swagger_data)
                    for prop_name, prop_details in schema.get("properties", {}).items():
                        properties.append({
                            "parametro": prop_name,
                            "description": prop_details.get("description", ""),
                            "type": prop_details.get("type", "string"),
                            "required": prop_name in schema.get("required", []),
                            "example": prop_details.get("example")
                        })
        return properties
    def _extract_response_example(self, endpoint_details: Dict) -> Dict:
        """Extrai o exemplo de resposta (status 200)"""
        responses = endpoint_details.get("responses", {})
        if "200" in responses:
            content = responses["200"].get("content", {})
            if content:
                return content.get("application/json", {}).get("example", {})
        return {}
    def _resolve_schema_reference(self, ref: str, swagger_data: Dict) -> Dict:
        """Resolve referências ($ref) nos schemas"""
        if not ref.startswith("#/components/schemas/"):
            return {}
        schema_name = ref.split("/")[-1]
        return swagger_data.get("components", {}).get("schemas", {}).get(schema_name, {})
