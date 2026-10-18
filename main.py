"""Punto de entrada de Flexi Studio GUI."""
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox
from estilos import ESTILO
from interfaz_pyqt import InicioSesion, VentanaPrincipal
from configurar_conexiones import DialogoConexiones
from configuracion_local import ruta_configuracion


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Flexi Studio')
    app.setOrganizationName('Flexi Zamora')
    app.setStyle('Fusion')
    # Login y ventana principal no coexisten; evitamos un quit automático al aceptar login.
    app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(ESTILO)
    if '--configurar' in sys.argv:
        return 0 if DialogoConexiones().exec() == QDialog.DialogCode.Accepted else 1
    if not ruta_configuracion().exists():
        QMessageBox.information(None, 'Primer inicio de Flexi Studio',
            'Configura las conexiones a SQL Server y/o PostgreSQL.\n'
            'Puedes importar el archivo .env de tu versión anterior.')
        if DialogoConexiones().exec() != QDialog.DialogCode.Accepted:
            return 0
    while True:
        login = InicioSesion()
        if login.exec() != QDialog.DialogCode.Accepted:
            break
        panel = VentanaPrincipal(login.db, login.sesion)
        panel.show()
        app.exec()
        if not getattr(panel, '_cerrar_pedido', False):
            break
    return 0

if __name__ == '__main__':
    sys.exit(main())
