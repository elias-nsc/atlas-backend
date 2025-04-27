from fastapi import status

# Exemplo concreto para a rota /test/{name}
test_response_example = {
    status.HTTP_200_OK: {
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "message": "Operação Realizada com sucesso!",
                    "data": {
                        "message": "Olá João"
                    }
                }
            }
        }
    }
}