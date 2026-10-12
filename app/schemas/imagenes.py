"""Colección: imagenes

Campos esperados (referencia, aún sin validar):
- doc_id, ruta_archivo, descripcion, etiquetas [], embedding [512], modelo
"""

NOMBRE = "imagenes"

# RN-12
REGLAS = {
    "bsonType": "object",
    "required": ["doc_id", "ruta_archivo", "embedding", "modelo"],
    "properties": {
        "doc_id": {"bsonType": "objectId"},
        "ruta_archivo": {"bsonType": "string", "minLength": 1},
        "descripcion": {"bsonType": "string"},
        "etiquetas": {
            "bsonType": "array",
            "items": {"bsonType": "string"},
        },
        "embedding": {
            "bsonType": "array",
            "minItems": 512,
            "maxItems": 512,
            "items": {"bsonType": "number"},
        },
        "modelo": {"bsonType": "string"},
    },
}

INDICES = [
    {
        "nombre": "idx_documento",
        "campos": [("doc_id", 1)],
    },
]

INDICE_VECTORIAL = {
    "nombre": "vector_index_img",
    "definicion": {
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 512,
                "similarity": "cosine",
            }
        ]
    },
}
