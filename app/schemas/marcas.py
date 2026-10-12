"""Colección: marcas

Campos esperados (referencia, aún sin validar):
- nombre, pais
"""

NOMBRE = "marcas"

REGLAS = {
    "bsonType": "object",
    "required": ["nombre"],
    "properties": {
        "nombre": {"bsonType": "string"},
    },
}

INDICES = [
    {
        "nombre": "uniq_nombre",
        "campos": [("nombre", 1)],
        "unico": True,
    },
]
