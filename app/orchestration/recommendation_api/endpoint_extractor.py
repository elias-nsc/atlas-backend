import re
class EndpointExtractor:
    
    @staticmethod
    def extract_recommended_endpoints(response):
        """
        Extrai os endpoints recomendados da resposta do Ollama.
        """
        options = []
        for line in response.split("\n"):
            if "Opção" in line and "-" in line:
                parts = line.split(" - ")
                if len(parts) >= 3:
                    sanitized_path = EndpointExtractor.sanitize_path(parts[1].strip())
                    options.append({"path": sanitized_path, "description": parts[2].strip()})
        return options

    @staticmethod

    def sanitize_path(path):
        """
        Remove caracteres especiais extras, como ** ou espaços extras.
        """
        return re.sub(r"[^a-zA-Z0-9/{}/_.-]", "", path)