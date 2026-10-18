"""Capa del CRUD PyQt6 que REUTILIZA las clases de conexión originales.

Los métodos crear_conexion(), ejecutar_consulta() y cerrar_conexion() viven en
conexion_SQLS_Flexi.py / conexion_PG_Flexi.py, igual que en el trabajo inicial.
Aquí solo se adapta la respuesta JSON al formato que consume la interfaz V7.
"""
from __future__ import annotations
import json

from esquema_flexi import TABLAS
from configuracion_local import leer_configuracion


class ErrorDatos(Exception):
    pass


class BaseDatos:
    def __init__(self, motor: str, configuracion=None):
        if motor not in ('postgres', 'sqlserver'):
            raise ValueError('Selecciona PostgreSQL o SQL Server.')
        self.motor = motor
        self.configuracion = configuracion
        self.conexion_original = None
        self.conn = None  # Compatibilidad con el código de V7.

    @property
    def placeholder(self):
        return '%s' if self.motor == 'postgres' else '?'

    def conectar(self):
        if self.conn is not None:
            return
        config = self.configuracion if self.configuracion is not None else leer_configuracion()
        if self.motor == 'postgres':
            from conexion_PG_Flexi import ConexionPostgresql
            conexion = ConexionPostgresql(configuracion=config)
        else:
            from conexion_SQLS_Flexi import ConexionSQLServer
            conexion = ConexionSQLServer(configuracion=config)
        cnx = conexion.crear_conexion()
        if cnx is None:
            raise ErrorDatos(f'No se pudo conectar a {self.motor}: {conexion.ultimo_error}')
        self.conexion_original = conexion
        self.conn = cnx

    def _ejecutar_original(self, sql, params=()):
        self.conectar()
        try:
            # Ambas clases devuelven JSON (el código original usaba ese contrato).
            texto = self.conexion_original.ejecutar_consulta(sql, tuple(params))
            resultado = json.loads(texto)
            # Si el controlador reconectó tras un corte, conservar su conexión vigente.
            self.conn = self.conexion_original.CNX
            if not isinstance(resultado, dict) or not resultado.get('estado'):
                if isinstance(resultado, dict):
                    mensaje = resultado.get('error') or resultado.get('mensaje') or 'Error de base de datos.'
                else:
                    mensaje = 'La conexión devolvió un resultado inválido.'
                raise ErrorDatos(str(mensaje))
            return resultado
        except ErrorDatos:
            raise
        except (ValueError, TypeError, AttributeError, KeyError) as exc:
            raise ErrorDatos('La conexión original devolvió una respuesta inválida.') from exc

    def leer(self, sql, params=()):
        try:
            return self._ejecutar_original(sql, params).get('registros', [])
        except ErrorDatos as exc:
            raise ErrorDatos(f'Consulta fallida: {exc}') from exc

    def escribir(self, sql, params=()):
        try:
            return self._ejecutar_original(sql, params).get('filas_afectadas', 0)
        except ErrorDatos as exc:
            raise ErrorDatos(f'No se pudo guardar la operación: {exc}') from exc

    def validar_tabla(self, nombre):
        if nombre not in TABLAS:
            raise ErrorDatos('Tabla no reconocida.')
        return TABLAS[nombre]

    def filas(self, nombre):
        t = self.validar_tabla(nombre)
        # Contraseñas nunca salen por el explorador de tablas.
        campos = ', '.join(c.nombre for c in t.visibles)
        return self.leer(f'SELECT {campos} FROM {t.nombre} ORDER BY {t.pk}')

    def uno(self, nombre, identificador):
        t = self.validar_tabla(nombre)
        campos = ', '.join(c.nombre for c in t.visibles)
        return next(iter(self.leer(
            f'SELECT {campos} FROM {t.nombre} WHERE {t.pk} = {self.placeholder}',
            (identificador,))), None)

    def insertar(self, nombre, datos):
        t = self.validar_tabla(nombre)
        validos = {c.nombre for c in t.modificables}
        if not datos or not set(datos).issubset(validos):
            raise ErrorDatos('Datos o columnas inválidos.')
        cols = list(datos)
        marcas = ', '.join([self.placeholder] * len(cols))
        return self.escribir(f'INSERT INTO {t.nombre} ({", ".join(cols)}) VALUES ({marcas})',
                             [datos[k] for k in cols])

    def actualizar(self, nombre, pk, datos):
        t = self.validar_tabla(nombre)
        validos = {c.nombre for c in t.modificables}
        if not datos or not set(datos).issubset(validos):
            raise ErrorDatos('Datos o columnas inválidos.')
        asignaciones = ', '.join(f'{c} = {self.placeholder}' for c in datos)
        return self.escribir(f'UPDATE {t.nombre} SET {asignaciones} WHERE {t.pk} = {self.placeholder}',
                             [*datos.values(), pk])

    def eliminar(self, nombre, pk):
        t = self.validar_tabla(nombre)
        return self.escribir(f'DELETE FROM {t.nombre} WHERE {t.pk} = {self.placeholder}', (pk,))

    def ligados(self, tabla_origen, campo_fk, valor):
        """Solo permite filtrar campos FK declarados por el esquema."""
        t = self.validar_tabla(tabla_origen)
        if not any(c.nombre == campo_fk and c.fk for c in t.campos):
            raise ErrorDatos('Liga no registrada.')
        campos = ', '.join(c.nombre for c in t.visibles)
        return self.leer(f'SELECT {campos} FROM {t.nombre} WHERE {campo_fk} = {self.placeholder} ORDER BY {t.pk}',
                         (valor,))

    def cerrar(self):
        if self.conexion_original is not None:
            try:
                self.conexion_original.cerrar_conexion()
            finally:
                self.conexion_original = None
                self.conn = None
        else:
            self.conn = None


def etiqueta_registro(tabla, row):
    candidatos = {
        'Tipo_Usuario': ('nombre_rol',), 'Categoria': ('nombre_categoria',),
        'Marca': ('nombre_marca',), 'Linea_Estilo': ('descripcion_estilo',),
        'Estatus_Producto': ('nombre_estatus',), 'Talla': ('numero_talla', 'clasificacion_talla'),
        'Forma_Pago': ('descripcion_pago',), 'Producto': ('codigo', 'nombre_modelo'),
        'Usuario': ('nombre', 'apellido_paterno'), 'Inventario': ('ubicacion_estante_bodega',),
        'Venta': ('fecha_venta', 'monto_total'), 'Detalle_Venta': ('cantidad_vendida', 'subtotal_linea'),
    }
    return ' · '.join(str(row.get(k)) for k in candidatos.get(tabla, ()) if row.get(k) is not None)
