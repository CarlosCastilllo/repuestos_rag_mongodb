"""Colección: cupones

Campos esperados (referencia, aún sin validar):
- codigo, descuento_pct, vigente_hasta, usos_restantes
"""

NOMBRE = "cupones"

# RN-05
REGLAS = {
    "bsonType": "object",
    "required": ["codigo", "descuento_pct", "vigente_hasta", "usos_restantes"],
    "properties": {
        "codigo": {
            "bsonType": "string",
            "minLength": 4,
            "maxLength": 20,
            "pattern": r"^[A-Z0-9_-]{4,20}$",
        },
        "descuento_pct": {
            "bsonType": "number",
            "minimum": 1,
            "maximum": 100,
        },
        "vigente_hasta": {"bsonType": "date"},
        "usos_restantes": {"bsonType": "number", "minimum": 0},
    },
}

INDICES = [
    {
        "nombre": "uniq_codigo",
        "campos": [("codigo", 1)],
        "unico": True,
    },
]
