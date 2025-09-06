# JobForm

JobForm é uma aplicação Full Stack para envio de currículos, construída com **FastAPI** no backend e **Vue.js 3 + Vite** no frontend. O sistema permite enviar formulários com validação, salvar arquivos e enviar e-mails de notificação.  

---

## 🏗 Estrutura do projeto

```
jobform/
├── backend/
│   ├── app/                 # Código Python (FastAPI)
│   ├── tests/               # Testes unitários
│   ├── uploads/             # Arquivos enviados (local ou temporário)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/                 # Código Vue.js
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── .env
```

---

## ⚡ Tecnologias

- **Backend**: FastAPI, SQLAlchemy, SQLite, FastAPI-Mail, Python 3.10+
- **Frontend**: Vue.js 3, Vite
- **Docker**: Contêineres separados para frontend e backend
- **Banco de dados**: SQLite (simples para testes)
- **Testes**: Pytest, TestClient FastAPI

---

## 🔧 Funcionalidades

1. Formulário de envio de currículo com campos:
   - Nome
   - E-mail
   - Telefone
   - Cargo desejado (texto livre)
   - Escolaridade (select)
   - Observações (opcional)
   - Arquivo (PDF, DOC, DOCX; máximo 1MB)
2. Validação completa de campos e arquivos
3. Armazenamento de dados em banco SQLite
4. Registro de IP e data/hora do envio
5. Envio de e-mail com dados do formulário (arquivo anexo)
6. Testes unitários cobrindo casos de sucesso e falha

---

## 📦 Instalação e execução

### 1. Configurar variáveis de ambiente

Crie arquivo `.env` na raiz:

```ini
MAIL_USERNAME=seu_email@gmail.com
MAIL_PASSWORD=sua_senha_de_app
MAIL_FROM=seu_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
```

---

### 2. Rodar com Docker

```bash
docker-compose up --build
```

- Acessar: http://localhost:8080

> Frontend chama backend via `/api/...` configurado no Nginx.

---

### 3. Rodar local (sem Docker)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Testes

Os testes usam Pytest com **diretório temporário para uploads**:

```bash
PYTHONPATH=backend pytest backend/tests
```

Testes cobrem:

- Campos obrigatórios ausentes
- Arquivos inválidos (extensão e tamanho)
- Envio bem-sucedido
- Evita criação de arquivos corrompidos

---

## 🗄 Banco de dados

- SQLite (`jobform.db`)
- Tabela principal: `candidato`
- Campos:
  - `id`, `nome`, `email`, `telefone`, `cargo_desejado`, `escolaridade`, `observacoes`, `arquivo`, `ip`, `data_envio`

---

## 📂 Upload de arquivos

- Permitido: `.pdf`, `.doc`, `.docx`
- Tamanho máximo: 1MB
- Armazenados em `backend/uploads` (ou temporário durante testes)
- Nome gerado automaticamente para evitar conflitos

---

## ✉️ Envio de e-mail

- Configuração via FastAPI-Mail usando `.env`
- Envia HTML com dados do candidato
- Arquivo anexo incluído se presente
- Logs de erro aparecem no backend, mas envio não bloqueia salvamento

---

## ⚙️ Docker Compose

- Serviço **backend**: porta 8000
- Serviço **frontend**: porta 8080
- Volumes:
  - Backend: mantém `uploads` e banco SQLite
  - Frontend: serve build via Nginx

---

## ✅ Considerações finais

- Projeto pronto para testes e deploy local ou em servidor
- Código modularizado:
  - `app/crud` → operações de banco
  - `app/models` → modelos SQLAlchemy
  - `app/schemas` → Pydantic para validação
  - `app/utils/file.py` → upload seguro
  - `app/utils/email.py` → envio de e-mails
- Fácil de adaptar para PostgreSQL ou outro banco em produção
