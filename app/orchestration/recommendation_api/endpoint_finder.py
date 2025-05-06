class EndpointDetailsFinder:

    @staticmethod
    def find_endpoint_details(swagger_data, path):
        """
        Busca detalhes do endpoint no Swagger pelo path.
        Separa os parâmetros por tipo: path, query, body.
        """
        for method, details in swagger_data.get("paths", {}).get(path, {}).items():
            parameters = details.get("parameters", [])
            request_body = details.get("requestBody", {})

            # Separa por tipo
            path_params = [
                {"name": p["name"], "type": p.get("schema", {}).get("type", "string")}
                for p in parameters if p.get("in") == "path"
            ]
            query_params = [
                {"name": p["name"], "type": p.get("schema", {}).get("type", "string")}
                for p in parameters if p.get("in") == "query"
            ]

            # Extrai campos do body (quando houver)
            body_schema = request_body.get("content", {}).get("application/json", {}).get("schema", {})
            body_fields = []
            if "properties" in body_schema:
                body_fields = [
                    {"name": field, "type": definition.get("type", "string")}
                    for field, definition in body_schema["properties"].items()
                ]

            return {
                "path": path,
                "method": method.upper(),
                "path_params": path_params,
                "query_params": query_params,
                "request_body": body_fields,
            }

        return None
