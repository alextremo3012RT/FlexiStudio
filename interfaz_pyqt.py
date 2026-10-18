"""Aplicación gráfica Flexi Studio, PyQt6. Interfaz red/graphite, roles y 12 tablas."""
from __future__ import annotations
import os
import sys
import time
import unicodedata
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSortFilterProxyModel, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QFrame, QLineEdit, QComboBox, QFormLayout,
    QTableView, QHeaderView, QMessageBox, QFileDialog, QScrollArea,
    QSpinBox, QDoubleSpinBox, QCheckBox, QDialogButtonBox, QTreeWidget,
    QTreeWidgetItem, QAbstractItemView, QStackedWidget, QSizePolicy,
    QSplitter, QStatusBar
)

from esquema_flexi import TABLAS, MAESTRAS, OPERATIVAS, ligas_de
from base_datos import BaseDatos, ErrorDatos, etiqueta_registro
from seguridad import (Autenticacion, AccesoDenegado, Servicio, exigir,
                       generar_hash)
from estilos import ESTILO, COLOR_ROJO, COLOR_ROJO_CLARO
from exportar_excel import exportar
from configuracion_local import leer_configuracion
from configurar_conexiones import DialogoConexiones


def etiqueta(txt, ident=None, clase=None, size=None):
    lab = QLabel(str(txt))
    if ident: lab.setObjectName(ident)
    if clase: lab.setProperty('class', clase)
    if size: lab.setMinimumHeight(size)
    lab.setWordWrap(True)
    return lab


def boton(texto, fn=None, tipo=None, minimo=None):
    b = QPushButton(texto)
    if tipo: b.setObjectName(tipo)
    if minimo: b.setMinimumWidth(minimo)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    if fn: b.clicked.connect(fn)
    return b


def superficie(vertical=True, nombre='surface', margen=20, espacio=12):
    f = QFrame()
    f.setObjectName(nombre)
    ly = QVBoxLayout(f) if vertical else QHBoxLayout(f)
    ly.setContentsMargins(margen, margen, margen, margen)
    ly.setSpacing(espacio)
    return f, ly


def aviso(parent, titulo, msg, error=False):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Critical if error else QMessageBox.Icon.Information)
    box.setWindowTitle(titulo)
    box.setText(str(msg))
    box.exec()


def confirmar(parent, pregunta, titulo='Confirmar acción'):
    resp = QMessageBox.question(parent, titulo, pregunta,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No)
    return resp == QMessageBox.StandardButton.Yes


def normalizar(valor):
    return ''.join(x for x in unicodedata.normalize('NFKD', str(valor or '').casefold())
                   if not unicodedata.combining(x))


class InicioSesion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = None
        self.sesion = None
        self._fallos = 0
        self._bloqueado_hasta = 0.0
        self.setWindowTitle('FLEXI STUDIO  /  ACCESO SEGURO')
        self.setMinimumSize(850, 530)
        self.resize(1000, 605)
        self.setObjectName('appBackground')
        self.setModal(True)
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        izquierda = QWidget(objectName='loginLeft')
        izquierda.setMinimumWidth(400)
        ai = QVBoxLayout(izquierda)
        ai.setContentsMargins(52, 50, 42, 46)
        ai.setSpacing(17)
        ai.addWidget(etiqueta('flexi.', 'logo'))
        ai.addWidget(etiqueta('STUDIO  /  GESTIÓN INTELIGENTE', 'sectionLabel'))
        ai.addSpacing(85)
        ai.addWidget(etiqueta('Diseñado para una\nmejor operación.', 'brandTitle'))
        ai.addWidget(etiqueta('Administración de calzado, catálogos, inventario y datos conectados desde un solo lugar.', 'muted'))
        ai.addStretch()
        pill = etiqueta('●   RED / GRAPHITE  •  DESKTOP EDITION', 'pill')
        pill.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        ai.addWidget(pill)
        ai.addWidget(etiqueta('FLEXI ZAMORA     /     SEGURIDAD Y CONTROL', 'caption'))
        derecha = QWidget(objectName='loginRight')
        ar = QVBoxLayout(derecha)
        ar.setContentsMargins(70, 70, 70, 65)
        ar.setSpacing(16)
        ar.addStretch()
        ar.addWidget(etiqueta('ACCESO AL SISTEMA', 'sectionLabel'))
        ar.addWidget(etiqueta('Bienvenido a Flexi.', 'pageTitle'))
        ar.addWidget(etiqueta('Ingresa tus credenciales para continuar.', 'muted'))
        ar.addSpacing(12)
        ar.addWidget(etiqueta('MOTOR DE BASE DE DATOS', 'sectionLabel'))
        self.motor = QComboBox()
        self.motor.addItem('PostgreSQL', 'postgres')
        self.motor.addItem('SQL Server', 'sqlserver')
        if leer_configuracion().get('FLEXI_DB','postgres').lower() == 'sqlserver': self.motor.setCurrentIndex(1)
        ar.addWidget(self.motor)
        ar.addWidget(etiqueta('CORREO ELECTRÓNICO', 'sectionLabel'))
        self.correo = QLineEdit()
        self.correo.setPlaceholderText('usuario@flexizamora.com')
        self.correo.setClearButtonEnabled(True)
        ar.addWidget(self.correo)
        ar.addWidget(etiqueta('CONTRASEÑA', 'sectionLabel'))
        self.clave = QLineEdit()
        self.clave.setEchoMode(QLineEdit.EchoMode.Password)
        self.clave.setPlaceholderText('Escribe tu contraseña')
        self.clave.returnPressed.connect(self.ingresar)
        ar.addWidget(self.clave)
        self.btn_ingresar = boton('INGRESAR AL SISTEMA  →', self.ingresar, 'primary')
        self.btn_ingresar.setMinimumHeight(49)
        ar.addWidget(self.btn_ingresar)
        self.error = etiqueta('', 'muted')
        self.error.setStyleSheet('color: #FF7788;')
        ar.addWidget(self.error)
        ar.addWidget(boton('⚙  Configurar conexiones de base de datos', self.abrir_configuracion))
        ar.addWidget(etiqueta('Las cuentas se validan en tu base de datos existente.', 'caption'))
        ar.addStretch()
        outer.addWidget(izquierda, 5)
        outer.addWidget(derecha, 6)

    def abrir_configuracion(self):
        if DialogoConexiones(self).exec() == QDialog.DialogCode.Accepted:
            motor = leer_configuracion().get('FLEXI_DB', 'postgres')
            indice = self.motor.findData(motor)
            if indice >= 0:
                self.motor.setCurrentIndex(indice)
            self.error.setText('Conexiones actualizadas. Ya puedes iniciar sesión.')

    def ingresar(self):
        self.error.setText('')
        correo = self.correo.text().strip()
        clave = self.clave.text()
        if not correo or not clave:
            self.error.setText('Introduce correo y contraseña.')
            return
        if time.monotonic() < self._bloqueado_hasta:
            self.error.setText('Demasiados intentos. Espera 30 segundos.')
            return
        db = BaseDatos(self.motor.currentData())
        auth = Autenticacion(db)
        auth.fallos = self._fallos
        auth.bloqueado_hasta = self._bloqueado_hasta
        self.btn_ingresar.setEnabled(False)
        QApplication.processEvents()
        try:
            db.conectar()
            sesion = auth.autenticar(correo, clave)
            self.db, self.sesion = db, sesion
            self.clave.clear()
            self.accept()
        except Exception as exc:
            self.error.setText(str(exc))
            self.clave.clear()
            db.cerrar()
        finally:
            self._fallos = auth.fallos
            self._bloqueado_hasta = auth.bloqueado_hasta
            self.btn_ingresar.setEnabled(True)


class ModeloRegistros(QAbstractTableModel):
    def __init__(self, tabla, rows, etiquetas_fk=None, parent=None):
        super().__init__(parent)
        self.tabla = TABLAS[tabla]
        self.rows = list(rows)
        self.columnas = list(self.tabla.visibles)
        self.etiquetas_fk = etiquetas_fk or {}

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.rows)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.columnas)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.columnas[section].etiqueta
            return f'{section + 1:02}'
        return None

    def formato(self, row, columna):
        c = self.columnas[columna]
        v = row.get(c.nombre)
        if c.fk and v is not None:
            ref = self.etiquetas_fk.get(c.fk, {}).get(str(v))
            if ref: return f'{ref}  ·  #{v}'
        if v is None: return '—'
        if c.tipo == 'booleano': return 'Activo' if v in (1, True, '1') else 'Inactivo'
        if c.tipo == 'precio':
            try: return f'$ {float(v):,.2f}'
            except (TypeError, ValueError): pass
        return str(v)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid(): return None
        fila = self.rows[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return self.formato(fila, index.column())
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if self.columnas[index.column()].tipo in ('entero', 'precio', 'numero'):
                return int(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        if role == Qt.ItemDataRole.ForegroundRole:
            if self.columnas[index.column()].nombre == self.tabla.pk:
                return QColor('#FF7489')
        return None


class FiltroRegistros(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.campo = '*'
        self.texto = ''

    def aplicar(self, campo, texto):
        self.campo, self.texto = campo, normalizar(texto)
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, parent):
        m = self.sourceModel()
        if not self.texto: return True
        data = m.rows[source_row]
        campos = range(len(m.columnas)) if self.campo == '*' else [i for i,c in enumerate(m.columnas) if c.nombre == self.campo]
        return any(self.texto in normalizar(m.formato(data, i)) for i in campos)


class EditorRegistro(QDialog):
    def __init__(self, servicio, tabla, registro=None, parent=None):
        super().__init__(parent)
        self.servicio = servicio
        self.tabla = TABLAS[tabla]
        self.registro = registro
        self.campos = {}
        self.setWindowTitle(('Editar' if registro else 'Nuevo') + ' • ' + self.tabla.titulo)
        self.resize(610, 590)
        self.setMinimumWidth(540)
        base = QVBoxLayout(self)
        base.setContentsMargins(30, 24, 30, 22)
        base.setSpacing(13)
        base.addWidget(etiqueta('FLEXI  /  FORMULARIO', 'sectionLabel'))
        base.addWidget(etiqueta(('Editar ' if registro else 'Registrar ') + self.tabla.titulo.lower(), 'pageTitle'))
        base.addWidget(etiqueta('Los campos con * son obligatorios. Selecciona las relaciones por nombre.', 'muted'))
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        interno = QWidget()
        form = QFormLayout(interno)
        form.setContentsMargins(3, 10, 12, 12)
        form.setSpacing(14)
        for campo in self.tabla.modificables:
            if campo.fk:
                w = QComboBox()
                w.addItem('Seleccionar...', None)
                items = self.servicio.consultar(campo.fk)
                items.sort(key=lambda r: str(etiqueta_registro(campo.fk, r)).casefold())
                id_fk = TABLAS[campo.fk].pk
                for r in items:
                    w.addItem(f"{etiqueta_registro(campo.fk, r)}  ·  #{r[id_fk]}", r[id_fk])
                if registro is not None:
                    idx = w.findData(registro.get(campo.nombre))
                    w.setCurrentIndex(max(0, idx))
            elif campo.tipo == 'booleano':
                w = QCheckBox('Activo')
                w.setChecked(bool(registro.get(campo.nombre, True)) if registro else True)
            elif campo.tipo == 'entero':
                w = QSpinBox()
                w.setMaximum(1_000_000_000)
                w.setMinimum(0)
                if registro is not None: w.setValue(int(registro.get(campo.nombre) or 0))
            elif campo.tipo in ('precio', 'numero'):
                w = QDoubleSpinBox()
                w.setDecimals(2 if campo.tipo == 'precio' else 1)
                w.setSingleStep(0.01 if campo.tipo == 'precio' else 0.5)
                w.setMaximum(100_000_000)
                w.setMinimum(0.01 if campo.tipo == 'precio' else 0)
                if registro is not None: w.setValue(float(registro.get(campo.nombre) or 0))
            else:
                w = QLineEdit()
                if registro is not None and registro.get(campo.nombre) is not None:
                    w.setText(str(registro.get(campo.nombre)))
                w.setPlaceholderText('Introduce ' + campo.etiqueta.lower())
            self.campos[campo.nombre] = (campo, w)
            form.addRow(etiqueta(campo.etiqueta + (' *' if campo.requerido else ''), 'muted'), w)
        scroll.setWidget(interno)
        base.addWidget(scroll, 1)
        actions = QHBoxLayout()
        actions.addStretch()
        actions.addWidget(boton('Cancelar', self.reject))
        actions.addWidget(boton('Guardar cambios' if registro else 'Registrar', self.guardar, 'primary'))
        base.addLayout(actions)

    def guardar(self):
        datos = {}
        for key, (c, w) in self.campos.items():
            if isinstance(w, QComboBox): val = w.currentData()
            elif isinstance(w, QCheckBox): val = w.isChecked()
            elif isinstance(w, (QSpinBox, QDoubleSpinBox)): val = w.value()
            else: val = w.text().strip() or None
            if c.requerido and (val is None or val == ''):
                aviso(self, 'Dato requerido', f'Completa el campo: {c.etiqueta}', True)
                return
            if c.nombre == 'precio_venta' and float(val) <= 0:
                aviso(self, 'Precio inválido', 'El precio debe ser mayor a cero.', True)
                return
            datos[key] = val
        try:
            if self.registro is not None:
                result = self.servicio.actualizar(self.tabla.nombre, self.registro[self.tabla.pk], datos)
            else:
                result = self.servicio.insertar(self.tabla.nombre, datos)
            if not result:
                aviso(self, 'Sin cambios', 'Ningún registro fue modificado.')
                return
            self.accept()
        except Exception as exc:
            aviso(self, 'No se pudo guardar', str(exc), True)


class EditorUsuario(QDialog):
    """Alta/edición de cuentas con roles reales Tipo_Usuario y contraseña PBKDF2."""
    def __init__(self, servicio, registro=None, parent=None):
        super().__init__(parent)
        self.servicio, self.registro = servicio, registro
        self.setWindowTitle('Cuenta de usuario • Flexi')
        self.setMinimumWidth(510)
        form_root = QVBoxLayout(self)
        form_root.setContentsMargins(30,25,30,25)
        form_root.setSpacing(15)
        form_root.addWidget(etiqueta('ACCESO Y PERSONAL', 'sectionLabel'))
        form_root.addWidget(etiqueta('Editar cuenta' if registro else 'Nueva cuenta', 'pageTitle'))
        form = QFormLayout()
        form.setSpacing(12)
        self.inputs = {}
        for key, lab in [('nombre','Nombre *'),('apellido_paterno','Apellido paterno *'),
                         ('apellido_materno','Apellido materno'),('correo_electronico','Correo electrónico *'),
                         ('telefono','Teléfono')]:
            w = QLineEdit()
            if registro: w.setText(str(registro.get(key) or ''))
            self.inputs[key] = w
            form.addRow(lab,w)
        self.rol = QComboBox()
        roles = self.servicio.consultar('Tipo_Usuario')
        for r in roles:
            self.rol.addItem(r['nombre_rol'], r['id_tipo_usuario'])
        if registro:
            idx = self.rol.findData(registro['id_tipo_usuario'])
            self.rol.setCurrentIndex(max(0, idx))
        form.addRow('Rol de usuario *', self.rol)
        self.activo = QCheckBox('Permitir iniciar sesión')
        self.activo.setChecked(bool(registro.get('estatus_activo', True)) if registro else True)
        form.addRow('Estado de cuenta', self.activo)
        if not registro:
            self.pwd = QLineEdit()
            self.pwd.setEchoMode(QLineEdit.EchoMode.Password)
            self.pwd.setPlaceholderText('12 caracteres como mínimo')
            form.addRow('Contraseña inicial *', self.pwd)
            self.pwd2 = QLineEdit()
            self.pwd2.setEchoMode(QLineEdit.EchoMode.Password)
            form.addRow('Confirmar contraseña *', self.pwd2)
        form_root.addLayout(form)
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(boton('Cancelar', self.reject))
        row.addWidget(boton('Guardar cuenta', self.guardar, 'primary'))
        form_root.addLayout(row)

    def guardar(self):
        datos = {k:w.text().strip() for k,w in self.inputs.items()}
        datos.update(id_tipo_usuario=self.rol.currentData(), estatus_activo=self.activo.isChecked())
        try:
            if self.registro:
                self.servicio.editar_usuario(self.registro['id_usuario'], datos)
            else:
                if self.pwd.text() != self.pwd2.text():
                    raise ValueError('Las contraseñas no coinciden.')
                self.servicio.crear_usuario(datos, self.pwd.text())
            self.accept()
        except Exception as exc:
            aviso(self, 'No se pudo guardar la cuenta', str(exc), True)


class PasswordUsuario(QDialog):
    def __init__(self, servicio, usuario, parent=None):
        super().__init__(parent)
        self.servicio, self.usuario = servicio, usuario
        self.setWindowTitle('Restablecer contraseña')
        self.setMinimumWidth(470)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(26,26,26,26)
        lay.setSpacing(13)
        lay.addWidget(etiqueta('RESTABLECER ACCESO', 'sectionLabel'))
        lay.addWidget(etiqueta(f"{usuario['nombre']} {usuario['apellido_paterno']}", 'sectionTitle'))
        lay.addWidget(etiqueta('La nueva contraseña se almacenará con un hash seguro, no en texto plano.', 'muted'))
        self.clave = QLineEdit()
        self.clave.setEchoMode(QLineEdit.EchoMode.Password)
        self.clave.setPlaceholderText('Nueva contraseña (mínimo 12 caracteres)')
        self.confirmacion = QLineEdit()
        self.confirmacion.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirmacion.setPlaceholderText('Repite la nueva contraseña')
        lay.addWidget(self.clave)
        lay.addWidget(self.confirmacion)
        actions = QHBoxLayout()
        actions.addWidget(boton('Cancelar', self.reject))
        actions.addWidget(boton('Actualizar contraseña', self.guardar, 'primary'))
        lay.addLayout(actions)

    def guardar(self):
        try:
            if self.clave.text() != self.confirmacion.text():
                raise ValueError('Las contraseñas no coinciden.')
            self.servicio.cambiar_password(self.usuario['id_usuario'], self.clave.text())
            self.accept()
        except Exception as exc:
            aviso(self, 'Contraseña inválida', str(exc), True)


class DetalleRegistro(QDialog):
    def __init__(self, tabla, registro, lookup, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Detalle • ' + TABLAS[tabla].titulo)
        self.resize(570, 530)
        ly = QVBoxLayout(self)
        ly.setContentsMargins(28,24,28,24)
        ly.setSpacing(12)
        ly.addWidget(etiqueta('FICHA DE REGISTRO', 'sectionLabel'))
        ly.addWidget(etiqueta(TABLAS[tabla].titulo, 'pageTitle'))
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        internal = QWidget()
        form = QFormLayout(internal)
        form.setSpacing(16)
        for c in TABLAS[tabla].visibles:
            val = registro.get(c.nombre)
            if c.fk and val is not None:
                val = f"{lookup.get(c.fk, {}).get(str(val), 'Registro relacionado')} · #{val}"
            if val is None: val = '—'
            if c.tipo == 'booleano': val = 'Activo' if bool(val) else 'Inactivo'
            vlabel = etiqueta(str(val))
            vlabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            form.addRow(etiqueta(c.etiqueta, 'muted'), vlabel)
        scroll.setWidget(internal)
        ly.addWidget(scroll)
        ly.addWidget(boton('Cerrar', self.accept))


class NavegadorLigas(QDialog):
    abrir = pyqtSignal(str, object)
    def __init__(self, servicio, tabla, fila, parent=None):
        super().__init__(parent)
        self.servicio = servicio
        self.tabla = tabla
        self.fila = fila
        self.setWindowTitle('Ligas de registros • Flexi')
        self.resize(780, 510)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(27, 26, 27, 22)
        lay.setSpacing(11)
        lay.addWidget(etiqueta('RELACIONES ENTRE TABLAS', 'sectionLabel'))
        lay.addWidget(etiqueta('Explorar ligas', 'pageTitle'))
        lay.addWidget(etiqueta(f"{TABLAS[tabla].titulo}  /  Registro #{fila[TABLAS[tabla].pk]}   •   Doble clic para navegar", 'muted'))
        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Tabla / relación', 'Registro'])
        self.tree.setAlternatingRowColors(True)
        self.tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        lay.addWidget(self.tree)
        salientes, entrantes = ligas_de(tabla)
        grupo = QTreeWidgetItem(self.tree, ['LIGAS HACIA OTRAS TABLAS', ''])
        for _, campo, destino, _ in salientes:
            valor = fila.get(campo)
            if valor is None: continue
            try:
                exigir(servicio.sesion, 'consultar', destino)
                r = servicio.db.uno(destino, valor)
                if r:
                    it = QTreeWidgetItem(grupo, [f'{TABLAS[destino].titulo} · {campo}',
                                                 etiqueta_registro(destino, r) + f'   #{valor}'])
                    it.setData(0, Qt.ItemDataRole.UserRole, (destino, valor))
            except (AccesoDenegado, ErrorDatos):
                continue
        grupo2 = QTreeWidgetItem(self.tree, ['REGISTROS QUE UTILIZAN ESTA TABLA', ''])
        for origen, campo, _, _ in entrantes:
            try:
                exigir(servicio.sesion, 'consultar', origen)
                relacionados = servicio.db.ligados(origen, campo, fila[TABLAS[tabla].pk])
                sub = QTreeWidgetItem(grupo2, [f'{TABLAS[origen].titulo} · {campo}', f'{len(relacionados)} registros'])
                for r in relacionados[:200]:
                    pk = r[TABLAS[origen].pk]
                    item = QTreeWidgetItem(sub, [TABLAS[origen].titulo, etiqueta_registro(origen, r) + f'   #{pk}'])
                    item.setData(0, Qt.ItemDataRole.UserRole, (origen, pk))
            except (AccesoDenegado, ErrorDatos):
                continue
        self.tree.expandToDepth(1)
        self.tree.itemDoubleClicked.connect(self.ir)
        lay.addWidget(boton('Cerrar', self.reject))

    def ir(self, item, column):
        target = item.data(0, Qt.ItemDataRole.UserRole)
        if target:
            self.abrir.emit(*target)
            self.accept()


class VentanaPrincipal(QMainWindow):
    def __init__(self, db, sesion):
        super().__init__()
        self.db = db
        self.sesion = sesion
        self.srv = Servicio(db, sesion)
        self.actual = 'Producto'
        self.lookups = {}
        self.modelo = None
        self.proxy = None
        self.botones_nav = {}
        self.setWindowTitle(f'FLEXI STUDIO  /  {sesion.etiqueta_rol}  /  {db.motor.upper()}')
        self.resize(1450, 860)
        self.setMinimumSize(1080, 660)
        self.setObjectName('appBackground')
        main = QWidget(objectName='appBackground')
        self.setCentralWidget(main)
        root = QHBoxLayout(main)
        root.setContentsMargins(0,0,0,0)
        root.setSpacing(0)
        self._sidebar(root)
        right = QWidget(objectName='centralPanel')
        rlay = QVBoxLayout(right)
        rlay.setContentsMargins(0,0,0,0)
        rlay.setSpacing(0)
        self._topbar(rlay)
        self.stack = QStackedWidget()
        self.dashboard = QWidget()
        self.catalogo = QWidget()
        self._dashboard(self.dashboard)
        self._catalogo(self.catalogo)
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.catalogo)
        rlay.addWidget(self.stack)
        root.addWidget(right, 1)
        sb = QStatusBar()
        self.setStatusBar(sb)
        sb.showMessage('●  Conexión activa    •    Sesión protegida    •    Flechas y doble clic disponibles')
        self.ir_inicio()

    def _sidebar(self, root):
        panel = QWidget(objectName='sideBar')
        panel.setFixedWidth(250)
        ly = QVBoxLayout(panel)
        ly.setContentsMargins(22,26,22,24)
        ly.setSpacing(6)
        ly.addWidget(etiqueta('flexi.', 'logoSmall'))
        ly.addWidget(etiqueta('STUDIO    /    ADMIN CONSOLE', 'caption'))
        ly.addSpacing(30)
        ly.addWidget(etiqueta('ESPACIO DE TRABAJO', 'sectionLabel'))
        self.btn_inicio = boton('⌂   Panel general', self.ir_inicio, 'nav')
        self.btn_inicio.setCheckable(True)
        ly.addWidget(self.btn_inicio)
        ly.addSpacing(17)
        ly.addWidget(etiqueta('TABLAS MAESTRAS', 'sectionLabel'))
        scroll = QScrollArea()
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidgetResizable(True)
        group = QWidget()
        nav = QVBoxLayout(group)
        nav.setContentsMargins(0,6,5,6)
        nav.setSpacing(4)
        for tabla in MAESTRAS:
            b = boton('◇   '+tabla.titulo, lambda _, t=tabla.nombre: self.ir_tabla(t), 'nav')
            b.setCheckable(True)
            nav.addWidget(b)
            self.botones_nav[tabla.nombre] = b
        nav.addSpacing(20)
        nav.addWidget(etiqueta('OPERACIONES', 'sectionLabel'))
        for tabla in OPERATIVAS:
            if not self.sesion.es_admin and tabla.nombre not in ('Producto','Inventario'):
                continue
            b = boton('▤   '+tabla.titulo, lambda _, t=tabla.nombre: self.ir_tabla(t), 'nav')
            b.setCheckable(True)
            nav.addWidget(b)
            self.botones_nav[tabla.nombre] = b
        nav.addStretch()
        scroll.setWidget(group)
        ly.addWidget(scroll, 1)
        ly.addSpacing(14)
        frame, f = superficie(nombre='redSurface', margen=14, espacio=6)
        f.addWidget(etiqueta(self.sesion.etiqueta_rol, 'sectionLabel'))
        f.addWidget(etiqueta(self.sesion.nombre, 'sectionTitle'))
        mail = etiqueta(self.sesion.correo, 'caption')
        f.addWidget(mail)
        ly.addWidget(frame)
        ly.addWidget(boton('↪   Cerrar sesión', self.cerrar_sesion))
        root.addWidget(panel)

    def _topbar(self, root):
        top = QWidget(objectName='topBar')
        ly = QHBoxLayout(top)
        ly.setContentsMargins(34,16,34,16)
        ly.addWidget(etiqueta('FLEXI   /   WORKSPACE', 'sectionLabel'))
        ly.addStretch()
        pill = etiqueta('●  '+self.db.motor.upper() + '  /  CONECTADO', 'pill')
        pill.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        ly.addWidget(pill)
        ly.addSpacing(20)
        ly.addWidget(etiqueta(self.sesion.etiqueta_rol, 'caption'))
        root.addWidget(top)

    def _page_container(self, parent):
        ly = QVBoxLayout(parent)
        ly.setContentsMargins(35,30,35,30)
        ly.setSpacing(19)
        return ly

    def _dashboard(self, page):
        lay = self._page_container(page)
        top = QHBoxLayout()
        head = QVBoxLayout()
        head.addWidget(etiqueta('TU ESPACIO DE TRABAJO', 'sectionLabel'))
        head.addWidget(etiqueta('Panel general', 'pageTitle'))
        head.addWidget(etiqueta('Una vista clara de la operación y sus datos.', 'muted'))
        top.addLayout(head)
        top.addStretch()
        self.fecha = etiqueta(datetime.now().strftime('%d / %m / %Y'), 'pill')
        top.addWidget(self.fecha)
        lay.addLayout(top)
        kpis = QHBoxLayout()
        kpis.setSpacing(15)
        self.kpis = {}
        for key, titulo, descript in (
            ('Producto','PRODUCTOS','Modelos registrados'),
            ('Marca','MARCAS','Catálogo de marcas'),
            ('Categoria','CATEGORÍAS','Segmentos activos'),
            ('Inventario','INVENTARIO','Renglones de stock'),
        ):
            box, content = superficie(nombre='kpiCard', margen=21, espacio=10)
            content.addWidget(etiqueta(titulo, 'sectionLabel'))
            numero = etiqueta('—', 'kpi')
            self.kpis[key] = numero
            content.addWidget(numero)
            content.addWidget(etiqueta(descript, 'caption'))
            kpis.addWidget(box, 1)
        lay.addLayout(kpis)
        container, body = superficie(nombre='surface', margen=27, espacio=14)
        body.addWidget(etiqueta('NAVEGACIÓN RÁPIDA', 'sectionLabel'))
        body.addWidget(etiqueta('¿Qué deseas hacer hoy?', 'sectionTitle'))
        body.addWidget(etiqueta('Abre un catálogo para consultar, buscar por una sola letra, seguir ligas o exportar a Excel.', 'muted'))
        acciones = QHBoxLayout()
        acciones.addWidget(boton('Explorar productos    ↗', lambda: self.ir_tabla('Producto'), 'primary'))
        acciones.addWidget(boton('Consultar inventario    ↗', lambda: self.ir_tabla('Inventario')))
        acciones.addWidget(boton('Administrar categorías    ↗', lambda: self.ir_tabla('Categoria')))
        acciones.addStretch()
        body.addLayout(acciones)
        lay.addWidget(container)
        note, b = superficie(nombre='redSurface', margen=22, espacio=8)
        b.addWidget(etiqueta('SEGURIDAD POR ROL', 'sectionLabel'))
        b.addWidget(etiqueta(
            'Administrador: catálogos, producto, ventas y gestión de cuentas.' if self.sesion.es_admin else
            'Trabajador: consulta de catálogos, productos e inventario. Exportaciones y ligas permitidas.', 'muted'))
        lay.addWidget(note)
        lay.addStretch()

    def _catalogo(self, page):
        ly = self._page_container(page)
        h = QHBoxLayout()
        left = QVBoxLayout()
        left.setSpacing(4)
        left.addWidget(etiqueta('EXPLORADOR DE DATOS  /  TABLAS', 'sectionLabel'))
        self.title_tabla = etiqueta('Productos', 'pageTitle')
        left.addWidget(self.title_tabla)
        self.sub_tabla = etiqueta('', 'muted')
        left.addWidget(self.sub_tabla)
        h.addLayout(left)
        h.addStretch()
        self.btn_nuevo = boton('＋  Nuevo registro', self.nuevo_registro, 'primary')
        self.btn_editar = boton('✎  Editar', self.editar_registro)
        self.btn_eliminar = boton('×  Eliminar', self.eliminar_registro, 'danger')
        self.btn_password = boton('⇄  Restablecer clave', self.reset_password)
        for b in (self.btn_nuevo,self.btn_editar,self.btn_eliminar,self.btn_password): h.addWidget(b)
        ly.addLayout(h)
        filtros, fl = superficie(vertical=True, nombre='surface', margen=14, espacio=9)
        fila_busqueda = QHBoxLayout()
        fila_acciones = QHBoxLayout()
        self.campo_busqueda = QComboBox()
        self.campo_busqueda.setMinimumWidth(195)
        self.campo_busqueda.currentIndexChanged.connect(self.filtrar)
        self.busqueda = QLineEdit()
        self.busqueda.setMinimumWidth(270)
        self.busqueda.setPlaceholderText('Buscar... una sola letra es suficiente')
        self.busqueda.setClearButtonEnabled(True)
        self.busqueda.textChanged.connect(self.filtrar)
        self.btn_export = boton('↓  Exportar Excel', self.exportar_xlsx)
        self.btn_ligas = boton('↗  Ver ligas', self.abrir_ligas)
        self.btn_reload = boton('⟳  Actualizar', self.refrescar)
        fila_busqueda.addWidget(etiqueta('BUSCAR POR', 'sectionLabel'))
        fila_busqueda.addWidget(self.campo_busqueda)
        fila_busqueda.addWidget(self.busqueda, 1)
        fila_acciones.addStretch()
        fila_acciones.addWidget(self.btn_export)
        fila_acciones.addWidget(self.btn_ligas)
        fila_acciones.addWidget(self.btn_reload)
        fl.addLayout(fila_busqueda)
        fl.addLayout(fila_acciones)
        ly.addWidget(filtros)
        self.table = QTableView()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(41)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setMinimumSectionSize(115)
        self.table.setSortingEnabled(False)
        self.table.doubleClicked.connect(self.ver_detalle)
        self.table.setWordWrap(False)
        ly.addWidget(self.table, 1)
        foot = QHBoxLayout()
        self.contador = etiqueta('0 registros', 'sectionLabel')
        foot.addWidget(self.contador)
        foot.addStretch()
        foot.addWidget(etiqueta('Doble clic: detalle     •     Búsqueda inmediata     •     Excel con filtro actual', 'caption'))
        ly.addLayout(foot)

    def marcar_nav(self, tabla=None):
        self.btn_inicio.setChecked(tabla is None)
        for name, b in self.botones_nav.items():
            b.setChecked(name == tabla)

    def ir_inicio(self):
        self.marcar_nav(None)
        self.stack.setCurrentWidget(self.dashboard)
        for name, lab in self.kpis.items():
            try: lab.setText(str(len(self.srv.consultar(name))))
            except Exception: lab.setText('—')

    def ir_tabla(self, tabla, selecionar_id=None):
        try:
            exigir(self.sesion, 'consultar', tabla)
            self.actual = tabla
            self.marcar_nav(tabla)
            self.stack.setCurrentWidget(self.catalogo)
            self.title_tabla.setText(TABLAS[tabla].titulo)
            self.sub_tabla.setText(
                f"{TABLAS[tabla].grupo}  /  {('Lectura y gestión' if self.sesion.es_admin else 'Solo consulta')}  /  {self.db.motor.upper()}")
            self.btn_nuevo.setVisible(self.sesion.es_admin and (TABLAS[tabla].editable or tabla == 'Usuario'))
            self.btn_editar.setVisible(self.sesion.es_admin and (TABLAS[tabla].editable or tabla == 'Usuario'))
            self.btn_eliminar.setVisible(self.sesion.es_admin and TABLAS[tabla].editable)
            self.btn_password.setVisible(self.sesion.es_admin and tabla == 'Usuario')
            self.refrescar()
            if selecionar_id is not None:
                self.campo_busqueda.setCurrentIndex(1) # pk es la primera columna
                self.busqueda.setText(str(selecionar_id))
                if self.proxy and self.proxy.rowCount():
                    self.table.selectRow(0)
        except Exception as exc:
            aviso(self, 'No se pudo abrir la tabla', str(exc), True)

    def refrescar(self):
        try:
            filas = self.srv.consultar(self.actual)
            lookup = {}
            for c in TABLAS[self.actual].visibles:
                if c.fk and c.fk not in lookup:
                    try:
                        rel = self.srv.consultar(c.fk)
                        lookup[c.fk] = {str(r[TABLAS[c.fk].pk]): etiqueta_registro(c.fk,r) for r in rel}
                    except AccesoDenegado:
                        lookup[c.fk] = {}
            self.lookups = lookup
            anterior_modelo, anterior_proxy = self.modelo, self.proxy
            self.modelo = ModeloRegistros(self.actual, filas, lookup, self)
            self.proxy = FiltroRegistros(self)
            self.proxy.setSourceModel(self.modelo)
            self.table.setModel(self.proxy)
            if anterior_proxy: anterior_proxy.deleteLater()
            if anterior_modelo: anterior_modelo.deleteLater()
            self.campo_busqueda.blockSignals(True)
            self.campo_busqueda.clear()
            self.campo_busqueda.addItem('Todos los campos', '*')
            for c in TABLAS[self.actual].visibles:
                self.campo_busqueda.addItem(c.etiqueta, c.nombre)
            self.campo_busqueda.blockSignals(False)
            self.busqueda.blockSignals(True)
            self.busqueda.clear()
            self.busqueda.blockSignals(False)
            self.table.horizontalHeader().resizeSections(QHeaderView.ResizeMode.ResizeToContents)
            self.filtrar()
            self.statusBar().showMessage(f'{len(filas)} registros cargados de {TABLAS[self.actual].titulo}')
        except Exception as exc:
            aviso(self, 'Error de consulta', str(exc), True)

    def filtrar(self, *args):
        if self.proxy:
            self.proxy.aplicar(self.campo_busqueda.currentData() or '*', self.busqueda.text())
            self.contador.setText(f'{self.proxy.rowCount():,} coincidencias  /  {len(self.modelo.rows):,} registros')

    def seleccionado(self):
        if not self.proxy or not self.table.selectionModel(): return None
        idx = self.table.selectionModel().currentIndex()
        if not idx.isValid(): return None
        source_idx = self.proxy.mapToSource(idx)
        if source_idx.row() >= len(self.modelo.rows): return None
        return self.modelo.rows[source_idx.row()]

    def _seleccion_requerida(self):
        r = self.seleccionado()
        if r is None:
            aviso(self, 'Selecciona un registro', 'Haz clic sobre una fila de la tabla.')
        return r

    def ver_detalle(self, index=None):
        r = self._seleccion_requerida()
        if r: DetalleRegistro(self.actual, r, self.lookups, self).exec()

    def nuevo_registro(self):
        try:
            if self.actual == 'Usuario':
                dlg = EditorUsuario(self.srv, parent=self)
            else:
                exigir(self.sesion, 'insertar', self.actual)
                dlg = EditorRegistro(self.srv, self.actual, parent=self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                self.refrescar()
                self.statusBar().showMessage('Registro creado correctamente', 4000)
        except Exception as exc:
            aviso(self, 'No se pudo crear', str(exc), True)

    def editar_registro(self):
        r = self._seleccion_requerida()
        if not r: return
        try:
            if self.actual == 'Usuario':
                dlg = EditorUsuario(self.srv, r, self)
            else:
                exigir(self.sesion, 'actualizar', self.actual)
                dlg = EditorRegistro(self.srv, self.actual, r, self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                self.refrescar()
        except Exception as exc:
            aviso(self, 'No se pudo editar', str(exc), True)

    def eliminar_registro(self):
        r = self._seleccion_requerida()
        if not r: return
        t = TABLAS[self.actual]
        if not confirmar(self, f'¿Eliminar {t.titulo} #{r[t.pk]}?\n\nEsta acción es permanente y puede estar bloqueada por ligas de la base de datos.',
                         'Confirmar eliminación'):
            return
        try:
            affected = self.srv.eliminar(self.actual, r[t.pk])
            if affected:
                self.refrescar()
                aviso(self, 'Operación completada', 'Registro eliminado correctamente.')
            else:
                aviso(self, 'Sin cambios', 'No se encontró el registro.')
        except Exception as exc:
            aviso(self, 'Eliminación rechazada', str(exc), True)

    def reset_password(self):
        r = self._seleccion_requerida()
        if r and self.actual == 'Usuario':
            if PasswordUsuario(self.srv, r, self).exec() == QDialog.DialogCode.Accepted:
                aviso(self, 'Credencial actualizada', 'Contraseña guardada correctamente.')

    def exportar_xlsx(self):
        if not self.proxy: return
        n = self.proxy.rowCount()
        if not n:
            aviso(self, 'Sin resultados', 'La búsqueda actual no contiene registros para exportar.')
            return
        self.contador.setText(f'Exportando {n} registros...')
        nombre = f'Flexi_{self.actual}_{datetime.now():%Y%m%d_%H%M}.xlsx'
        destino, _ = QFileDialog.getSaveFileName(self, 'Guardar reporte Excel', str(Path.home()/'Documents'/nombre),
                                                 'Excel (*.xlsx)')
        if not destino:
            self.filtrar()
            return
        if not destino.lower().endswith('.xlsx'): destino += '.xlsx'
        try:
            registros = [self.modelo.rows[self.proxy.mapToSource(self.proxy.index(i,0)).row()]
                         for i in range(n)]
            campos = [(c.nombre, c.etiqueta) for c in TABLAS[self.actual].visibles]
            exportar(self.actual, campos, registros, destino)
            aviso(self, 'Excel exportado', f'Se exportaron {n} registros.\n\nArchivo:\n{destino}')
        except Exception as exc:
            aviso(self, 'Error de exportación', str(exc), True)
        self.filtrar()

    def abrir_ligas(self):
        r = self._seleccion_requerida()
        if not r: return
        dlg = NavegadorLigas(self.srv, self.actual, r, self)
        dlg.abrir.connect(lambda tabla, pk: QTimer.singleShot(0, lambda: self.ir_tabla(tabla, pk)))
        dlg.exec()

    def cerrar_sesion(self):
        if confirmar(self, '¿Cerrar sesión y volver al inicio de sesión?', 'Cerrar sesión'):
            self._cerrar_pedido = True
            self.close()

    def closeEvent(self, event):
        # El bucle del main relanza login solamente si se pidió cerrar sesión.
        if not getattr(self, '_cerrar_pedido', False):
            if not confirmar(self, '¿Deseas salir de Flexi Studio?', 'Salir'):
                event.ignore()
                return
        try: self.db.cerrar()
        finally:
            event.accept()
            QApplication.instance().exit(0)
