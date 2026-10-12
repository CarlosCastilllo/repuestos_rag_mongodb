"""Colección: clientes

Campos esperados (referencia, aún sin validar):
- nombre, telefono, email, tipo, direcciones [{alias, calle, ciudad, principal}]
"""

NOMBRE = "clientes"

REGLAS = {
    "bsonType": "object",
    "required": ["nombre", "telefono"],
    "properties": {
        "nombre": {"bsonType": "string"},
        "telefono": {"bsonType": "string"},
        "email": {
            "bsonType": "string",
            "pattern": r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        },
        "tipo": {
            "bsonType": "string",
            "enum": ["particular", "mototaxista", "domiciliario", "taller"],
        },
        "direcciones": {
            "bsonType": "array",
            "maxItems": 5,
            "items": {
                "bsonType": "object",
                "required": ["alias", "calle", "ciudad"],
                "properties": {
                    "alias": {"bsonType": "string"},
                    "calle": {"bsonType": "string"},
                    "ciudad": {"bsonType": "string"},
                    "principal": {"bsonType": "bool"},
                },
            },
        },
    },
}

INDICES = [
    {
        "nombre": "uniq_telefono",
        "campos": [("telefono", 1)],
        "unico": True,
    },
    {
        "nombre": "uniq_email_parcial",
        "campos": [("email", 1)],
        "unico": True,
        "parcial": {"email": {"$type": "string"}},
    },
]
