"""Colección: pedidos

Campos esperados (referencia, aún sin validar):
- cliente_id, vendedor, canal (mostrador/whatsapp), fecha
- items [{producto_id, nombre_snapshot, precio_pagado, cantidad}]
- cupon_aplicado {codigo, descuento_pct}, envio {tipo, estado, guia}
- devoluciones [], total
"""

NOMBRE = "pedidos"

# RN-03, RN-07
REGLAS = {
    "bsonType": "object",
    "required": [
        "cliente_id",
        "vendedor",
        "canal",
        "fecha",
        "items",
        "total",
    ],
    "properties": {
        "cliente_id": {"bsonType": "objectId"},
        "vendedor": {"bsonType": "string"},
        "canal": {
            "bsonType": "string",
            "enum": ["mostrador", "whatsapp"],
        },
        "fecha": {"bsonType": "date"},
        "items": {
            "bsonType": "array",
            "minItems": 1,
            "items": {
                "bsonType": "object",
                "required": [
                    "producto_id",
                    "nombre_snapshot",
                    "precio_pagado",
                    "cantidad",
                ],
                "properties": {
                    "producto_id": {"bsonType": "objectId"},
                    "nombre_snapshot": {"bsonType": "string"},
                    "precio_pagado": {
                        "bsonType": "number",
                        "minimum": 0,
                        "exclusiveMinimum": True,
                    },
                    "cantidad": {"bsonType": "number", "minimum": 1},
                },
            },
        },
        "cupon_aplicado": {
            "bsonType": "object",
            "properties": {
                "codigo": {"bsonType": "string"},
                "descuento_pct": {"bsonType": "number"},
            },
        },
        "envio": {
            "bsonType": "object",
            "properties": {
                "tipo": {"bsonType": "string"},
                "estado": {
                    "bsonType": "string",
                    "enum": ["pendiente", "en camino", "entregado"],
                },
                "guia": {"bsonType": ["string", "null"]},
            },
        },
        "devoluciones": {
            "bsonType": "array",
            "items": {
                "bsonType": "object",
                "required": ["fecha", "motivo", "items"],
                "properties": {
                    "fecha": {"bsonType": "date"},
                    "motivo": {"bsonType": "string"},
                    "items": {"bsonType": "array", "minItems": 1},
                },
            },
        },
        "total": {"bsonType": "number"},
    },
}

INDICES = [
    {
        "nombre": "idx_cliente_fecha",
        "campos": [("cliente_id", 1), ("fecha", -1)],
    },
    {
        "nombre": "idx_items_producto",
        "campos": [("items.producto_id", 1)],
    },
    {
        "nombre": "idx_fecha",
        "campos": [("fecha", 1)],
    },
]
