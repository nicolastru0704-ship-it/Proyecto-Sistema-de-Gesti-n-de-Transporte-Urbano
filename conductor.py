from typing import Dict
from .persona import Persona

class Conductor(Persona):
    def __init__(self, nombre: str, documento: str, licencia: str):
        super().__init__(nombre, documento)
        self.licencia = licencia
        self.ganancias_acumuladas = 0.0

    def to_dict(self) -> Dict:
        d = super().to_dict()
        d.update({"licencia": self.licencia, "ganancias_acumuladas": f"{self.ganancias_acumuladas:.2f}"})
        return d
