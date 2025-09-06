from fastapi import FastAPI
from .core.database import engine, Base
from .routes import candidatos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobForm - Backend")
app.include_router(candidatos.router)

@app.get("/")
async def root():
    return {"status": "ok", "service": "JobForm backend"}