"""Diccionario de datos basado en los dos scripts SQL Flexi Zamora suministrados.

No se crean tablas ni se altera su estructura; la identificación de nombres SQL
está limitada a los declarados aquí (evita interpolar identificadores de usuario).
"""
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Campo:
    nombre: str
    etiqueta: str
    tipo: str = 'texto'  # texto, entero, numero, precio, fecha, booleano
    requerido: bool = True
    fk: str | None = None
    secreto: bool = False
    autogenerado: bool = False
    defecto: bool = False


@dataclass(frozen=True)
class Tabla:
    nombre: str
    titulo: str
    grupo: str
    pk: str
    campos: tuple[Campo, ...]
    editable: bool = True
    nota: str = ''
    @property
    def visibles(self):
        return tuple(c for c in self.campos if not c.secreto)
    @property
    def modificables(self):
        return tuple(c for c in self.campos if not c.autogenerado and not c.secreto)
    @property
    def primaria(self):
        return next(c for c in self.campos if c.nombre == self.pk)


def C(n, e, tipo='texto', *, requerido=True, fk=None, secreto=False, autogenerado=False, defecto=False):
    return Campo(n, e, tipo, requerido, fk, secreto, autogenerado, defecto)

TABLAS = {
    t.nombre: t for t in (
        Tabla('Tipo_Usuario', 'Tipos de usuario', 'Maestras', 'id_tipo_usuario', (
            C('id_tipo_usuario','ID de rol','entero',autogenerado=True),
            C('nombre_rol','Rol'), C('descripcion_permisos','Permisos', requerido=False))),
        Tabla('Categoria', 'Categorías', 'Maestras', 'id_categoria', (
            C('id_categoria','ID categoría','entero',autogenerado=True), C('nombre_categoria','Categoría'))),
        Tabla('Marca', 'Marcas', 'Maestras', 'id_marca', (
            C('id_marca','ID marca','entero',autogenerado=True), C('nombre_marca','Marca'))),
        Tabla('Linea_Estilo', 'Líneas / estilos', 'Maestras', 'id_linea', (
            C('id_linea','ID línea','entero',autogenerado=True), C('descripcion_estilo','Estilo'))),
        Tabla('Estatus_Producto', 'Estatus de producto', 'Maestras', 'id_estatus_producto', (
            C('id_estatus_producto','ID estatus','entero',autogenerado=True), C('nombre_estatus','Estatus'))),
        Tabla('Talla', 'Tallas', 'Maestras', 'id_talla', (
            C('id_talla','ID talla','entero',autogenerado=True), C('numero_talla','Número de talla','numero'),
            C('clasificacion_talla','Clasificación'))),
        Tabla('Forma_Pago', 'Formas de pago', 'Maestras', 'id_forma_pago', (
            C('id_forma_pago','ID forma de pago','entero',autogenerado=True), C('descripcion_pago','Forma de pago'))),
        Tabla('Producto', 'Productos', 'Operativas', 'id_producto', (
            C('id_producto','ID producto','entero',autogenerado=True),
            C('id_categoria','Categoría','entero',fk='Categoria'), C('id_marca','Marca','entero',fk='Marca'),
            C('id_linea','Línea de estilo','entero',fk='Linea_Estilo'),
            C('id_estatus_producto','Estatus','entero',fk='Estatus_Producto'),
            C('codigo','Código / SKU'), C('nombre_modelo','Modelo'),
            C('descripcion_producto','Descripción',requerido=False), C('precio_venta','Precio','precio'),
            C('color','Color'), C('material','Material'), C('imagen','Ruta de imagen',requerido=False))),
        Tabla('Usuario', 'Usuarios', 'Operativas', 'id_usuario', (
            C('id_usuario','ID usuario','entero',autogenerado=True),
            C('id_tipo_usuario','Rol','entero',fk='Tipo_Usuario'),
            C('nombre','Nombre'), C('apellido_paterno','Apellido paterno'),
            C('apellido_materno','Apellido materno',requerido=False),
            C('correo_electronico','Correo electrónico'),
            C('contrasena','Contraseña',secreto=True),
            C('telefono','Teléfono',requerido=False),
            C('estatus_activo','Activo','booleano',requerido=False,defecto=True)),
            editable=False, nota='Sólo consulta: la gestión de credenciales requiere contraseñas seguras y permisos.'),
        Tabla('Inventario', 'Inventario', 'Operativas', 'id_inventario', (
            C('id_inventario','ID inventario','entero',autogenerado=True),
            C('id_producto','Producto','entero',fk='Producto'), C('id_talla','Talla','entero',fk='Talla'),
            C('stock_disponible','Stock disponible','entero'), C('stock_minimo_alerta','Mínimo alerta','entero',defecto=True),
            C('ubicacion_estante_bodega','Ubicación bodega')),
            editable=False, nota='Sólo consulta: los movimientos requieren control de existencias.'),
        Tabla('Venta', 'Ventas', 'Operativas', 'id_venta', (
            C('id_venta','ID venta','entero',autogenerado=True),
            C('id_usuario','Usuario','entero',fk='Usuario'), C('id_forma_pago','Forma de pago','entero',fk='Forma_Pago'),
            C('fecha_venta','Fecha de venta','fecha',requerido=False,defecto=True),
            C('monto_subtotal','Subtotal','precio'), C('monto_iva','IVA','precio'), C('monto_total','Total','precio')),
            editable=False, nota='Sólo consulta: las ventas deben registrarse con su detalle y cálculos consistentes.'),
        Tabla('Detalle_Venta', 'Detalle de ventas', 'Operativas', 'id_detalle_venta', (
            C('id_detalle_venta','ID detalle','entero',autogenerado=True),
            C('id_venta','Venta','entero',fk='Venta'), C('id_inventario','Inventario','entero',fk='Inventario'),
            C('cantidad_vendida','Cantidad vendida','entero'),
            C('precio_unitario_historico','Precio unitario','precio'),
            C('subtotal_linea','Subtotal línea','precio',autogenerado=True)),
            editable=False, nota='Sólo consulta: subtotal calculado y consistencia con Venta/Inventario.'),
    )
}

MAESTRAS = [t for t in TABLAS.values() if t.grupo == 'Maestras']
OPERATIVAS = [t for t in TABLAS.values() if t.grupo == 'Operativas']


def ligas_de(tabla):
    """Relaciones definidas realmente en los scripts SQL: FK salientes y entrantes."""
    actual = TABLAS[tabla]
    salientes = [(actual.nombre, c.nombre, c.fk, TABLAS[c.fk].pk) for c in actual.campos if c.fk]
    entrantes = [(otra.nombre, c.nombre, actual.nombre, actual.pk)
                 for otra in TABLAS.values() for c in otra.campos if c.fk == tabla]
    return salientes, entrantes
