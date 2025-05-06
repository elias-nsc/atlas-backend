from fastapi import APIRouter, Depends
from app.orchestration.recommendation_api.orchestrator import Orchestrator
from app.views.response import test_response_example
from app.views.description import description_ola
from pydantic import BaseModel, Field
from typing import Optional

from app.views.types import *

router = APIRouter()

@router.post("/analyze-endpoints",)
async def analyze_endpoints(request: AnalysisRequestDTO):
    result = Orchestrator.analyze_swagger(request.model_name, request.user_query)
    return result

# @router.post("/execute-endpoint")
# async def execute_endpoint(request: ExecuteEndpointRequestDTO):
#     result = Orchestrator.execute_selected_option(request.selected_option, request.options)
#     return result

@router.post("/get-endpoint-params")
async def get_endpoint_params(request: GetParamsRequestDTO):
    return Orchestrator.get_required_params(request.selected_option, request.options)


@router.post("/execute-endpoint-with-params")
async def execute_endpoint_with_params(request: ExecuteWithParamsDTO):
    return Orchestrator.execute_endpoint_with_params(request.path, request.params)

