"""Colección: consultas

Campos esperados (referencia, aún sin validar):
- pregunta, estrategia_chunking, chunks_recuperados [{chunk_id, score}]
- respuesta, tiempos, fecha
"""

NOMBRE = "consultas"

REGLAS = {
    "bsonType": "object",
    "required": ["pregunta", "respuesta", "fecha"],
    "properties": {
        "pregunta": {"bsonType": "string"},
        "estrategia_chunking": {
            "bsonType": "string",
            "enum": ["fixed-size", "sentence-aware", "semantic"],
        },
        "chunks_recuperados": {
            "bsonType": "array",
            "items": {
                "bsonType": "object",
                "required": ["chunk_id", "score"],
                "properties": {
                    "chunk_id": {"bsonType": "objectId"},
                    "score": {
                        "bsonType": "number",
                        "minimum": 0,
                        "maximum": 1,
                    },
                },
            },
        },
        "respuesta": {"bsonType": "string"},
        "tiempos": {"bsonType": "object"},
        "fecha": {"bsonType": "date"},
    },
}

INDICES = [
    {
        "nombre": "idx_fecha",
        "campos": [("fecha", 1)],
    },
    {
        "nombre": "idx_estrategia_fecha",
        "campos": [("estrategia_chunking", 1), ("fecha", 1)],
    },
]
