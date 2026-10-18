"""Configuración por usuario, fuera de la carpeta del programa.

En Windows se guarda en AppData/Roaming/FlexiStudio/conexiones.json.
En modo desarrollo se puede leer el .env de V6 como respaldo.
"""
from __future__ import annotations
import os
import json
import sys
import tempfile
from pathlib import Path
from dotenv import dotenv_values

CAMPOS = {
    'FLEXI_DB': 'postgres',
    'PG_HOST': 'localhost',
    'PG_PORT': '5432',
    'PG_DATABASE': 'FlexiZamoraPG',
    'PG_USER': 'postgres',
    'PG_PASSWORD': '',
    'MSSQL_SERVER': 'localhost',
    'MSSQL_DATABASE': 'FlexiZamora',
    'MSSQL_USER': '',
    'MSSQL_PASSWORD': '',
    'MSSQL_TRUST_CERT': 'yes',
}


def ruta_configuracion() -> Path:
    perfil = os.environ.get('APPDATA')
    if perfil:
        return Path(perfil) / 'FlexiStudio' / 'conexiones.json'
    return Path.home() / '.flexistudio' / 'conexiones.json'


def leer_configuracion() -> dict[str, str]:
    ruta = ruta_configuracion()
    if ruta.is_file():
        with ruta.open(encoding='utf-8') as archivo:
            leidos = json.load(archivo)
        if not isinstance(leidos, dict):
            raise ValueError('El archivo de conexiones tiene un formato incorrecto.')
    elif not getattr(sys, 'frozen', False) and Path(__file__).with_name('.env').is_file():
        # Compatibilidad con el entorno V6 de desarrollo; no incluido en el instalador.
        leidos = dotenv_values(Path(__file__).with_name('.env'), interpolate=False)
    else:
        leidos = {}
    datos = CAMPOS.copy()
    datos.update({k: str(v) for k, v in leidos.items() if k in CAMPOS and v is not None})
    return datos


def guardar_configuracion(datos: dict[str, str]) -> Path:
    if set(datos) - set(CAMPOS):
        raise ValueError('La configuración contiene campos desconocidos.')
    valores = CAMPOS | {k: str(v) for k, v in datos.items()}
    if valores['FLEXI_DB'] not in ('postgres', 'sqlserver'):
        raise ValueError('Motor de base de datos no reconocido.')
    if not valores['PG_PORT'].isdigit() or not 1 <= int(valores['PG_PORT']) <= 65535:
        raise ValueError('Puerto de PostgreSQL inválido.')
    ruta = ruta_configuracion()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    contenido = json.dumps(valores, ensure_ascii=False, indent=2) + '\n'
    temporal = None
    try:
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=ruta.parent,
                                         prefix='config_', suffix='.tmp', delete=False) as archivo:
            temporal = Path(archivo.name)
            archivo.write(contenido)
        os.chmod(temporal, 0o600)
        os.replace(temporal, ruta)
    finally:
        if temporal and temporal.exists():
            temporal.unlink()
    return ruta


def importar_configuracion(origen: Path) -> dict[str, str]:
    if not origen.is_file():
        raise FileNotFoundError('No se encontró el archivo .env elegido.')
    valores = dotenv_values(origen, interpolate=False)
    datos = leer_configuracion()
    datos.update({k: str(v) for k, v in valores.items() if k in CAMPOS and v is not None})
    return datos
