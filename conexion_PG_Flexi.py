"""Conexión PostgreSQL del proyecto original, adaptada para Flexi Studio V8.

Se mantienen los métodos y atributos originales, sin contraseña fija.
La configuración proviene del perfil del usuario en Windows.
"""
import json
import decimal
from datetime import date, datetime
from configuracion_local import leer_configuracion


def serializador_personalizado(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(f'Tipo {type(obj)} no es serializable en JSON')


def _proteger_error(error, secreto):
    mensaje = str(error)
    return mensaje.replace(str(secreto), '[OCULTO]') if secreto else mensaje


class ConexionPostgresql:
    def __init__(self, configuracion=None):
        config = configuracion if configuracion is not None else leer_configuracion()
        self.HOST = config.get('PG_HOST', 'localhost')
        self.PORT = config.get('PG_PORT', '5432')
        self.DATABASE_NAME = config.get('PG_DATABASE', 'FlexiZamoraPG')
        self.USER = config.get('PG_USER', 'postgres')
        self.PASSWORD = config.get('PG_PASSWORD', '')
        self.CNX = None
        self.CURSOR = None
        self.ultimo_error = ''

    def crear_conexion(self):
        try:
            import psycopg2
            self.CNX = psycopg2.connect(
                host=self.HOST, port=self.PORT, dbname=self.DATABASE_NAME,
                user=self.USER, password=self.PASSWORD, connect_timeout=7,
            )
            self.CURSOR = self.CNX.cursor()
            self.ultimo_error = ''
            return self.CNX
        except Exception as exc:
            self.ultimo_error = _proteger_error(exc, self.PASSWORD)
            if self.CNX is not None:
                try: self.CNX.close()
                except Exception: pass
            self.CNX = None
            self.CURSOR = None
            return None

    def ejecutar_consulta(self, sql, parametros=None):
        """Método original: ejecuta SQL parametrizado y devuelve una respuesta JSON."""
        try:
            if self.CNX is None or getattr(self.CNX, 'closed', False):
                if self.crear_conexion() is None:
                    return json.dumps({'estado': False, 'mensaje': self.ultimo_error}, ensure_ascii=False)
            if parametros is not None and len(parametros) > 0:
                self.CURSOR.execute(sql, tuple(parametros))
            else:
                self.CURSOR.execute(sql)
            tipo = sql.strip().split()[0].upper()
            if tipo == 'SELECT':
                columnas = [col[0] for col in self.CURSOR.description]
                registros = [dict(zip(columnas, fila)) for fila in self.CURSOR.fetchall()]
                return json.dumps({'estado': True, 'Tipo': 'SELECT', 'registros': registros},
                                  ensure_ascii=False, default=serializador_personalizado)
            filas_afectadas = self.CURSOR.rowcount
            self.CNX.commit()
            return json.dumps({'estado': True, 'Tipo': tipo,
                               'filas_afectadas': filas_afectadas,
                               'mensaje': f'Operación {tipo} ejecutada exitosamente.'},
                              ensure_ascii=False)
        except Exception as exc:
            if self.CNX is not None:
                try: self.CNX.rollback()
                except Exception: pass
            return json.dumps({'estado': False, 'mensaje': 'Error en la consulta SQL',
                               'error': _proteger_error(exc, self.PASSWORD)}, ensure_ascii=False)

    def cerrar_conexion(self):
        try:
            if self.CURSOR is not None:
                self.CURSOR.close()
                self.CURSOR = None
            if self.CNX is not None:
                self.CNX.close()
                self.CNX = None
            return True
        except Exception as exc:
            self.ultimo_error = _proteger_error(exc, self.PASSWORD)
            return False
