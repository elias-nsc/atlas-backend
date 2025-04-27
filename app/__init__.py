from fastapi import FastAPI
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
app.include_router(router)