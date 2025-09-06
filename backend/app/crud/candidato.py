from sqlalchemy.orm import Session
from ..models import candidato as candidato_model
from ..schemas import candidato as candidato_schemas

def create_candidato(db: Session, candidato: candidato_schemas.CandidatoCreate, arquivo_path: str, ip: str):
    db_cand = candidato_model.Candidato(
        nome=candidato.nome,
        email=candidato.email,
        telefone=candidato.telefone,
        cargo_desejado=candidato.cargo_desejado,
        escolaridade=candidato.escolaridade,
        observacoes=candidato.observacoes,
        arquivo=arquivo_path,
        ip=ip,
    )

    db.add(db_cand)
    db.commit()
    db.refresh(db_cand)

    return db_cand