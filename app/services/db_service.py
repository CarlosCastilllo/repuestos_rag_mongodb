"""Funciones compartidas para conectarse a MongoDB."""

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.utils.env import MONGODB_DB_NAME, MONGODB_URI

_client: MongoClient | None = None


def get_client() -> MongoClient:
    """Devuelve el cliente de MongoDB reutilizable."""
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    return _client


def get_db():
    """Devuelve la base de datos configurada."""
    return get_client()[MONGODB_DB_NAME]


def ping() -> bool:
    """Comprueba si el servidor de MongoDB responde."""
    try:
        get_client().admin.command("ping")
        return True
    except PyMongoError:
        return False
