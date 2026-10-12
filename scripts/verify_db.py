"""Muestra el estado de reglas e índices de las colecciones configuradas."""

import sys

from pymongo.errors import PyMongoError

from app.schemas import COLECCIONES


def main() -> int:
    """Consulta reglas, índices normales, documentos e índices vectoriales."""
    try:
        from app.services.db_service import get_db

        db = get_db()
        nombres_existentes = set(db.list_collection_names())
    except Exception as error:
        print(
            f"No se pudo consultar la base de datos ({type(error).__name__}). "
            "Revisa la configuración de MongoDB y la conexión."
        )
        return 1

    colecciones_con_reglas = 0
    total_indices = 0
    fallidos = 0
    print(f"Estado de la base de datos: {db.name}\n")

    for esquema in COLECCIONES:
        nombre = esquema.NOMBRE
        if nombre not in nombres_existentes:
            fallidos += 1
            print(f"✘ {nombre}: la colección no existe")
            continue

        coleccion = db[nombre]
        try:
            opciones = coleccion.options()
            tiene_reglas = "$jsonSchema" in opciones.get("validator", {})
            if tiene_reglas:
                colecciones_con_reglas += 1

            indices = [
                indice["name"]
                for indice in coleccion.list_indexes()
                if indice["name"] != "_id_"
            ]
            indices_faltantes = {
                indice["nombre"] for indice in esquema.INDICES
            } - set(indices)
            cantidad_documentos = coleccion.count_documents({})
            total_indices += len(indices)

            print(
                f"{nombre}: reglas={'sí' if tiene_reglas else 'no'}; "
                f"índices normales={', '.join(indices) if indices else '(ninguno)'}; "
                f"documentos={cantidad_documentos}"
            )
            if not tiene_reglas:
                fallidos += 1
                print(f"  ✘ Falta la regla de validación para {nombre}")
            if indices_faltantes:
                fallidos += 1
                print(
                    "  ✘ Faltan índices normales: "
                    + ", ".join(sorted(indices_faltantes))
                )
        except PyMongoError as error:
            fallidos += 1
            print(f"✘ {nombre}: no se pudo verificar ({type(error).__name__})")
            continue

        indice_vectorial_esperado = getattr(esquema, "INDICE_VECTORIAL", None)
        if indice_vectorial_esperado is not None:
            try:
                indices_vectoriales = list(coleccion.list_search_indexes())
                for indice in indices_vectoriales:
                    print(
                        f"  Índice vectorial: {indice.get('name', '(sin nombre)')}; "
                        f"colección={nombre}; "
                        f"estado={indice.get('status', 'desconocido')}; "
                        f"consultable={indice.get('queryable', 'desconocido')}"
                    )
                esperado = next(
                    (
                        indice
                        for indice in indices_vectoriales
                        if indice.get("name") == indice_vectorial_esperado["nombre"]
                    ),
                    None,
                )
                if esperado is None:
                    fallidos += 1
                    print(
                        f"  ✘ No aparece el índice vectorial esperado "
                        f"{indice_vectorial_esperado['nombre']}"
                    )
                elif (
                    esperado.get("status") != "READY"
                    or esperado.get("queryable") is not True
                ):
                    fallidos += 1
                    print("  • El índice vectorial aún no está listo para consultar")
            except PyMongoError as error:
                fallidos += 1
                print(
                    f"  ✘ No se pudo consultar el índice vectorial de {nombre} "
                    f"({type(error).__name__})"
                )

    print(
        "\nResumen: "
        f"{colecciones_con_reglas}/{len(COLECCIONES)} colecciones con reglas; "
        f"{total_indices} índices normales encontrados "
        "(sin contar el índice automático _id_)."
    )
    return 1 if fallidos else 0


if __name__ == "__main__":
    sys.exit(main())
