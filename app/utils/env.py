"""Carga y valida las variables de entorno del proyecto."""

import os

from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

if not MONGODB_URI:
    raise ValueError("Falta la variable de entorno MONGODB_URI en el archivo .env.")

if not MONGODB_DB_NAME:
    raise ValueError("Falta la variable de entorno MONGODB_DB_NAME en el archivo .env.")
