"""Colección: movimientos_inventario

Campos esperados (referencia, aún sin validar):
- producto_id, tipo (entrada/salida/ajuste), cantidad, proveedor_id, pedido_id, fecha
"""

NOMBRE = "movimientos_inventario"

REGLAS = {
    "bsonType": "object",
    "required": ["producto_id", "tipo", "cantidad", "fecha"],
    "properties": {
        "producto_id": {"bsonType": "objectId"},
        "tipo": {
            "bsonType": "string",
            "enum": ["entrada", "salida", "ajuste"],
        },
        "cantidad": {"bsonType": "number"},
        "proveedor_id": {"bsonType": "objectId"},
        "pedido_id": {"bsonType": "objectId"},
        "fecha": {"bsonType": "date"},
    },
}

INDICES = [
    {
        "nombre": "idx_producto_fecha",
        "campos": [("producto_id", 1), ("fecha", -1)],
    },
    {
        "nombre": "idx_proveedor_parcial",
        "campos": [("proveedor_id", 1)],
        "parcial": {"proveedor_id": {"$exists": True}},
    },
]
