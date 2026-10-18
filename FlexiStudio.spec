# -*- mode: python ; coding: utf-8 -*-
# Compilar solo en Windows. Incluye recursos nativos del controlador mssql-python.
from pathlib import Path
import importlib.util
from PyInstaller.utils.hooks import collect_all

ROOT = Path(SPECPATH)
extra_datas, extra_binaries, extra_imports = [], [], []
for paquete in ('mssql_python', 'mssql_py_core'):
    if importlib.util.find_spec(paquete) is not None:
        datas, binaries, imports = collect_all(paquete)
        extra_datas.extend(datas)
        extra_binaries.extend(binaries)
        extra_imports.extend(imports)

a = Analysis(
    [str(ROOT / 'main.py')],
    pathex=[str(ROOT)],
    binaries=extra_binaries,
    datas=extra_datas,
    hiddenimports=['psycopg2', 'mssql_python', 'conexion_PG_Flexi', 'conexion_SQLS_Flexi'] + extra_imports,
    hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True, name='FlexiStudio',
    debug=False, bootloader_ignore_signals=False, strip=False,
    upx=False, console=False,
    icon=str(ROOT / 'assets' / 'flexi.ico'),
)
coll = COLLECT(
    exe, a.binaries, a.datas,
    strip=False, upx=False, name='FlexiStudio',
)
