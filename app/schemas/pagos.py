"""Colección: pagos

Campos esperados (referencia, aún sin validar):
- pedido_id, metodo, valor, estado, fecha
"""

NOMBRE = "pagos"

# RN-06
REGLAS = {
    "bsonType": "object",
    "required": ["pedido_id", "metodo", "valor", "estado", "fecha"],
    "properties": {
        "pedido_id": {"bsonType": "objectId"},
        "metodo": {
            "bsonType": "string",
            "enum": ["efectivo", "transferencia", "tarjeta", "billetera digital"],
        },
        "valor": {
            "bsonType": "number",
            "minimum": 0,
            "exclusiveMinimum": True,
        },
        "estado": {
            "bsonType": "string",
            "enum": ["pendiente", "aprobado", "rechazado"],
        },
        "fecha": {"bsonType": "date"},
    },
}

INDICES = [
    {
        "nombre": "uniq_pedido",
        "campos": [("pedido_id", 1)],
        "unico": True,
    },
]
