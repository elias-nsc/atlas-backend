from fastapi import APIRouter, Depends
from app.orchestration.orchestrator import TestOrchestrator
from app.views.response import test_response_example
from app.views.description import description_ola

from app.views.types import TestNameDTO

router = APIRouter()

@router.get("/test/{name}",
            tags=["Olá"],
            responses=test_response_example,
            description=description_ola,
            summary="Retorna um olá + nome",
            )
def test_endpoint(name: str = Depends(TestNameDTO)):
    greeting = TestOrchestrator.greet(name)
    return greeting