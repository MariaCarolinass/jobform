from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..core.database import Base


class Candidato(Base):
    __tablename__ = "candidatos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    telefone = Column(String(50), nullable=False)
    cargo_desejado = Column(String(150), nullable=False)
    escolaridade = Column(String(50), nullable=False)
    observacoes = Column(Text, nullable=True)
    arquivo = Column(String(255), nullable=False)
    ip = Column(String(45), nullable=False)
    data_envio = Column(DateTime(timezone=True), server_default=func.now())