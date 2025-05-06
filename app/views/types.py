from pydantic import BaseModel, Field

class AnalysisRequestDTO(BaseModel):
    model_name: str = Field(...,
                          description="Nome do modelo LLM a ser usado (ex: 'deepseek-r1:14b')")
    user_query: str = Field(...,
                           description="Pergunta/necessidade do usuário para análise dos endpoints")

class GetParamsRequestDTO(BaseModel):
    selected_option: str
    options: list[str]

class ExecuteWithParamsDTO(BaseModel):
    path: str
    params: dict  # parâmetros preenchidos pelo usuário (path/query/body)


