from typing import Optional, Dict
from .persona import Persona

class Pasajero(Persona):
    def __init__(self, nombre: str, documento: str, correo: Optional[str] = None):
        super().__init__(nombre, documento)
        self.correo = correo

    def to_dict(self) -> Dict:
        d = super().to_dict()
        d.update({"correo": self.correo or ""})
        return d
