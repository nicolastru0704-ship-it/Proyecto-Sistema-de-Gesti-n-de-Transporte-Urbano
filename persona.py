import uuid
from typing import Dict

class Persona:
    def __init__(self, nombre: str, documento: str):
        self.id = str(uuid.uuid4())
        self.nombre = nombre
        self.documento = documento

    def to_dict(self) -> Dict:
        return {"id": self.id, "nombre": self.nombre, "documento": self.documento}
