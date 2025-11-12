import json
import random
from pathlib import Path
from typing import List, Dict
from models import Animal, Herd, AnimalStatus, Location


class DataManager:
    """Gerenciador de dados dos animais e rebanhos com simulação"""

    def __init__(self, data_file: str = "animal-history.json"):
        self.data_file = Path(__file__).parent / data_file
        self.animals: List[Animal] = []
        self.herds: List[Herd] = []
        self._load_data()

    def _load_data(self):
        """Carrega dados do arquivo JSON"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Carrega rebanhos
        self.herds = [Herd(**herd) for herd in data['herds']]

        # Carrega animais e inicializa com último registro do histórico
        for animal_data in data['animals']:
            animal = Animal(**animal_data)

            # Se tem histórico, pega o último registro
            if animal.history and len(animal.history) > 0:
                last_record = animal.history[-1]
                animal.status = last_record.status
                animal.location = last_record.location
                animal.temperature = last_record.temperature
                animal.steps = last_record.steps

            # Verifica alertas iniciais
            animal = self._check_alerts(animal)
            self.animals.append(animal)

    def _is_point_in_polygon(self, point: Location, polygon: List[Location]) -> bool:
        """Verifica se um ponto está dentro de um polígono"""
        x, y = point.lat, point.lng
        n = len(polygon)
        inside = False

        p1 = polygon[0]
        for i in range(1, n + 1):
            p2 = polygon[i % n]
            if y > min(p1.lng, p2.lng):
                if y <= max(p1.lng, p2.lng):
                    if x <= max(p1.lat, p2.lat):
                        if p1.lng != p2.lng:
                            xinters = (y - p1.lng) * (p2.lat - p1.lat) / (p2.lng - p1.lng) + p1.lat
                        if p1.lat == p2.lat or x <= xinters:
                            inside = not inside
            p1 = p2

        return inside

    def _check_alerts(self, animal: Animal) -> Animal:
        """Verifica e atualiza alertas do animal"""
        alerts = []
        status = AnimalStatus.Healthy

        # Verifica temperatura
        if animal.temperature >= 40.0:
            status = AnimalStatus.Danger
            alerts.append('Temperatura muito alta')
        elif animal.temperature >= 39.1:
            status = AnimalStatus.Warning
            alerts.append('Temperatura elevada')

        # Verifica geofencing
        herd = next((h for h in self.herds if h.id == animal.herdId), None)
        if herd and not self._is_point_in_polygon(animal.location, herd.polygon):
            if status < AnimalStatus.Warning:
                status = AnimalStatus.Warning
            alerts.append('Fora da área designada')

        animal.status = status
        animal.alert = '; '.join(alerts) if alerts else None
        return animal

    def simulate_update(self):
        """Simula atualização dos dados dos animais"""
        for i, animal in enumerate(self.animals):
            # Simula movimento (pequeno deslocamento)
            animal.location.lat += random.uniform(-0.0001, 0.0001)
            animal.location.lng += random.uniform(-0.0001, 0.0001)

            # Simula temperatura
            random_status = random.random()
            if random_status < 0.01 and animal.status != AnimalStatus.Danger:
                animal.temperature = round(random.uniform(40.0, 41.5), 1)
            elif random_status < 0.03 and animal.status == AnimalStatus.Healthy:
                animal.temperature = round(random.uniform(39.1, 39.9), 1)
            elif animal.status != AnimalStatus.Healthy and random_status > 0.1:
                animal.temperature = round(random.uniform(38.0, 39.0), 1)
            else:
                animal.temperature = round(
                    max(38.0, min(41.5, animal.temperature + random.uniform(-0.2, 0.2))),
                    1
                )

            # Simula passos (incremento)
            animal.steps += random.randint(10, 50)

            # Atualiza alertas
            self.animals[i] = self._check_alerts(animal)

    def get_animals(self) -> List[Animal]:
        """Retorna lista de animais"""
        return self.animals

    def get_herds(self) -> List[Herd]:
        """Retorna lista de rebanhos"""
        return self.herds

    def get_animal_by_id(self, animal_id: int) -> Animal | None:
        """Retorna um animal específico pelo ID"""
        return next((a for a in self.animals if a.id == animal_id), None)

    def get_herd_by_id(self, herd_id: int) -> Herd | None:
        """Retorna um rebanho específico pelo ID"""
        return next((h for h in self.herds if h.id == herd_id), None)
