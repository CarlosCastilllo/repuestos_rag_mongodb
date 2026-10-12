"""Colección: resenas

Campos esperados (referencia, aún sin validar):
- producto_id, cliente_id, rating, texto, fecha
"""

NOMBRE = "resenas"

REGLAS = {
    "bsonType": "object",
    "required": ["producto_id", "cliente_id", "rating", "fecha"],
    "properties": {
        "producto_id": {"bsonType": "objectId"},
        "cliente_id": {"bsonType": "objectId"},
        "rating": {
            "bsonType": "number",
            "minimum": 1,
            "maximum": 5,
        },
        "texto": {"bsonType": "string", "maxLength": 1000},
        "fecha": {"bsonType": "date"},
    },
}

INDICES = [
    {
        "nombre": "idx_producto_fecha",
        "campos": [("producto_id", 1), ("fecha", -1)],
    },
    {
        "nombre": "idx_cliente",
        "campos": [("cliente_id", 1)],
    },
]
