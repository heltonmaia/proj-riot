from pydantic import BaseModel
from typing import List, Optional
from enum import IntEnum


class AnimalStatus(IntEnum):
    """Status do animal"""
    Healthy = 0
    Warning = 1
    Danger = 2


class Location(BaseModel):
    """Coordenadas geográficas"""
    lat: float
    lng: float


class AnimalHistoryRecord(BaseModel):
    """Registro histórico de um animal"""
    date: str
    status: AnimalStatus
    location: Location
    temperature: float
    steps: int


class Animal(BaseModel):
    """Modelo de dados de um animal"""
    id: int
    collarId: str
    herdId: int
    name: str
    status: AnimalStatus
    alert: Optional[str] = None
    location: Location
    temperature: float
    steps: int
    type: str  # 'Vaca' | 'Touro' | 'Bezerro'
    breed: str
    age: int  # em meses
    weight: float  # em kg
    history: Optional[List[AnimalHistoryRecord]] = None


class Herd(BaseModel):
    """Modelo de dados de um rebanho"""
    id: int
    name: str
    region: str
    location: Location
    polygon: List[Location]


class AnimalsResponse(BaseModel):
    """Resposta da API com lista de animais"""
    animals: List[Animal]


class HerdsResponse(BaseModel):
    """Resposta da API com lista de rebanhos"""
    herds: List[Herd]


class DataResponse(BaseModel):
    """Resposta completa com animais e rebanhos"""
    animals: List[Animal]
    herds: List[Herd]
