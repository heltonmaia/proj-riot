from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os
from typing import List

from models import Animal, Herd, DataResponse, AnimalsResponse, HerdsResponse
from data_manager import DataManager


# Gerenciador de dados global
data_manager: DataManager | None = None


async def simulate_data_updates():
    """Task assíncrona para simular atualizações dos dados"""
    while True:
        await asyncio.sleep(2)  # Atualiza a cada 2 segundos
        if data_manager:
            data_manager.simulate_update()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    global data_manager

    # Startup: Inicializa dados e inicia simulação
    data_manager = DataManager()
    task = asyncio.create_task(simulate_data_updates())

    yield

    # Shutdown: Cancela a task de simulação
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


# Cria aplicação FastAPI
app = FastAPI(
    title="R-IoT Backend API",
    description="API para monitoramento rural inteligente com dados simulados",
    version="1.0.0",
    lifespan=lifespan
)

# Configuração de CORS
# Em desenvolvimento: permite todas as origens (*)
# Em produção: use ALLOWED_ORIGINS (ex: export ALLOWED_ORIGINS="https://seu-dominio.com,https://app.seu-dominio.com")
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins != "*":
    allowed_origins = [origin.strip() for origin in allowed_origins.split(",")]
else:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "R-IoT Backend API",
        "version": "1.0.0",
        "endpoints": {
            "animals": "/api/animals",
            "herds": "/api/herds",
            "data": "/api/data",
            "animal_by_id": "/api/animals/{animal_id}",
            "herd_by_id": "/api/herds/{herd_id}",
            "docs": "/docs"
        }
    }


@app.get("/api/animals", response_model=AnimalsResponse)
async def get_animals():
    """Retorna lista de todos os animais com dados atualizados"""
    if not data_manager:
        raise HTTPException(status_code=500, detail="Data manager not initialized")

    return AnimalsResponse(animals=data_manager.get_animals())


@app.get("/api/herds", response_model=HerdsResponse)
async def get_herds():
    """Retorna lista de todos os rebanhos"""
    if not data_manager:
        raise HTTPException(status_code=500, detail="Data manager not initialized")

    return HerdsResponse(herds=data_manager.get_herds())


@app.get("/api/data", response_model=DataResponse)
async def get_all_data():
    """Retorna todos os dados (animais e rebanhos)"""
    if not data_manager:
        raise HTTPException(status_code=500, detail="Data manager not initialized")

    return DataResponse(
        animals=data_manager.get_animals(),
        herds=data_manager.get_herds()
    )


@app.get("/api/animals/{animal_id}", response_model=Animal)
async def get_animal(animal_id: int):
    """Retorna dados de um animal específico"""
    if not data_manager:
        raise HTTPException(status_code=500, detail="Data manager not initialized")

    animal = data_manager.get_animal_by_id(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail=f"Animal {animal_id} not found")

    return animal


@app.get("/api/herds/{herd_id}", response_model=Herd)
async def get_herd(herd_id: int):
    """Retorna dados de um rebanho específico"""
    if not data_manager:
        raise HTTPException(status_code=500, detail="Data manager not initialized")

    herd = data_manager.get_herd_by_id(herd_id)
    if not herd:
        raise HTTPException(status_code=404, detail=f"Herd {herd_id} not found")

    return herd


@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "animals_count": len(data_manager.get_animals()) if data_manager else 0,
        "herds_count": len(data_manager.get_herds()) if data_manager else 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
