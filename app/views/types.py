from pydantic import BaseModel, Field

class TestNameDTO(BaseModel):
    name: str = Field(...,description="Nome para a saudação. Deve ter entre 2 e 50 caracteres alfabéticos.")
    