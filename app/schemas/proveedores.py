"""Colección: proveedores

Campos esperados (referencia, aún sin validar):
- nombre, contacto, telefono
"""

NOMBRE = "proveedores"

REGLAS = {
    "bsonType": "object",
    "required": ["nombre", "telefono"],
    "properties": {
        "nombre": {"bsonType": "string"},
        "telefono": {"bsonType": "string"},
        "contacto": {"bsonType": "string"},
    },
}

INDICES = [
    {
        "nombre": "idx_nombre",
        "campos": [("nombre", 1)],
    },
]
