# Flexi Studio V8

Proyecto académico de aplicación de escritorio para administrar datos de una zapatería mediante **Python**, **PyQt6** y bases de datos **SQL Server** o **PostgreSQL**.

## Funcionalidades

- Inicio de sesión y permisos según el tipo de usuario.
- Consulta, alta, modificación y eliminación de registros (CRUD), sujetos a permisos y relaciones.
- Administración de catálogos e inventario.
- Exportación de resultados a Excel.
- Configuración de conexión a SQL Server o PostgreSQL.

## Requisitos

- Windows y Python 3 de 64 bits.
- Un servidor SQL Server o PostgreSQL accesible.
- Dependencias incluidas en `requirements.txt`.

## Instalación desde el código fuente

1. Descargar o clonar este repositorio.
2. Abrir una terminal en la carpeta que contiene `main.py`.
3. Crear y activar un entorno virtual (opcional, recomendado):

   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   ```

4. Instalar las dependencias:

   ```powershell
   py -m pip install -r requirements.txt
   ```

5. Preparar **una** base de datos de prueba usando los scripts en `FLEXI Base de Datos/`:
   - **SQL Server:** ejecutar `FlexiZamora_SQL_Server.sql` desde SQL Server Management Studio; crea la base `FlexiZamora`.
   - **PostgreSQL:** crear primero una base vacía (por ejemplo, `FlexiZamoraPG`) y ejecutar `FlexiZamora_PostgreSQL.sql` dentro de ella mediante pgAdmin.

6. Iniciar la aplicación y configurar la conexión:

   ```powershell
   py main.py
   ```

7. Para activar la cuenta administrativa incluida como ejemplo en los scripts SQL, después de configurar la conexión y con permisos en la base de datos, ejecutar **uno** de los siguientes comandos:

   ```powershell
   py configurar_admin.py --motor sqlserver
   # o
   py configurar_admin.py --motor postgres
   ```

   El asistente solicitará el correo del administrador existente y una contraseña nueva de al menos 12 caracteres. Los marcadores de contraseña incluidos en los scripts SQL no permiten iniciar sesión directamente.

## Guía completa

Consulta [`LEEME_PRIMERO.txt`](LEEME_PRIMERO.txt) para las instrucciones detalladas de instalación, configuración, uso y solución de problemas.

## Seguridad

- **No subir** archivos `.env`, `conexiones.json` ni contraseñas reales.
- La configuración local de conexiones se guarda fuera de la carpeta del proyecto, en el perfil del usuario.
- Los registros de demostración de los scripts SQL deben revisarse antes de publicar el repositorio para asegurar que no contengan datos personales reales.

## Instalador de Windows

Los archivos `CREAR_INSTALADOR.bat`, `FlexiStudio.spec` y `FlexiStudio_Instalador.iss` permiten compilar un instalador en Windows usando PyInstaller e Inno Setup 6. El ejecutable `.exe` no es necesario para revisar el código fuente ni para instalar las dependencias con `requirements.txt`.
