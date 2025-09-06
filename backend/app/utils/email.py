import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from dotenv import load_dotenv

load_dotenv()
conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost"),
    MAIL_STARTTLS = os.getenv("MAIL_STARTTLS", "True").lower() in ("true", "1", "yes"),
    MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS", "False").lower() in ("true", "1", "yes"),
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_candidato_email(candidato, arquivo_path: str | None = None):
    html = f"""
    <h3>Novo envio de currículo</h3>
    <ul>
        <li><strong>Nome:</strong> {candidato.nome}</li>
        <li><strong>Email:</strong> {candidato.email}</li>
        <li><strong>Telefone:</strong> {candidato.telefone}</li>
        <li><strong>Cargo desejado:</strong> {candidato.cargo_desejado}</li>
        <li><strong>Escolaridade:</strong> {candidato.escolaridade}</li>
        <li><strong>Observações:</strong> {candidato.observacoes or "-"}</li>
        <li><strong>IP:</strong> {candidato.ip}</li>
        <li><strong>Data envio:</strong> {candidato.data_envio}</li>
    </ul>
    """

    message = MessageSchema(
        subject="[JobForm] Novo currículo enviado",
        recipients=[os.getenv("MAIL_FROM")],
        body=html,
        subtype=MessageType.html,
        attachments=[arquivo_path] if arquivo_path else None
    )

    fm = FastMail(conf)
    await fm.send_message(message)