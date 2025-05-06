import requests
class ApiRequester:
    def __init__(self, base_url):
        self.base_url = base_url
        
    def make_request(self, endpoint):
        """
        Solicita os parâmetros e realiza a requisição na API.
        """
        print("\nForneça os dados necessários para a requisição.")
        path = endpoint["path"]
        print(path)
        for param in endpoint["parameters"]:
            if f"{{{param['name']}}}" in path:  
                value = input(f"{param['name']} ({param['type']}): ")
                print(value)
                path = path.replace(f"{{{param['name']}}}", value)
        print(path)

        params = {}
        for param in endpoint["parameters"]:
            if f"{{{param['name']}}}" not in path: 
                value = input(f"{param['name']} ({param['type']}): ")
                params[param["name"]] = value
        print(params)

        body = {}
        for field in endpoint["request_body"]:
            value = input(f"{field['name']} ({field['type']}): ")
            body[field["name"]] = value
        print(body)
        
        url = self.base_url + path
        print(f"URL da requisição: {url}")
        try:
            if endpoint["method"] == "GET":
                response = requests.get(url,  params=params)
                print("parametros: ",params)
            elif endpoint["method"] == "POST":
                response = requests.post(url,  json=body)
            elif endpoint["method"] == "PUT":
                response = requests.put(url,  json=body)
            elif endpoint["method"] == "DELETE":
                response = requests.delete(url,  params=params)
            else:
                print(f"Método HTTP não suportado: {endpoint['method']}")
                return
            print("\nResposta da API:")
            print(f"Status Code: {response.status_code}")
            print(f"Resposta: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer a requisição: {e}")