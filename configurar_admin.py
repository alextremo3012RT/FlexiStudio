"""Activación inicial segura: ejecutar localmente con acceso a la BD.

No utiliza las contraseñas de ejemplo del script SQL.
Requiere confirmación explícita y acceso administrativo real a la conexión.
"""
import argparse
import getpass
from base_datos import BaseDatos
from seguridad import generar_hash


def configurar(db, correo, clave, confirmar, *, force=False):
    if clave != confirmar:
        raise ValueError('Las contraseñas no coinciden.')
    cuentas = db.leer(
        f"SELECT u.id_usuario, u.contrasena FROM Usuario u "
        f"JOIN Tipo_Usuario t ON t.id_tipo_usuario=u.id_tipo_usuario "
        f"WHERE LOWER(t.nombre_rol)='administrador' "
        f"AND LOWER(u.correo_electronico)=LOWER({db.placeholder})", (correo,))
    if len(cuentas) != 1:
        raise ValueError('No existe exactamente un administrador con ese correo.')
    cuenta = cuentas[0]
    if str(cuenta['contrasena']).startswith('pbkdf2_sha256$') and not force:
        raise ValueError('Ya tiene una contraseña configurada. El cambio requiere --restablecer.')
    hash_ = generar_hash(clave)
    afectados = db.escribir(f'UPDATE Usuario SET contrasena={db.placeholder} '
                           f'WHERE id_usuario={db.placeholder}', (hash_, cuenta['id_usuario']))
    return afectados


def main():
    parser = argparse.ArgumentParser(description='Activar una cuenta Administrador Flexi')
    parser.add_argument('--motor', choices=['postgres', 'sqlserver'], required=True)
    parser.add_argument('--restablecer', action='store_true',
                        help='Sobrescribe contraseña actual: SOLO desde un equipo con credenciales de BD autorizadas')
    args = parser.parse_args()
    db = BaseDatos(args.motor)
    try:
        db.conectar()
        print('ACTIVACIÓN LOCAL DE ADMINISTRADOR — FLEXI')
        print('Es necesario tener acceso a la configuración de base de datos de este equipo.')
        correo = input('Correo del administrador existente: ').strip()
        clave = getpass.getpass('Nueva contraseña (mínimo 12 caracteres): ')
        confirmar = getpass.getpass('Repite la contraseña: ')
        if configurar(db, correo, clave, confirmar, force=args.restablecer):
            print('Cuenta activada. Ya puedes iniciar sesión desde la aplicación PyQt6.')
    except Exception as exc:
        print(f'No se pudo completar: {exc}')
        raise SystemExit(1)
    finally:
        db.cerrar()

if __name__ == '__main__':
    main()
