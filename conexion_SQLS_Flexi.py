"""Conexión SQL Server del proyecto original, adaptada para Flexi Studio V8.

Conserva los métodos educativos crear_conexion(), ejecutar_consulta() y
cerrar_conexion(), además de los atributos CNX y CURSOR.
La única fuente de credenciales es la configuración local de Flexi Studio;
no se carga .env automáticamente ni se imprime información sensible.
"""
import json
from configuracion_local import leer_configuracion


def _proteger_error(error, secretos):
    mensaje = str(error)
    for secreto in secretos:
        if secreto:
            mensaje = mensaje.replace(str(secreto), '[OCULTO]')
    return mensaje


class ConexionSQLServer:
    def __init__(self, configuracion=None):
        config = configuracion if configuracion is not None else leer_configuracion()
        self.SERVER_NAME = config.get('MSSQL_SERVER', config.get('SERVER_NAME', 'localhost'))
        self.DATABASE_NAME = config.get('MSSQL_DATABASE', config.get('DATABASE_NAME', 'FlexiZamora'))
        self.USER = config.get('MSSQL_USER', config.get('USER', ''))
        self.PASSWORD = config.get('MSSQL_PASSWORD', config.get('PASSWORD', ''))
        self.TRUST_CERT = config.get('MSSQL_TRUST_CERT', 'yes')
        self.CNX = None
        self.CURSOR = None
        self.ultimo_error = ''

    def crear_conexion(self):
        try:
            if not self.USER or not self.PASSWORD:
                raise ValueError('Completa el usuario y contraseña de SQL Server en Configurar conexiones.')
            import mssql_python
            # Los valores van entre llaves para proteger caracteres como ; y }.
            def encerrar(valor):
                return '{' + str(valor).replace('}', '}}') + '}'
            cadena = ';'.join([
                f'Server={encerrar(self.SERVER_NAME)}',
                f'Database={encerrar(self.DATABASE_NAME)}',
                f'UID={encerrar(self.USER)}',
                f'PWD={encerrar(self.PASSWORD)}',
                'Encrypt=yes',
                f'TrustServerCertificate={self.TRUST_CERT}',
            ]) + ';'
            self.CNX = mssql_python.connect(cadena)
            self.CURSOR = self.CNX.cursor()
            self.ultimo_error = ''
            return self.CNX
        except Exception as exc:
            self.ultimo_error = _proteger_error(exc, (self.PASSWORD,))
            if self.CNX is not None:
                try: self.CNX.close()
                except Exception: pass
            self.CNX = None
            self.CURSOR = None
            return None

    def ejecutar_consulta(self, sql, parametros=None):
        """Método original: devuelve JSON con estado, registros o filas afectadas."""
        try:
            if self.CNX is None and self.crear_conexion() is None:
                return json.dumps({'estado': False, 'mensaje': self.ultimo_error}, ensure_ascii=False)
            if parametros is not None and len(parametros) > 0:
                self.CURSOR.execute(sql, tuple(parametros))
            else:
                self.CURSOR.execute(sql)
            tipo = sql.strip().split()[0].upper()
            if tipo == 'SELECT':
                columnas = [col[0] for col in self.CURSOR.description]
                registros = self.CURSOR.fetchall()
                resultados = [dict(zip(columnas, fila)) for fila in registros]
                return json.dumps({'estado': True, 'tipo': 'SELECT', 'registros': resultados},
                                  ensure_ascii=False, default=str)
            filas = self.CURSOR.rowcount
            self.CNX.commit()
            mensajes = {'INSERT': 'Registro insertado correctamente',
                        'UPDATE': 'Registro actualizado correctamente',
                        'DELETE': 'Registro eliminado correctamente'}
            return json.dumps({'estado': True, 'tipo': tipo,
                               'mensaje': mensajes.get(tipo, 'Consulta ejecutada correctamente'),
                               'filas_afectadas': filas}, ensure_ascii=False)
        except Exception as exc:
            if self.CNX is not None:
                try: self.CNX.rollback()
                except Exception: pass
            tipo_error = type(exc).__name__
            return json.dumps({'estado': False, 'tipo': tipo_error,
                               'mensaje': 'Error en la consulta SQL',
                               'error': _proteger_error(exc, (self.PASSWORD,))}, ensure_ascii=False)

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
            self.ultimo_error = _proteger_error(exc, (self.PASSWORD,))
            return False
