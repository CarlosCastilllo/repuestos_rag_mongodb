"""Colección: chunks

Campos esperados (referencia, aún sin validar):
- doc_id, chunk_index, estrategia_chunking, chunk_texto, embedding [384]
- modelo, idioma, fecha, fecha_ingesta
"""

NOMBRE = "chunks"

# RN-09, RN-10
REGLAS = {
    "bsonType": "object",
    "required": [
        "doc_id",
        "chunk_index",
        "estrategia_chunking",
        "chunk_texto",
        "embedding",
        "modelo",
    ],
    "properties": {
        "doc_id": {"bsonType": "objectId"},
        "chunk_index": {"bsonType": "int", "minimum": 0},
        "estrategia_chunking": {
            "bsonType": "string",
            "enum": ["fixed-size", "sentence-aware", "semantic"],
        },
        "chunk_texto": {"bsonType": "string", "minLength": 1},
        "embedding": {
            "bsonType": "array",
            "minItems": 384,
            "maxItems": 384,
            "items": {"bsonType": "number"},
        },
        "modelo": {"bsonType": "string"},
        "idioma": {"bsonType": "string"},
        "fecha": {"bsonType": "date"},
        "fecha_ingesta": {"bsonType": "date"},
    },
}

INDICES = [
    {
        "nombre": "uniq_doc_estrategia_indice",
        "campos": [
            ("doc_id", 1),
            ("estrategia_chunking", 1),
            ("chunk_index", 1),
        ],
        "unico": True,
    },
]

INDICE_VECTORIAL = {
    "nombre": "vector_index",
    "definicion": {
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 384,
                "similarity": "cosine",
            },
            {"type": "filter", "path": "estrategia_chunking"},
            {"type": "filter", "path": "idioma"},
        ]
    },
}
