from typing import Optional, Dict
import uuid

class Ruta:
    def __init__(self, origen: str, destino: str, horario: str, tarifa_base: float):
        self.id = str(uuid.uuid4())
        self.origen = origen
        self.destino = destino
        self.horario = horario
        self.tarifa_base = float(tarifa_base)
        self.conductor_asignado_id: Optional[str] = None

    def asignar_conductor(self, conductor_id: str):
        self.conductor_asignado_id = conductor_id

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "origen": self.origen,
            "destino": self.destino,
            "horario": self.horario,
            "tarifa_base": f"{self.tarifa_base:.2f}",
            "conductor_asignado_id": self.conductor_asignado_id or ""
        }
