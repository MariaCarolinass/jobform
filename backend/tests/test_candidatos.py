from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine
from app.utils.file import UPLOAD_DIR, MAX_BYTES, ALLOWED_EXT
import pytest

Base.metadata.create_all(bind=engine)
client = TestClient(app)

@pytest.fixture(autouse=True)
def temp_upload_dir(tmp_path, monkeypatch):
    """Redireciona UPLOAD_DIR para um diretório temporário"""
    temp_dir = tmp_path / "uploads"
    temp_dir.mkdir()
    monkeypatch.setattr("app.utils.file.UPLOAD_DIR", str(temp_dir))
    return temp_dir

def test_missing_fields():
    resp = client.post("/candidatos", data={})
    assert resp.status_code == 422

def test_invalid_file_extension(temp_upload_dir, tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(b"hello")

    with open(file_path, "rb") as f:
        resp = client.post(
            "/candidatos",
            data={
                "nome": "Fulano",
                "email": "fulano@example.com",
                "telefone": "123456789",
                "cargo_desejado": "Dev",
                "escolaridade": "Superior",
            },
            files={"arquivo": ("test.txt", f, "text/plain")},
        )

    assert resp.status_code == 400
    assert "não permitida" in resp.json()["detail"]

def test_large_file(temp_upload_dir, tmp_path):
    large = tmp_path / "big.pdf"  # arquivo > 1MB
    large.write_bytes(b"0" * (MAX_BYTES + 1))

    with open(large, "rb") as f:
        resp = client.post(
            "/candidatos",
            data={
                "nome": "Fulano",
                "email": "fulano@example.com",
                "telefone": "123456789",
                "cargo_desejado": "Dev",
                "escolaridade": "Superior",
            },
            files={"arquivo": ("big.pdf", f, "application/pdf")},
        )

    assert resp.status_code == 400
    assert "tamanho máximo" in resp.json()["detail"]

def test_successful_submission(temp_upload_dir, tmp_path):
    small = tmp_path / "cv.pdf"
    small.write_bytes(b"%PDF-1.4\n%Teste\n")  # conteúdo mínimo válido de PDF

    with open(small, "rb") as f:
        resp = client.post(
            "/candidatos",
            data={
                "nome": "Fulano",
                "email": "fulano@example.com",
                "telefone": "123456789",
                "cargo_desejado": "Dev",
                "escolaridade": "Superior",
            },
            files={"arquivo": ("cv.pdf", f, "application/pdf")},
        )

    assert resp.status_code == 201
    json_data = resp.json()
    assert "id" in json_data
    assert json_data["nome"] == "Fulano"
    
    saved_files = list(Path(temp_upload_dir).iterdir())
    assert any(f.name in json_data["arquivo"] for f in saved_files)
