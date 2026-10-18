"""Contraseñas con PBKDF2, permisos centralizados y usuarios en tabla Usuario existente."""
from __future__ import annotations
import hashlib
import hmac
import os
import re
import time
from dataclasses import dataclass
from base_datos import ErrorDatos

ITERACIONES = 600_000
PREFIJO = 'pbkdf2_sha256'


def generar_hash(contrasena: str) -> str:
    if len(contrasena) < 12:
        raise ValueError('La contraseña debe tener por lo menos 12 caracteres.')
    sal = os.urandom(16)
    digest = hashlib.pbkdf2_hmac('sha256', contrasena.encode('utf-8'), sal, ITERACIONES)
    return f'{PREFIJO}${ITERACIONES}${sal.hex()}${digest.hex()}'


def comprobar_hash(contrasena: str, almacenado: str) -> bool:
    try:
        algoritmo, iteraciones, sal, digest = almacenado.split('$')
        if algoritmo != PREFIJO or not (200_000 <= int(iteraciones) <= 1_000_000):
            return False
        calculado = hashlib.pbkdf2_hmac('sha256', contrasena.encode('utf-8'),
                                        bytes.fromhex(sal), int(iteraciones))
        return hmac.compare_digest(calculado, bytes.fromhex(digest))
    except (AttributeError, TypeError, ValueError):
        # Los 'hash_admin123' precargados en los scripts NO son hashes reales.
        return False


@dataclass(frozen=True)
class Sesion:
    id_usuario: int
    nombre: str
    correo: str
    rol: str
    @property
    def es_admin(self):
        return self.rol.strip().casefold() == 'administrador'
    @property
    def etiqueta_rol(self):
        return 'ADMINISTRADOR' if self.es_admin else 'TRABAJADOR'


class AccesoDenegado(PermissionError):
    pass


class Autenticacion:
    def __init__(self, db):
        self.db = db
        self.fallos = 0
        self.bloqueado_hasta = 0.0

    def autenticar(self, correo, contrasena):
        if time.monotonic() < self.bloqueado_hasta:
            raise AccesoDenegado('Demasiados intentos. Espera 30 segundos.')
        sql = (f'SELECT u.id_usuario, u.nombre, u.apellido_paterno, u.correo_electronico, '
               f'u.contrasena, u.estatus_activo, t.nombre_rol '
               f'FROM Usuario u JOIN Tipo_Usuario t ON u.id_tipo_usuario=t.id_tipo_usuario '
               f'WHERE LOWER(u.correo_electronico) = LOWER({self.db.placeholder})')
        datos = self.db.leer(sql, (correo.strip(),))
        row = datos[0] if len(datos) == 1 else None
        if row and bool(row['estatus_activo']) and comprobar_hash(contrasena, row.get('contrasena')):
            self.fallos = 0
            self.bloqueado_hasta = 0
            return Sesion(int(row['id_usuario']),
                          f"{row['nombre']} {row['apellido_paterno']}",
                          row['correo_electronico'], row['nombre_rol'])
        self.fallos += 1
        if self.fallos >= 5:
            self.bloqueado_hasta = time.monotonic() + 30
            self.fallos = 0
        raise AccesoDenegado('Correo o contraseña incorrectos, o cuenta inactiva.')


# Permisos se validan también en el servicio, no solamente ocultando botones en la UI.
def exigir(sesion: Sesion, accion: str, tabla: str | None = None):
    if sesion is None:
        raise AccesoDenegado('Debes iniciar sesión.')
    if sesion.es_admin:
        return
    if accion != 'consultar':
        raise AccesoDenegado('Solo un administrador puede hacer esta operación.')
    if tabla not in ('Tipo_Usuario','Categoria','Marca','Linea_Estilo',
                     'Estatus_Producto','Talla','Forma_Pago','Producto','Inventario'):
        raise AccesoDenegado('No tienes permiso para consultar esta tabla.')


class Servicio:
    def __init__(self, db, sesion):
        self.db, self.sesion = db, sesion

    def consultar(self, tabla):
        exigir(self.sesion, 'consultar', tabla)
        return self.db.filas(tabla)

    def insertar(self, tabla, datos):
        exigir(self.sesion, 'insertar', tabla)
        from esquema_flexi import TABLAS
        if not TABLAS[tabla].editable:
            raise AccesoDenegado('Esta tabla es solo de consulta.')
        return self.db.insertar(tabla, datos)

    def actualizar(self, tabla, pk, datos):
        exigir(self.sesion, 'actualizar', tabla)
        from esquema_flexi import TABLAS
        if not TABLAS[tabla].editable:
            raise AccesoDenegado('Esta tabla es solo de consulta.')
        if tabla == 'Tipo_Usuario' and int(pk) == 1:
            raise AccesoDenegado('El rol Administrador del sistema está protegido.')
        return self.db.actualizar(tabla, pk, datos)

    def eliminar(self, tabla, pk):
        exigir(self.sesion, 'eliminar', tabla)
        from esquema_flexi import TABLAS
        if not TABLAS[tabla].editable:
            raise AccesoDenegado('Esta tabla es solo de consulta.')
        if tabla == 'Tipo_Usuario' and int(pk) == 1:
            raise AccesoDenegado('El rol Administrador del sistema está protegido.')
        return self.db.eliminar(tabla, pk)

    def usuarios(self):
        exigir(self.sesion, 'usuarios')
        return self.db.filas('Usuario')

    def crear_usuario(self, datos, contrasena):
        exigir(self.sesion, 'usuarios')
        hash_ = generar_hash(contrasena)
        correo = datos['correo_electronico'].strip().lower()
        self._comprobar_correo(correo)
        obligatorios = ('id_tipo_usuario', 'nombre', 'apellido_paterno', 'correo_electronico')
        if any(not str(datos.get(c, '')).strip() for c in obligatorios):
            raise ValueError('Nombre, apellido, correo y rol son obligatorios.')
        cols = [*obligatorios, 'apellido_materno', 'telefono', 'estatus_activo', 'contrasena']
        valores = {**datos, 'correo_electronico': correo, 'contrasena': hash_}
        return self._insertar_usuario(cols, valores)

    def _insertar_usuario(self, cols, datos):
        marcadores = ', '.join([self.db.placeholder] * len(cols))
        return self.db.escribir(f'INSERT INTO Usuario ({", ".join(cols)}) VALUES ({marcadores})',
                                [datos.get(c) for c in cols])

    def _comprobar_correo(self, correo, excepto=None):
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', correo):
            raise ValueError('Introduce un correo válido.')
        q = f'SELECT id_usuario FROM Usuario WHERE LOWER(correo_electronico) = LOWER({self.db.placeholder})'
        found = self.db.leer(q, (correo,))
        if any(int(r['id_usuario']) != excepto for r in found):
            raise ValueError('Ya existe una cuenta con ese correo.')

    def editar_usuario(self, user_id, datos):
        exigir(self.sesion, 'usuarios')
        if not datos:
            return 0
        if 'correo_electronico' in datos:
            correo = datos['correo_electronico'].strip().lower()
            self._comprobar_correo(correo, excepto=int(user_id))
            datos['correo_electronico'] = correo
        campos = {'nombre','apellido_paterno','apellido_materno','telefono',
                  'correo_electronico','id_tipo_usuario','estatus_activo'}
        if not set(datos) <= campos:
            raise ValueError('Campo de usuario no permitido.')
        if int(user_id) == self.sesion.id_usuario:
            if datos.get('estatus_activo') is False:
                raise ValueError('No puedes desactivar tu propia cuenta.')
            if 'id_tipo_usuario' in datos:
                actual = self.db.leer(f'SELECT id_tipo_usuario FROM Usuario WHERE id_usuario={self.db.placeholder}', (user_id,))
                if actual and int(datos['id_tipo_usuario']) != int(actual[0]['id_tipo_usuario']):
                    raise ValueError('No puedes cambiar tu propio rol.')
        cambio = ', '.join(f'{c}={self.db.placeholder}' for c in datos)
        return self.db.escribir(f'UPDATE Usuario SET {cambio} WHERE id_usuario={self.db.placeholder}',
                                (*datos.values(), user_id))

    def cambiar_password(self, user_id, nueva_password):
        exigir(self.sesion, 'usuarios')
        hash_ = generar_hash(nueva_password)
        return self.db.escribir(f'UPDATE Usuario SET contrasena={self.db.placeholder} '
                                f'WHERE id_usuario={self.db.placeholder}', (hash_, user_id))
