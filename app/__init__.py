from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.views.views import router

tags_metadata = [
    {
        "name": "Ola",
        "description": "Operações para retornar olá",
    }
]

app = FastAPI(
    title="Atlas",
    description="API para gerenciamento de posições",
    version="1.0.0",
    openapi_tags=tags_metadata
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens. Se preferir, especifique as origens que deseja permitir.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Inclui o seu router
app.include_router(router)
