"""Crea las colecciones definidas en los esquemas."""

import json
import sys

from pymongo.errors import PyMongoError
from pymongo.operations import SearchIndexModel

from app.schemas import COLECCIONES


def _json_canonico(definicion: dict) -> str:
    """Serializa una definición para comparar índices sin depender del orden."""
    return json.dumps(definicion, sort_keys=True, ensure_ascii=False)


def _crear_indices(coleccion, definiciones: list[dict]) -> tuple[int, int]:
    """Crea los índices declarados y devuelve cuántos se crearon y fallaron."""
    creados = 0
    fallidos = 0

    for indice in definiciones:
        opciones = {}
        if "nombre" in indice:
            opciones["name"] = indice["nombre"]
        if "unico" in indice:
            opciones["unique"] = indice["unico"]
        if "parcial" in indice:
            opciones["partialFilterExpression"] = indice["parcial"]
        if "pesos" in indice:
            opciones["weights"] = indice["pesos"]
        if "idioma_por_defecto" in indice:
            opciones["default_language"] = indice["idioma_por_defecto"]

        try:
            coleccion.create_index(indice["campos"], **opciones)
            creados += 1
        except PyMongoError as error:
            fallidos += 1
            print(
                f"✘ Índice {indice.get('nombre', '(sin nombre)')} "
                f"en {coleccion.name}: no se pudo crear "
                f"({type(error).__name__}). Comprueba si existe con otra definición."
            )

    return creados, fallidos


def _crear_indices_vectoriales(db) -> tuple[int, int, int]:
    """Solicita los índices vectoriales declarados en los esquemas."""
    creados = 0
    ya_existian = 0
    fallidos = 0

    for esquema in COLECCIONES:
        indice = getattr(esquema, "INDICE_VECTORIAL", None)
        if indice is None:
            continue

        nombre = indice["nombre"]
        definicion = indice["definicion"]
        coleccion = db[esquema.NOMBRE]

        try:
            existentes = list(coleccion.list_search_indexes())
        except PyMongoError as error:
            fallidos += 1
            print(
                f"✘ {esquema.NOMBRE}: no se pudieron consultar los índices "
                f"vectoriales ({type(error).__name__})."
            )
            print(
                "  Definición para crear manualmente en Atlas Search "
                "(Create Search Index → Vector Search):"
            )
            print(json.dumps(definicion, indent=2, ensure_ascii=False))
            continue

        existente = next(
            (elemento for elemento in existentes if elemento.get("name") == nombre),
            None,
        )
        if existente is not None:
            definicion_existente = existente.get(
                "latestDefinition", existente.get("definition")
            )
            if (
                definicion_existente is not None
                and _json_canonico(definicion_existente)
                == _json_canonico(definicion)
            ):
                ya_existian += 1
                print(f"• {esquema.NOMBRE}: índice vectorial ya existía")
            else:
                fallidos += 1
                print(
                    f"✘ {esquema.NOMBRE}: el índice vectorial '{nombre}' ya existe "
                    "con una definición distinta. No se modificó ni se eliminó."
                )
            continue

        try:
            modelo = SearchIndexModel(
                definition=definicion,
                name=nombre,
                type="vectorSearch",
            )
            coleccion.create_search_index(modelo)
            creados += 1
            print(
                f"✔ {esquema.NOMBRE}: índice vectorial {nombre} solicitado "
                "(puede tardar un minuto en estar listo)"
            )
        except PyMongoError as error:
            fallidos += 1
            print(
                f"✘ {esquema.NOMBRE}: no se pudo crear el índice vectorial "
                f"({type(error).__name__})."
            )
            print(
                "  Definición para crear manualmente en Atlas Search "
                "(Create Search Index → Vector Search):"
            )
            print(json.dumps(definicion, indent=2, ensure_ascii=False))

    return creados, ya_existian, fallidos


def main() -> int:
    """Inicializa todas las colecciones y resume los resultados."""
    try:
        from app.services.db_service import get_db

        db = get_db()
    except Exception as error:
        print(
            f"No se pudo acceder a la base de datos ({type(error).__name__}). "
            "Revisa el archivo .env y la conexión con MongoDB."
        )
        return 1

    try:
        existentes = set(db.list_collection_names())
    except Exception as error:
        print(
            f"No se pudieron consultar las colecciones ({type(error).__name__}). "
            "Revisa la URI, las credenciales y el acceso de red a MongoDB Atlas."
        )
        return 1
    creadas = 0
    ya_existian = 0
    fallidas = 0

    for esquema in COLECCIONES:
        nombre = esquema.NOMBRE
        estaba_creada = nombre in existentes

        try:
            reglas = esquema.REGLAS
            if not estaba_creada:
                opciones = {}
                if reglas is not None:
                    opciones = {
                        "validator": {"$jsonSchema": reglas},
                        "validationLevel": "strict",
                        "validationAction": "error",
                    }
                db.create_collection(nombre, **opciones)
            elif reglas is not None:
                db.command(
                    "collMod",
                    nombre,
                    validator={"$jsonSchema": reglas},
                    validationLevel="strict",
                    validationAction="error",
                )

            cantidad_indices, indices_fallidos = _crear_indices(
                db[nombre], esquema.INDICES
            )
            if estaba_creada:
                ya_existian += 1
                print(
                    f"• {nombre}: ya existía "
                    f"({cantidad_indices} índices, {indices_fallidos} fallidos)"
                )
            else:
                creadas += 1
                print(
                    f"✔ {nombre}: creada "
                    f"({cantidad_indices} índices, {indices_fallidos} fallidos)"
                )
            if indices_fallidos:
                fallidas += 1
        except Exception as error:
            fallidas += 1
            print(f"✘ {nombre}: falló ({type(error).__name__})")

    vectoriales_creados, vectoriales_existentes, vectoriales_fallidos = (
        _crear_indices_vectoriales(db)
    )
    fallidas += vectoriales_fallidos

    print(
        "\nResumen: "
        f"{creadas} colecciones creadas, {ya_existian} ya existían; "
        f"{vectoriales_creados} índices vectoriales solicitados, "
        f"{vectoriales_existentes} ya existían, {fallidas} fallos."
    )
    return 1 if fallidas else 0


if __name__ == "__main__":
    sys.exit(main())
