"""Editor gráfico de conexiones de base de datos (sin credenciales embebidas)."""
from __future__ import annotations
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QFileDialog, QMessageBox, QTabWidget, QWidget,
)
from configuracion_local import (CAMPOS, leer_configuracion, guardar_configuracion,
                                importar_configuracion, ruta_configuracion)


class DialogoConexiones(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Flexi Studio  /  Configurar conexiones')
        self.setMinimumWidth(540)
        self.campos = {}
        self.datos = leer_configuracion()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        titulo = QLabel('CONFIGURAR BASES DE DATOS')
        titulo.setObjectName('sectionLabel')
        layout.addWidget(titulo)
        nota = QLabel('Las conexiones se guardan únicamente en tu perfil de Windows. '
                      'Las contraseñas de base de datos se almacenan localmente; no compartas tu archivo de configuración.')
        nota.setWordWrap(True)
        layout.addWidget(nota)
        form = QFormLayout()
        self.motor = QComboBox()
        self.motor.addItem('PostgreSQL', 'postgres')
        self.motor.addItem('SQL Server', 'sqlserver')
        form.addRow('Base predeterminada', self.motor)
        layout.addLayout(form)

        tabs = QTabWidget()
        pg = QWidget(); pgform = QFormLayout(pg)
        self._campo(pgform, 'PG_HOST', 'Servidor')
        self._campo(pgform, 'PG_PORT', 'Puerto')
        self._campo(pgform, 'PG_DATABASE', 'Base de datos')
        self._campo(pgform, 'PG_USER', 'Usuario SQL')
        self._campo(pgform, 'PG_PASSWORD', 'Contraseña SQL', secreto=True)
        tabs.addTab(pg, 'PostgreSQL')

        sql = QWidget(); sqlform = QFormLayout(sql)
        self._campo(sqlform, 'MSSQL_SERVER', 'Servidor / instancia')
        self._campo(sqlform, 'MSSQL_DATABASE', 'Base de datos')
        self._campo(sqlform, 'MSSQL_USER', 'Usuario SQL')
        self._campo(sqlform, 'MSSQL_PASSWORD', 'Contraseña SQL', secreto=True)
        self.trust = QComboBox()
        self.trust.addItem('Sí (servidor local / pruebas)', 'yes')
        self.trust.addItem('No (certificado verificado)', 'no')
        sqlform.addRow('Confiar en certificado', self.trust)
        tabs.addTab(sql, 'SQL Server')
        layout.addWidget(tabs)
        self._poner_datos(self.datos)

        fila = QHBoxLayout()
        bimportar = QPushButton('Importar .env de V6...')
        bimportar.clicked.connect(self._importar)
        fila.addWidget(bimportar)
        fila.addStretch()
        bpg = QPushButton('Probar PostgreSQL')
        bpg.clicked.connect(lambda: self._probar('postgres'))
        fila.addWidget(bpg)
        bsql = QPushButton('Probar SQL Server')
        bsql.clicked.connect(lambda: self._probar('sqlserver'))
        fila.addWidget(bsql)
        layout.addLayout(fila)
        fila2 = QHBoxLayout()
        fila2.addStretch()
        cancelar = QPushButton('Cancelar'); cancelar.clicked.connect(self.reject)
        guardar = QPushButton('Guardar conexiones'); guardar.setObjectName('primary')
        guardar.clicked.connect(self._guardar)
        fila2.addWidget(cancelar); fila2.addWidget(guardar)
        layout.addLayout(fila2)
        self.info = QLabel(f'Ubicación: {ruta_configuracion()}')
        self.info.setWordWrap(True)
        layout.addWidget(self.info)

    def _campo(self, form, key, titulo, secreto=False):
        campo = QLineEdit()
        if secreto:
            campo.setEchoMode(QLineEdit.EchoMode.Password)
            campo.setPlaceholderText('Dejar vacío para conservar la contraseña guardada')
        self.campos[key] = campo
        form.addRow(titulo, campo)

    def _poner_datos(self, datos):
        for key, campo in self.campos.items():
            if key.endswith('_PASSWORD'):
                campo.clear()
            else:
                campo.setText(datos.get(key, ''))
        idx = self.motor.findData(datos.get('FLEXI_DB', 'postgres'))
        self.motor.setCurrentIndex(max(idx,0))
        idx = self.trust.findData(datos.get('MSSQL_TRUST_CERT','yes'))
        self.trust.setCurrentIndex(max(idx,0))

    def _valores(self):
        valores = self.datos.copy()
        valores['FLEXI_DB'] = self.motor.currentData()
        valores['MSSQL_TRUST_CERT'] = self.trust.currentData()
        for key, campo in self.campos.items():
            valor = campo.text()
            if key.endswith('_PASSWORD') and not valor:
                continue
            valores[key] = valor.strip() if not key.endswith('_PASSWORD') else valor
        return valores

    def _importar(self):
        nombre, _ = QFileDialog.getOpenFileName(self, 'Importar configuración V6', '',
                                               'Archivos de configuración (*.env *.txt);;Todos los archivos (*)')
        if not nombre:
            return
        try:
            self.datos = importar_configuracion(Path(nombre))
            self._poner_datos(self.datos)
            QMessageBox.information(self, 'Importado',
                                    'Se cargaron los valores. Pulsa Guardar conexiones para conservarlos.')
        except Exception as exc:
            QMessageBox.critical(self, 'No se pudo importar', str(exc))

    def _probar(self, motor):
        try:
            # Permite probar los datos del formulario SIN guardarlos todavía.
            from base_datos import BaseDatos
            db = BaseDatos(motor, configuracion=self._valores())
            try:
                db.conectar()
                db.leer('SELECT 1 AS prueba')
            finally:
                db.cerrar()
            QMessageBox.information(self, 'Conexión correcta',
                                    f'Se logró conectar a {"PostgreSQL" if motor == "postgres" else "SQL Server"}.')
        except Exception as exc:
            QMessageBox.warning(self, 'No se pudo conectar', str(exc))

    def _guardar(self):
        try:
            ruta = guardar_configuracion(self._valores())
            self.datos = leer_configuracion()
            QMessageBox.information(self, 'Configuración guardada',
                                    f'Conexiones guardadas en:\n{ruta}')
            self.accept()
        except Exception as exc:
            QMessageBox.critical(self, 'Error de configuración', str(exc))
