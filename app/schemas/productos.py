"""Colección: productos

Campos esperados (referencia, aún sin validar):
- nombre, categoria {_id, nombre}, marca {_id, nombre}, precio, stock
- especificaciones {}, compatibilidad [{moto_id, marca, modelo, cilindraje}]
- rating_promedio, total_resenas, imagenes_ids [], documentos_ids []
"""

NOMBRE = "productos"

# RN-01, RN-04
REGLAS = {
    "bsonType": "object",
    "required": [
        "nombre",
        "categoria",
        "marca",
        "precio",
        "stock",
        "especificaciones",
    ],
    "properties": {
        "nombre": {"bsonType": "string"},
        "categoria": {
            "bsonType": "object",
            "required": ["_id", "nombre"],
            "properties": {
                "_id": {"bsonType": "objectId"},
                "nombre": {"bsonType": "string"},
            },
        },
        "marca": {
            "bsonType": "object",
            "required": ["_id", "nombre"],
            "properties": {
                "_id": {"bsonType": "objectId"},
                "nombre": {"bsonType": "string"},
            },
        },
        "precio": {
            "bsonType": "number",
            "minimum": 0,
            "exclusiveMinimum": True,
        },
        "stock": {"bsonType": "number", "minimum": 0},
        "especificaciones": {"bsonType": "object"},
        "compatibilidad": {
            "bsonType": "array",
            "items": {
                "bsonType": "object",
                "required": ["moto_id", "marca", "modelo", "cilindraje"],
                "properties": {
                    "moto_id": {"bsonType": "objectId"},
                    "marca": {"bsonType": "string"},
                    "modelo": {"bsonType": "string"},
                    "cilindraje": {"bsonType": "number"},
                },
            },
        },
        "rating_promedio": {
            "bsonType": "number",
            "minimum": 0,
            "maximum": 5,
        },
        "total_resenas": {"bsonType": "number", "minimum": 0},
        "imagenes_ids": {
            "bsonType": "array",
            "items": {"bsonType": "objectId"},
        },
        "documentos_ids": {
            "bsonType": "array",
            "items": {"bsonType": "objectId"},
        },
    },
}

INDICES = [
    {
        "nombre": "idx_catalogo",
        "campos": [("categoria._id", 1), ("marca._id", 1), ("precio", 1)],
    },
    {
        "nombre": "idx_compatibilidad_moto",
        "campos": [("compatibilidad.moto_id", 1)],
    },
    {
        "nombre": "txt_nombre",
        "campos": [("nombre", "text")],
        "idioma_por_defecto": "spanish",
    },
]
