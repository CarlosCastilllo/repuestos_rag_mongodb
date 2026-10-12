"""Colección: documentos

Campos esperados (referencia, aún sin validar):
- titulo, idioma, fecha, fuente, contenido_texto
- metadatos {autor, categoria, etiquetas []}, imagenes [ObjectId]
"""

NOMBRE = "documentos"

# RN-08
REGLAS = {
    "bsonType": "object",
    "required": ["titulo", "idioma", "fecha", "fuente", "contenido_texto"],
    "properties": {
        "titulo": {"bsonType": "string"},
        "idioma": {
            "bsonType": "string",
            "enum": ["es", "en"],
        },
        "fecha": {"bsonType": "date"},
        "fuente": {"bsonType": "string"},
        "contenido_texto": {"bsonType": "string"},
        "metadatos": {
            "bsonType": "object",
            "properties": {
                "autor": {"bsonType": "string"},
                "categoria": {"bsonType": "string"},
                "etiquetas": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"},
                },
            },
        },
        "imagenes": {
            "bsonType": "array",
            "items": {"bsonType": "objectId"},
        },
    },
}

INDICES = [
    {
        "nombre": "idx_fecha_idioma",
        "campos": [("fecha", 1), ("idioma", 1)],
    },
    {
        "nombre": "idx_texto",
        "campos": [("contenido_texto", "text")],
        "idioma_por_defecto": "spanish",
    },
]
