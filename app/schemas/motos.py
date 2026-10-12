"""Colección: motos

Campos esperados (referencia, aún sin validar):
- marca, modelo, cilindraje, anio_desde, anio_hasta
"""

NOMBRE = "motos"

REGLAS = {
    "bsonType": "object",
    "required": ["marca", "modelo", "cilindraje"],
    "properties": {
        "marca": {"bsonType": "string"},
        "modelo": {"bsonType": "string"},
        "cilindraje": {
            "bsonType": "number",
            "minimum": 50,
            "maximum": 1500,
        },
        "anio_desde": {"bsonType": "int", "minimum": 1980},
        "anio_hasta": {"bsonType": "int", "minimum": 1980},
    },
}

INDICES = [
    {
        "nombre": "uniq_marca_modelo_cilindraje",
        "campos": [("marca", 1), ("modelo", 1), ("cilindraje", 1)],
        "unico": True,
    },
]
