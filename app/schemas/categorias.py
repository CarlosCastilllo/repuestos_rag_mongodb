"""Colección: categorias

Campos esperados (referencia, aún sin validar):
- nombre, descripcion
"""

NOMBRE = "categorias"

REGLAS = {
    "bsonType": "object",
    "required": ["nombre"],
    "properties": {
        "nombre": {"bsonType": "string", "minLength": 2},
    },
}

INDICES = [
    {
        "nombre": "uniq_nombre",
        "campos": [("nombre", 1)],
        "unico": True,
    },
]
