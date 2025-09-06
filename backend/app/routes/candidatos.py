from fastapi import APIRouter, Depends, UploadFile, File, Form, Request, HTTPException
from sqlalchemy.orm import Session
from ..crud import candidato as candidato_crud
from ..schemas import candidato as candidato_schemas
from ..core.database import get_db
from ..utils.file import save_upload_file
from ..utils.email import send_candidato_email

router = APIRouter()

@router.post("/candidatos", status_code=201, response_model=candidato_schemas.CandidatoRead)
async def create_candidato(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cargo_desejado: str = Form(...),
    escolaridade: str = Form(...),
    observacoes: str | None = Form(None),
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        candidato_in = candidato_schemas.CandidatoCreate(
            nome=nome,
            email=email,
            telefone=telefone,
            cargo_desejado=cargo_desejado,
            escolaridade=escolaridade,
            observacoes=observacoes,
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    arquivo_path = await save_upload_file(arquivo)
    ip = request.client.host if request.client else "-"
    db_obj = candidato_crud.create_candidato(db, candidato_in, arquivo_path, ip)
    
    email_status = "ok"
    try:
        await send_candidato_email(db_obj, arquivo_path)
    except Exception as e:
        print("Erro ao enviar email:", e)
        email_status = "falhou"

    return {**db_obj.__dict__, "email_status": email_status}