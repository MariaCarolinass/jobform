from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict
from typing import Annotated, Optional
from datetime import datetime


class CandidatoCreate(BaseModel):
    nome: Annotated[str, StringConstraints(min_length=2, max_length=150)]
    email: EmailStr
    telefone: Annotated[str, StringConstraints(min_length=6, max_length=50)]
    cargo_desejado: Annotated[str, StringConstraints(min_length=1, max_length=150)]
    escolaridade: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    observacoes: Optional[str] = None


class CandidatoRead(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    cargo_desejado: str
    escolaridade: str
    observacoes: Optional[str]
    arquivo: str
    ip: str
    data_envio: datetime

    model_config = ConfigDict(from_attributes=True)