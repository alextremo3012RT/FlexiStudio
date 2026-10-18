/*
 Autor: Alex Rivera Tapia
 Tema: Base de Datos Flexi Zamora - Script Unificado de Creacion e Inserciones (SQL Server)
 Fecha original: 16 de Septiembre del 2026
 Contenido: 12 tablas, registros originales y ampliacion de demostracion.

 INSTRUCCIONES:
 - Ejecutar en SQL Server Management Studio (SSMS), en una ventana de consulta.
 - Requiere permisos para CREATE DATABASE en el servidor.
 - Si FlexiZamora ya existe, este script no ejecuta las inserciones.
 - Tras el aviso de base existente, abra una ventana de consulta nueva en SSMS.
 - Para usarlo en otra computadora, la base de datos no debe existir previamente.
 - Las contrasenas del script original son ejemplos, NO hashes validos para iniciar sesion.
   Activar la cuenta del administrador desde el programa antes de usar el login.
 - Los nuevos modelos y marcas son ficticios para demostraciones academicas.
*/

-- ====================================================
-- PREPARACION DE LA BASE DE DATOS
-- ====================================================
USE master;
GO

-- Seguridad: no eliminar bases de datos que ya contienen informacion.
IF DB_ID('FlexiZamora') IS NOT NULL
BEGIN
    RAISERROR('FlexiZamora ya existe. No se ejecutara este script para evitar perdida de datos.', 16, 1);
    SET NOEXEC ON; -- Detiene tambien los lotes posteriores (GO).
END
GO

-- CREAR Y USAR BASE DE DATOS
CREATE DATABASE FlexiZamora;
GO

USE FlexiZamora;
GO

-- ====================================================
-- MÓDULO 1: CONTROL DE ACCESO Y USUARIOS
-- ====================================================

-- 1. Crear tabla Tipo_Usuario
CREATE TABLE Tipo_Usuario (
    id_tipo_usuario INTEGER NOT NULL IDENTITY(1,1),
    nombre_rol VARCHAR(30) NOT NULL,
    descripcion_permisos VARCHAR(150),
    PRIMARY KEY (id_tipo_usuario)
);

-- 2. Crear tabla Usuario
CREATE TABLE Usuario (
    id_usuario INTEGER NOT NULL IDENTITY(1,1),
    id_tipo_usuario INTEGER NOT NULL,
    nombre VARCHAR(30) NOT NULL,
    apellido_paterno VARCHAR(30) NOT NULL,
    apellido_materno VARCHAR(30),
    correo_electronico VARCHAR(100) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    estatus_activo BIT DEFAULT(1),
    PRIMARY KEY (id_usuario),
    FOREIGN KEY (id_tipo_usuario) REFERENCES Tipo_Usuario(id_tipo_usuario)
);
GO

-- Insertar Tipos de Usuario (Catálogo)
INSERT INTO Tipo_Usuario (nombre_rol, descripcion_permisos) VALUES
('Administrador', 'Acceso total al sistema, configuraciones y reportes'),
('Gerente', 'Gestion de inventarios, reportes de ventas y personal'),
('Vendedor', 'Atencion en punto de venta y consulta de stock'),
('Almacenista', 'Control de entradas, salidas y ubicaciones en bodega'),
('Cajero', 'Cobro de ventas y corte de caja');

-- Insertar Usuarios (5 registros)
INSERT INTO Usuario (id_tipo_usuario, nombre, apellido_paterno, apellido_materno, correo_electronico, contrasena, telefono, estatus_activo) VALUES
(1, 'Alex', 'Rivera', 'Tapia', 'alex.rivera@flexizamora.com', 'hash_admin123', '3511234567', 1),
(2, 'Fernanda', 'Gomez', 'Lopez', 'fer.gomez@flexizamora.com', 'hash_gerente2026', '3512345678', 1),
(3, 'Carlos', 'Mendoza', 'Perez', 'carlos.m@flexizamora.com', 'hash_vend123', '3513456789', 1),
(4, 'Sofia', 'Hernandez', 'Torres', 'sofia.h@flexizamora.com', 'hash_almacen1', '3514567890', 1),
(5, 'Luis', 'Ramirez', 'Sanchez', 'luis.r@flexizamora.com', 'hash_caja123', '3515678901', 1);
GO

-- ====================================================
-- MÓDULO 2: CATÁLOGO DE CALZADO
-- ====================================================

-- 3. Crear tabla Categoria
CREATE TABLE Categoria (
    id_categoria INTEGER NOT NULL IDENTITY(1,1),
    nombre_categoria VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_categoria)
);

-- 4. Crear tabla Marca
CREATE TABLE Marca (
    id_marca INTEGER NOT NULL IDENTITY(1,1),
    nombre_marca VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_marca)
);

-- 5. Crear tabla Linea_Estilo
CREATE TABLE Linea_Estilo (
    id_linea INTEGER NOT NULL IDENTITY(1,1),
    descripcion_estilo VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_linea)
);

-- 6. Crear tabla Estatus_Producto
CREATE TABLE Estatus_Producto (
    id_estatus_producto INTEGER NOT NULL IDENTITY(1,1),
    nombre_estatus VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_estatus_producto)
);

-- 7. Crear tabla Producto
CREATE TABLE Producto (
    id_producto INTEGER NOT NULL IDENTITY(1,1),
    id_categoria INTEGER NOT NULL,
    id_marca INTEGER NOT NULL,
    id_linea INTEGER NOT NULL,
    id_estatus_producto INTEGER NOT NULL,
    codigo VARCHAR(30) NOT NULL,
    nombre_modelo VARCHAR(80) NOT NULL,
    descripcion_producto VARCHAR(200),
    precio_venta DECIMAL(10,2) NOT NULL CHECK(precio_venta > 0),
    color VARCHAR(30) NOT NULL,
    material VARCHAR(30) NOT NULL,
    imagen VARCHAR(200),
    PRIMARY KEY (id_producto),
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria),
    FOREIGN KEY (id_marca) REFERENCES Marca(id_marca),
    FOREIGN KEY (id_linea) REFERENCES Linea_Estilo(id_linea),
    FOREIGN KEY (id_estatus_producto) REFERENCES Estatus_Producto(id_estatus_producto)
);
GO

-- Insertar Categorias
INSERT INTO Categoria (nombre_categoria) VALUES
('Dama'),
('Caballero'),
('Escolar'),
('Infantil Dama'),
('Infantil Caballero');

-- Ampliacion de Categoria (12 registros adicionales)
INSERT INTO Categoria (nombre_categoria) VALUES
    ('Dama Deportiva'),
    ('Caballero Deportivo'),
    ('Unisex'),
    ('Senderismo'),
    ('Running'),
    ('Urbano'),
    ('Sandalias'),
    ('Seguridad Industrial'),
    ('Ceremonia'),
    ('Juvenil'),
    ('Primeros Pasos'),
    ('Outdoor');

-- Insertar Marcas
INSERT INTO Marca (nombre_marca) VALUES
('Flexi'),
('Flexi Country'),
('Quirelli'),
('Flexi Youth'),
('Flexi Work');

-- Ampliacion de Marca (8 registros adicionales)
INSERT INTO Marca (nombre_marca) VALUES
    ('Flexi Move'),
    ('Flexi Active'),
    ('Flexi Urban'),
    ('Flexi Comfort'),
    ('Flexi Kids'),
    ('Flexi Trail'),
    ('Flexi Studio'),
    ('Flexi Pro');

-- Insertar Linea / Estilo
INSERT INTO Linea_Estilo (descripcion_estilo) VALUES
('Casual'),
('Formal'),
('Confort'),
('Deportivo'),
('Botas y Botines');

-- Ampliacion de Linea_Estilo (12 registros adicionales)
INSERT INTO Linea_Estilo (descripcion_estilo) VALUES
    ('Tenis Urbanos'),
    ('Running Ligero'),
    ('Slip On'),
    ('Skate Casual'),
    ('Senderismo'),
    ('Minimalista'),
    ('Retro Deportivo'),
    ('Plataforma'),
    ('Trail'),
    ('Training'),
    ('Sandalia Deportiva'),
    ('Mocasin Moderno');

-- Insertar Estatus de Producto
INSERT INTO Estatus_Producto (nombre_estatus) VALUES
('Activo'),
('Agotado'),
('Descontinuado'),
('En Promocion'),
('Proximamente');

-- Ampliacion de Estatus_Producto (2 registros adicionales)
INSERT INTO Estatus_Producto (nombre_estatus) VALUES
    ('Edicion Limitada'),
    ('Temporada Actual');

-- Insertar Productos (10 registros)
INSERT INTO Producto (id_categoria, id_marca, id_linea, id_estatus_producto, codigo, nombre_modelo, descripcion_producto, precio_venta, color, material, imagen) VALUES
(2, 1, 1, 1, 'FLX-40201', 'Mocasin Casual Clasico', 'Mocasin de piel vacuno suave con suela ligera', 1299.00, 'Negro', 'Piel', 'img/40201_negro.jpg'),
(2, 1, 2, 1, 'FLX-40202', 'Zapato Formal Oxford', 'Calzado elegante de amarrar ideal para oficina', 1499.00, 'Cafe', 'Piel', 'img/40202_cafe.jpg'),
(1, 1, 3, 1, 'FLX-10101', 'Balerina Confort Soft', 'Calzado comodo con plantilla acojinada para dama', 999.00, 'Beige', 'Piel', 'img/10101_beige.jpg'),
(1, 2, 5, 1, 'FLX-10502', 'Bota Outdoor Dama', 'Bota resistente con suela antiderrapante', 1699.00, 'Miel', 'Nobuck', 'img/10502_miel.jpg'),
(2, 2, 5, 1, 'FLX-50101', 'Botin Country Hombre', 'Botin robusto de piel con ajuste de agujetas', 1899.00, 'Tan', 'Piel', 'img/50101_tan.jpg'),
(3, 1, 2, 1, 'FLX-30101', 'Zapato Escolar Juvenil', 'Zapato escolar resistente para uso diario', 899.00, 'Negro', 'Piel', 'img/30101_negro.jpg'),
(2, 1, 4, 4, 'FLX-40801', 'Sneaker Urbano Casual', 'Tenis casual urbano de piel con plantilla removible', 1199.00, 'Blanco', 'Piel', 'img/40801_blanco.jpg'),
(1, 1, 1, 1, 'FLX-10205', 'Sandalia Confort Dama', 'Sandalia ligera de piel con cuña baja', 849.00, 'Azul Marino', 'Piel', 'img/10205_azul.jpg'),
(2, 5, 3, 1, 'FLX-90101', 'Calzado Antiderrapante Trabajo', 'Zapato de trabajo industrial ligero', 1599.00, 'Negro', 'Piel', 'img/90101_negro.jpg'),
(4, 4, 1, 1, 'FLX-70101', 'Zapato Niña Casual', 'Calzado infantil flexible con ajuste de velcro', 749.00, 'Rosa', 'Sintetico', 'img/70101_rosa.jpg');


-- Ampliacion de Productos (75 modelos ficticios para pruebas academicas)
-- Se enlazan por el nombre de sus catalogos, no por IDs escritos a mano.
INSERT INTO Producto (
    id_categoria, id_marca, id_linea, id_estatus_producto,
    codigo, nombre_modelo, descripcion_producto,
    precio_venta, color, material, imagen
)
SELECT
    c.id_categoria, m.id_marca, le.id_linea, ep.id_estatus_producto,
    demo.codigo, demo.modelo, demo.descripcion, demo.precio,
    demo.color, demo.material, demo.imagen
FROM (VALUES
    ('Dama Deportiva', 'Flexi', 'Deportivo', 'Activo',
     'FLX-DEMO-0001', 'Aero Sprint Low', 'Modelo de demostracion Aero Sprint Low, acabado negro mate, confeccion malla textil, ideal para uso diario.', 699.00,
     'Negro Mate', 'Malla Textil', 'img/demo_flx-demo-0001.jpg'),
    ('Caballero Deportivo', 'Flexi Comfort', 'Slip On', 'Activo',
     'FLX-DEMO-0002', 'Nova Street Low', 'Modelo de demostracion Nova Street Low, acabado terracota, confeccion textil reciclado, ideal para uso diario.', 836.00,
     'Terracota', 'Textil Reciclado', 'img/demo_flx-demo-0002.jpg'),
    ('Unisex', 'Flexi Youth', 'Plataforma', 'Activo',
     'FLX-DEMO-0003', 'Brisa Motion Low', 'Modelo de demostracion Brisa Motion Low, acabado chocolate, confeccion piel vegana, ideal para uso diario.', 973.00,
     'Chocolate', 'Piel Vegana', 'img/demo_flx-demo-0003.jpg'),
    ('Senderismo', 'Flexi Trail', 'Deportivo', 'En Promocion',
     'FLX-DEMO-0004', 'Lumen Runner Low', 'Modelo de demostracion Lumen Runner Low, acabado taupe, confeccion nobuck, ideal para uso diario.', 1110.00,
     'Taupe', 'Nobuck', 'img/demo_flx-demo-0004.jpg'),
    ('Running', 'Flexi Move', 'Slip On', 'Proximamente',
     'FLX-DEMO-0005', 'Nexo Retro Low', 'Modelo de demostracion Nexo Retro Low, acabado turquesa, confeccion lona, ideal para uso diario.', 1247.00,
     'Turquesa', 'Lona', 'img/demo_flx-demo-0005.jpg'),
    ('Urbano', 'Flexi Pro', 'Plataforma', 'Agotado',
     'FLX-DEMO-0006', 'Terra Walk Low', 'Modelo de demostracion Terra Walk Low, acabado gris grafito, confeccion piel sintetica, ideal para uso diario.', 1384.00,
     'Gris Grafito', 'Piel Sintetica', 'img/demo_flx-demo-0006.jpg'),
    ('Juvenil', 'Flexi Urban', 'Deportivo', 'Edicion Limitada',
     'FLX-DEMO-0007', 'Aura Flex Low', 'Modelo de demostracion Aura Flex Low, acabado rosa palo, confeccion tejido knit, ideal para uso diario.', 1521.00,
     'Rosa Palo', 'Tejido Knit', 'img/demo_flx-demo-0007.jpg'),
    ('Outdoor', 'Flexi Country', 'Slip On', 'Temporada Actual',
     'FLX-DEMO-0008', 'Pulse City Low', 'Modelo de demostracion Pulse City Low, acabado naranja quemado, confeccion mesh transpirable, ideal para uso diario.', 1658.00,
     'Naranja Quemado', 'Mesh Transpirable', 'img/demo_flx-demo-0008.jpg'),
    ('Dama', 'Flexi Kids', 'Plataforma', 'Activo',
     'FLX-DEMO-0009', 'Vector One Low', 'Modelo de demostracion Vector One Low, acabado grafito, confeccion gamuza, ideal para uso diario.', 1795.00,
     'Grafito', 'Gamuza', 'img/demo_flx-demo-0009.jpg'),
    ('Caballero', 'Flexi Work', 'Deportivo', 'Activo',
     'FLX-DEMO-0010', 'Orion Trail Low', 'Modelo de demostracion Orion Trail Low, acabado verde olivo, confeccion sintetico, ideal para uso diario.', 1932.00,
     'Verde Olivo', 'Sintetico', 'img/demo_flx-demo-0010.jpg'),
    ('Escolar', 'Flexi Studio', 'Slip On', 'Activo',
     'FLX-DEMO-0011', 'Viva Flow Low', 'Modelo de demostracion Viva Flow Low, acabado mostaza, confeccion piel, ideal para uso diario.', 2069.00,
     'Mostaza', 'Piel', 'img/demo_flx-demo-0011.jpg'),
    ('Infantil Dama', 'Flexi Active', 'Plataforma', 'En Promocion',
     'FLX-DEMO-0012', 'Ritmo Pro Low', 'Modelo de demostracion Ritmo Pro Low, acabado champan, confeccion microfibra, ideal para uso diario.', 2206.00,
     'Champan', 'Microfibra', 'img/demo_flx-demo-0012.jpg'),
    ('Infantil Caballero', 'Flexi', 'Deportivo', 'Proximamente',
     'FLX-DEMO-0013', 'Atlas Trek Low', 'Modelo de demostracion Atlas Trek Low, acabado fucsia, confeccion malla textil, ideal para uso diario.', 2343.00,
     'Fucsia', 'Malla Textil', 'img/demo_flx-demo-0013.jpg'),
    ('Dama Deportiva', 'Flexi Comfort', 'Slip On', 'Agotado',
     'FLX-DEMO-0014', 'Luna Shift Low', 'Modelo de demostracion Luna Shift Low, acabado blanco hueso, confeccion textil reciclado, ideal para uso diario.', 2480.00,
     'Blanco Hueso', 'Textil Reciclado', 'img/demo_flx-demo-0014.jpg'),
    ('Caballero Deportivo', 'Flexi Youth', 'Plataforma', 'Edicion Limitada',
     'FLX-DEMO-0015', 'Neo Classic Low', 'Modelo de demostracion Neo Classic Low, acabado lavanda, confeccion piel vegana, ideal para uso diario.', 817.00,
     'Lavanda', 'Piel Vegana', 'img/demo_flx-demo-0015.jpg'),
    ('Unisex', 'Flexi Trail', 'Deportivo', 'Temporada Actual',
     'FLX-DEMO-0016', 'Delta Move Low', 'Modelo de demostracion Delta Move Low, acabado borgona, confeccion nobuck, ideal para uso diario.', 954.00,
     'Borgona', 'Nobuck', 'img/demo_flx-demo-0016.jpg'),
    ('Senderismo', 'Flexi Move', 'Slip On', 'Activo',
     'FLX-DEMO-0017', 'Solar Glide Low', 'Modelo de demostracion Solar Glide Low, acabado azul acero, confeccion lona, ideal para uso diario.', 1091.00,
     'Azul Acero', 'Lona', 'img/demo_flx-demo-0017.jpg'),
    ('Running', 'Flexi Pro', 'Plataforma', 'Activo',
     'FLX-DEMO-0018', 'Zenith Pace Low', 'Modelo de demostracion Zenith Pace Low, acabado ciruela, confeccion piel sintetica, ideal para uso diario.', 1228.00,
     'Ciruela', 'Piel Sintetica', 'img/demo_flx-demo-0018.jpg'),
    ('Urbano', 'Flexi Urban', 'Deportivo', 'Activo',
     'FLX-DEMO-0019', 'Prisma Low Low', 'Modelo de demostracion Prisma Low Low, acabado arena, confeccion tejido knit, ideal para uso diario.', 1365.00,
     'Arena', 'Tejido Knit', 'img/demo_flx-demo-0019.jpg'),
    ('Juvenil', 'Flexi Country', 'Slip On', 'En Promocion',
     'FLX-DEMO-0020', 'Eco Step Low', 'Modelo de demostracion Eco Step Low, acabado verde menta, confeccion mesh transpirable, ideal para uso diario.', 1502.00,
     'Verde Menta', 'Mesh Transpirable', 'img/demo_flx-demo-0020.jpg'),
    ('Outdoor', 'Flexi Kids', 'Plataforma', 'Proximamente',
     'FLX-DEMO-0021', 'Cima Trail Low', 'Modelo de demostracion Cima Trail Low, acabado marfil, confeccion gamuza, ideal para uso diario.', 1639.00,
     'Marfil', 'Gamuza', 'img/demo_flx-demo-0021.jpg'),
    ('Dama', 'Flexi Work', 'Deportivo', 'Agotado',
     'FLX-DEMO-0022', 'Cobalt Rush Low', 'Modelo de demostracion Cobalt Rush Low, acabado crema, confeccion sintetico, ideal para uso diario.', 1776.00,
     'Crema', 'Sintetico', 'img/demo_flx-demo-0022.jpg'),
    ('Caballero', 'Flexi Studio', 'Slip On', 'Edicion Limitada',
     'FLX-DEMO-0023', 'Arco Sport Low', 'Modelo de demostracion Arco Sport Low, acabado rojo vino, confeccion piel, ideal para uso diario.', 1913.00,
     'Rojo Vino', 'Piel', 'img/demo_flx-demo-0023.jpg'),
    ('Escolar', 'Flexi Active', 'Plataforma', 'Temporada Actual',
     'FLX-DEMO-0024', 'Tempo Urban Low', 'Modelo de demostracion Tempo Urban Low, acabado azul cobalto, confeccion microfibra, ideal para uso diario.', 2050.00,
     'Azul Cobalto', 'Microfibra', 'img/demo_flx-demo-0024.jpg'),
    ('Infantil Dama', 'Flexi', 'Deportivo', 'Activo',
     'FLX-DEMO-0025', 'Duna Soft Low', 'Modelo de demostracion Duna Soft Low, acabado azul cielo, confeccion malla textil, ideal para uso diario.', 2187.00,
     'Azul Cielo', 'Malla Textil', 'img/demo_flx-demo-0025.jpg'),
    ('Infantil Caballero', 'Flexi Comfort', 'Slip On', 'Activo',
     'FLX-DEMO-0026', 'Aero Sprint Mid', 'Modelo de demostracion Aero Sprint Mid, acabado cobre, confeccion textil reciclado, ideal para uso diario.', 2324.00,
     'Cobre', 'Textil Reciclado', 'img/demo_flx-demo-0026.jpg'),
    ('Dama Deportiva', 'Flexi Youth', 'Plataforma', 'Activo',
     'FLX-DEMO-0027', 'Nova Street Mid', 'Modelo de demostracion Nova Street Mid, acabado azul petroleo, confeccion piel vegana, ideal para uso diario.', 2461.00,
     'Azul Petroleo', 'Piel Vegana', 'img/demo_flx-demo-0027.jpg'),
    ('Caballero Deportivo', 'Flexi Trail', 'Deportivo', 'En Promocion',
     'FLX-DEMO-0028', 'Brisa Motion Mid', 'Modelo de demostracion Brisa Motion Mid, acabado coral, confeccion nobuck, ideal para uso diario.', 798.00,
     'Coral', 'Nobuck', 'img/demo_flx-demo-0028.jpg'),
    ('Unisex', 'Flexi Move', 'Slip On', 'Proximamente',
     'FLX-DEMO-0029', 'Lumen Runner Mid', 'Modelo de demostracion Lumen Runner Mid, acabado plata, confeccion lona, ideal para uso diario.', 935.00,
     'Plata', 'Lona', 'img/demo_flx-demo-0029.jpg'),
    ('Senderismo', 'Flexi Pro', 'Plataforma', 'Agotado',
     'FLX-DEMO-0030', 'Nexo Retro Mid', 'Modelo de demostracion Nexo Retro Mid, acabado verde bosque, confeccion piel sintetica, ideal para uso diario.', 1072.00,
     'Verde Bosque', 'Piel Sintetica', 'img/demo_flx-demo-0030.jpg'),
    ('Running', 'Flexi Urban', 'Deportivo', 'Edicion Limitada',
     'FLX-DEMO-0031', 'Terra Walk Mid', 'Modelo de demostracion Terra Walk Mid, acabado negro mate, confeccion tejido knit, ideal para uso diario.', 1209.00,
     'Negro Mate', 'Tejido Knit', 'img/demo_flx-demo-0031.jpg'),
    ('Urbano', 'Flexi Country', 'Slip On', 'Temporada Actual',
     'FLX-DEMO-0032', 'Aura Flex Mid', 'Modelo de demostracion Aura Flex Mid, acabado terracota, confeccion mesh transpirable, ideal para uso diario.', 1346.00,
     'Terracota', 'Mesh Transpirable', 'img/demo_flx-demo-0032.jpg'),
    ('Juvenil', 'Flexi Kids', 'Plataforma', 'Activo',
     'FLX-DEMO-0033', 'Pulse City Mid', 'Modelo de demostracion Pulse City Mid, acabado chocolate, confeccion gamuza, ideal para uso diario.', 1483.00,
     'Chocolate', 'Gamuza', 'img/demo_flx-demo-0033.jpg'),
    ('Outdoor', 'Flexi Work', 'Deportivo', 'Activo',
     'FLX-DEMO-0034', 'Vector One Mid', 'Modelo de demostracion Vector One Mid, acabado taupe, confeccion sintetico, ideal para uso diario.', 1620.00,
     'Taupe', 'Sintetico', 'img/demo_flx-demo-0034.jpg'),
    ('Dama', 'Flexi Studio', 'Slip On', 'Activo',
     'FLX-DEMO-0035', 'Orion Trail Mid', 'Modelo de demostracion Orion Trail Mid, acabado turquesa, confeccion piel, ideal para uso diario.', 1757.00,
     'Turquesa', 'Piel', 'img/demo_flx-demo-0035.jpg'),
    ('Caballero', 'Flexi Active', 'Plataforma', 'En Promocion',
     'FLX-DEMO-0036', 'Viva Flow Mid', 'Modelo de demostracion Viva Flow Mid, acabado gris grafito, confeccion microfibra, ideal para uso diario.', 1894.00,
     'Gris Grafito', 'Microfibra', 'img/demo_flx-demo-0036.jpg'),
    ('Escolar', 'Flexi', 'Deportivo', 'Proximamente',
     'FLX-DEMO-0037', 'Ritmo Pro Mid', 'Modelo de demostracion Ritmo Pro Mid, acabado rosa palo, confeccion malla textil, ideal para uso diario.', 2031.00,
     'Rosa Palo', 'Malla Textil', 'img/demo_flx-demo-0037.jpg'),
    ('Infantil Dama', 'Flexi Comfort', 'Slip On', 'Agotado',
     'FLX-DEMO-0038', 'Atlas Trek Mid', 'Modelo de demostracion Atlas Trek Mid, acabado naranja quemado, confeccion textil reciclado, ideal para uso diario.', 2168.00,
     'Naranja Quemado', 'Textil Reciclado', 'img/demo_flx-demo-0038.jpg'),
    ('Infantil Caballero', 'Flexi Youth', 'Plataforma', 'Edicion Limitada',
     'FLX-DEMO-0039', 'Luna Shift Mid', 'Modelo de demostracion Luna Shift Mid, acabado grafito, confeccion piel vegana, ideal para uso diario.', 2305.00,
     'Grafito', 'Piel Vegana', 'img/demo_flx-demo-0039.jpg'),
    ('Dama Deportiva', 'Flexi Trail', 'Deportivo', 'Temporada Actual',
     'FLX-DEMO-0040', 'Neo Classic Mid', 'Modelo de demostracion Neo Classic Mid, acabado verde olivo, confeccion nobuck, ideal para uso diario.', 2442.00,
     'Verde Olivo', 'Nobuck', 'img/demo_flx-demo-0040.jpg'),
    ('Caballero Deportivo', 'Flexi Move', 'Slip On', 'Activo',
     'FLX-DEMO-0041', 'Delta Move Mid', 'Modelo de demostracion Delta Move Mid, acabado mostaza, confeccion lona, ideal para uso diario.', 779.00,
     'Mostaza', 'Lona', 'img/demo_flx-demo-0041.jpg'),
    ('Unisex', 'Flexi Pro', 'Plataforma', 'Activo',
     'FLX-DEMO-0042', 'Solar Glide Mid', 'Modelo de demostracion Solar Glide Mid, acabado champan, confeccion piel sintetica, ideal para uso diario.', 916.00,
     'Champan', 'Piel Sintetica', 'img/demo_flx-demo-0042.jpg'),
    ('Senderismo', 'Flexi Urban', 'Deportivo', 'Activo',
     'FLX-DEMO-0043', 'Zenith Pace Mid', 'Modelo de demostracion Zenith Pace Mid, acabado fucsia, confeccion tejido knit, ideal para uso diario.', 1053.00,
     'Fucsia', 'Tejido Knit', 'img/demo_flx-demo-0043.jpg'),
    ('Running', 'Flexi Country', 'Slip On', 'En Promocion',
     'FLX-DEMO-0044', 'Prisma Low Mid', 'Modelo de demostracion Prisma Low Mid, acabado blanco hueso, confeccion mesh transpirable, ideal para uso diario.', 1190.00,
     'Blanco Hueso', 'Mesh Transpirable', 'img/demo_flx-demo-0044.jpg'),
    ('Urbano', 'Flexi Kids', 'Plataforma', 'Proximamente',
     'FLX-DEMO-0045', 'Eco Step Mid', 'Modelo de demostracion Eco Step Mid, acabado lavanda, confeccion gamuza, ideal para uso diario.', 1327.00,
     'Lavanda', 'Gamuza', 'img/demo_flx-demo-0045.jpg'),
    ('Juvenil', 'Flexi Work', 'Deportivo', 'Agotado',
     'FLX-DEMO-0046', 'Cima Trail Mid', 'Modelo de demostracion Cima Trail Mid, acabado borgona, confeccion sintetico, ideal para uso diario.', 1464.00,
     'Borgona', 'Sintetico', 'img/demo_flx-demo-0046.jpg'),
    ('Outdoor', 'Flexi Studio', 'Slip On', 'Edicion Limitada',
     'FLX-DEMO-0047', 'Cobalt Rush Mid', 'Modelo de demostracion Cobalt Rush Mid, acabado azul acero, confeccion piel, ideal para uso diario.', 1601.00,
     'Azul Acero', 'Piel', 'img/demo_flx-demo-0047.jpg'),
    ('Dama', 'Flexi Active', 'Plataforma', 'Temporada Actual',
     'FLX-DEMO-0048', 'Arco Sport Mid', 'Modelo de demostracion Arco Sport Mid, acabado ciruela, confeccion microfibra, ideal para uso diario.', 1738.00,
     'Ciruela', 'Microfibra', 'img/demo_flx-demo-0048.jpg'),
    ('Caballero', 'Flexi', 'Deportivo', 'Activo',
     'FLX-DEMO-0049', 'Tempo Urban Mid', 'Modelo de demostracion Tempo Urban Mid, acabado arena, confeccion malla textil, ideal para uso diario.', 1875.00,
     'Arena', 'Malla Textil', 'img/demo_flx-demo-0049.jpg'),
    ('Escolar', 'Flexi Comfort', 'Slip On', 'Activo',
     'FLX-DEMO-0050', 'Duna Soft Mid', 'Modelo de demostracion Duna Soft Mid, acabado verde menta, confeccion textil reciclado, ideal para uso diario.', 2012.00,
     'Verde Menta', 'Textil Reciclado', 'img/demo_flx-demo-0050.jpg'),
    ('Infantil Dama', 'Flexi Youth', 'Plataforma', 'Activo',
     'FLX-DEMO-0051', 'Aero Sprint Max', 'Modelo de demostracion Aero Sprint Max, acabado marfil, confeccion piel vegana, ideal para uso diario.', 2149.00,
     'Marfil', 'Piel Vegana', 'img/demo_flx-demo-0051.jpg'),
    ('Infantil Caballero', 'Flexi Trail', 'Deportivo', 'En Promocion',
     'FLX-DEMO-0052', 'Nova Street Max', 'Modelo de demostracion Nova Street Max, acabado crema, confeccion nobuck, ideal para uso diario.', 2286.00,
     'Crema', 'Nobuck', 'img/demo_flx-demo-0052.jpg'),
    ('Dama Deportiva', 'Flexi Move', 'Slip On', 'Proximamente',
     'FLX-DEMO-0053', 'Brisa Motion Max', 'Modelo de demostracion Brisa Motion Max, acabado rojo vino, confeccion lona, ideal para uso diario.', 2423.00,
     'Rojo Vino', 'Lona', 'img/demo_flx-demo-0053.jpg'),
    ('Caballero Deportivo', 'Flexi Pro', 'Plataforma', 'Agotado',
     'FLX-DEMO-0054', 'Lumen Runner Max', 'Modelo de demostracion Lumen Runner Max, acabado azul cobalto, confeccion piel sintetica, ideal para uso diario.', 760.00,
     'Azul Cobalto', 'Piel Sintetica', 'img/demo_flx-demo-0054.jpg'),
    ('Unisex', 'Flexi Urban', 'Deportivo', 'Edicion Limitada',
     'FLX-DEMO-0055', 'Nexo Retro Max', 'Modelo de demostracion Nexo Retro Max, acabado azul cielo, confeccion tejido knit, ideal para uso diario.', 897.00,
     'Azul Cielo', 'Tejido Knit', 'img/demo_flx-demo-0055.jpg'),
    ('Senderismo', 'Flexi Country', 'Slip On', 'Temporada Actual',
     'FLX-DEMO-0056', 'Terra Walk Max', 'Modelo de demostracion Terra Walk Max, acabado cobre, confeccion mesh transpirable, ideal para uso diario.', 1034.00,
     'Cobre', 'Mesh Transpirable', 'img/demo_flx-demo-0056.jpg'),
    ('Running', 'Flexi Kids', 'Plataforma', 'Activo',
     'FLX-DEMO-0057', 'Aura Flex Max', 'Modelo de demostracion Aura Flex Max, acabado azul petroleo, confeccion gamuza, ideal para uso diario.', 1171.00,
     'Azul Petroleo', 'Gamuza', 'img/demo_flx-demo-0057.jpg'),
    ('Urbano', 'Flexi Work', 'Deportivo', 'Activo',
     'FLX-DEMO-0058', 'Pulse City Max', 'Modelo de demostracion Pulse City Max, acabado coral, confeccion sintetico, ideal para uso diario.', 1308.00,
     'Coral', 'Sintetico', 'img/demo_flx-demo-0058.jpg'),
    ('Juvenil', 'Flexi Studio', 'Slip On', 'Activo',
     'FLX-DEMO-0059', 'Vector One Max', 'Modelo de demostracion Vector One Max, acabado plata, confeccion piel, ideal para uso diario.', 1445.00,
     'Plata', 'Piel', 'img/demo_flx-demo-0059.jpg'),
    ('Outdoor', 'Flexi Active', 'Plataforma', 'En Promocion',
     'FLX-DEMO-0060', 'Orion Trail Max', 'Modelo de demostracion Orion Trail Max, acabado verde bosque, confeccion microfibra, ideal para uso diario.', 1582.00,
     'Verde Bosque', 'Microfibra', 'img/demo_flx-demo-0060.jpg'),
    ('Dama', 'Flexi', 'Deportivo', 'Proximamente',
     'FLX-DEMO-0061', 'Viva Flow Max', 'Modelo de demostracion Viva Flow Max, acabado negro mate, confeccion malla textil, ideal para uso diario.', 1719.00,
     'Negro Mate', 'Malla Textil', 'img/demo_flx-demo-0061.jpg'),
    ('Caballero', 'Flexi Comfort', 'Slip On', 'Agotado',
     'FLX-DEMO-0062', 'Ritmo Pro Max', 'Modelo de demostracion Ritmo Pro Max, acabado terracota, confeccion textil reciclado, ideal para uso diario.', 1856.00,
     'Terracota', 'Textil Reciclado', 'img/demo_flx-demo-0062.jpg'),
    ('Escolar', 'Flexi Youth', 'Plataforma', 'Edicion Limitada',
     'FLX-DEMO-0063', 'Atlas Trek Max', 'Modelo de demostracion Atlas Trek Max, acabado chocolate, confeccion piel vegana, ideal para uso diario.', 1993.00,
     'Chocolate', 'Piel Vegana', 'img/demo_flx-demo-0063.jpg'),
    ('Infantil Dama', 'Flexi Trail', 'Deportivo', 'Temporada Actual',
     'FLX-DEMO-0064', 'Luna Shift Max', 'Modelo de demostracion Luna Shift Max, acabado taupe, confeccion nobuck, ideal para uso diario.', 2130.00,
     'Taupe', 'Nobuck', 'img/demo_flx-demo-0064.jpg'),
    ('Infantil Caballero', 'Flexi Move', 'Slip On', 'Activo',
     'FLX-DEMO-0065', 'Neo Classic Max', 'Modelo de demostracion Neo Classic Max, acabado turquesa, confeccion lona, ideal para uso diario.', 2267.00,
     'Turquesa', 'Lona', 'img/demo_flx-demo-0065.jpg'),
    ('Dama Deportiva', 'Flexi Pro', 'Plataforma', 'Activo',
     'FLX-DEMO-0066', 'Delta Move Max', 'Modelo de demostracion Delta Move Max, acabado gris grafito, confeccion piel sintetica, ideal para uso diario.', 2404.00,
     'Gris Grafito', 'Piel Sintetica', 'img/demo_flx-demo-0066.jpg'),
    ('Caballero Deportivo', 'Flexi Urban', 'Deportivo', 'Activo',
     'FLX-DEMO-0067', 'Solar Glide Max', 'Modelo de demostracion Solar Glide Max, acabado rosa palo, confeccion tejido knit, ideal para uso diario.', 741.00,
     'Rosa Palo', 'Tejido Knit', 'img/demo_flx-demo-0067.jpg'),
    ('Unisex', 'Flexi Country', 'Slip On', 'En Promocion',
     'FLX-DEMO-0068', 'Zenith Pace Max', 'Modelo de demostracion Zenith Pace Max, acabado naranja quemado, confeccion mesh transpirable, ideal para uso diario.', 878.00,
     'Naranja Quemado', 'Mesh Transpirable', 'img/demo_flx-demo-0068.jpg'),
    ('Senderismo', 'Flexi Kids', 'Plataforma', 'Proximamente',
     'FLX-DEMO-0069', 'Prisma Low Max', 'Modelo de demostracion Prisma Low Max, acabado grafito, confeccion gamuza, ideal para uso diario.', 1015.00,
     'Grafito', 'Gamuza', 'img/demo_flx-demo-0069.jpg'),
    ('Running', 'Flexi Work', 'Deportivo', 'Agotado',
     'FLX-DEMO-0070', 'Eco Step Max', 'Modelo de demostracion Eco Step Max, acabado verde olivo, confeccion sintetico, ideal para uso diario.', 1152.00,
     'Verde Olivo', 'Sintetico', 'img/demo_flx-demo-0070.jpg'),
    ('Urbano', 'Flexi Studio', 'Slip On', 'Edicion Limitada',
     'FLX-DEMO-0071', 'Cima Trail Max', 'Modelo de demostracion Cima Trail Max, acabado mostaza, confeccion piel, ideal para uso diario.', 1289.00,
     'Mostaza', 'Piel', 'img/demo_flx-demo-0071.jpg'),
    ('Juvenil', 'Flexi Active', 'Plataforma', 'Temporada Actual',
     'FLX-DEMO-0072', 'Cobalt Rush Max', 'Modelo de demostracion Cobalt Rush Max, acabado champan, confeccion microfibra, ideal para uso diario.', 1426.00,
     'Champan', 'Microfibra', 'img/demo_flx-demo-0072.jpg'),
    ('Outdoor', 'Flexi', 'Deportivo', 'Activo',
     'FLX-DEMO-0073', 'Arco Sport Max', 'Modelo de demostracion Arco Sport Max, acabado fucsia, confeccion malla textil, ideal para uso diario.', 1563.00,
     'Fucsia', 'Malla Textil', 'img/demo_flx-demo-0073.jpg'),
    ('Dama', 'Flexi Comfort', 'Slip On', 'Activo',
     'FLX-DEMO-0074', 'Tempo Urban Max', 'Modelo de demostracion Tempo Urban Max, acabado blanco hueso, confeccion textil reciclado, ideal para uso diario.', 1700.00,
     'Blanco Hueso', 'Textil Reciclado', 'img/demo_flx-demo-0074.jpg'),
    ('Caballero', 'Flexi Youth', 'Plataforma', 'Activo',
     'FLX-DEMO-0075', 'Duna Soft Max', 'Modelo de demostracion Duna Soft Max, acabado lavanda, confeccion piel vegana, ideal para uso diario.', 1837.00,
     'Lavanda', 'Piel Vegana', 'img/demo_flx-demo-0075.jpg')
) AS demo (
    categoria, marca, estilo, estatus, codigo, modelo,
    descripcion, precio, color, material, imagen
)
INNER JOIN Categoria AS c ON c.nombre_categoria = demo.categoria
INNER JOIN Marca AS m ON m.nombre_marca = demo.marca
INNER JOIN Linea_Estilo AS le ON le.descripcion_estilo = demo.estilo
INNER JOIN Estatus_Producto AS ep ON ep.nombre_estatus = demo.estatus;

GO

-- ====================================================
-- MÓDULO 3: TALLAS E INVENTARIO
-- ====================================================

-- 8. Crear tabla Talla
CREATE TABLE Talla (
    id_talla INTEGER NOT NULL IDENTITY(1,1),
    numero_talla DECIMAL(3,1) NOT NULL,
    clasificacion_talla VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_talla)
);

-- 9. Crear tabla Inventario
CREATE TABLE Inventario (
    id_inventario INTEGER NOT NULL IDENTITY(1,1),
    id_producto INTEGER NOT NULL,
    id_talla INTEGER NOT NULL,
    stock_disponible INTEGER NOT NULL CHECK(stock_disponible >= 0),
    stock_minimo_alerta INTEGER NOT NULL DEFAULT 2,
    ubicacion_estante_bodega VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_inventario),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    FOREIGN KEY (id_talla) REFERENCES Talla(id_talla)
);
GO

-- Insertar Tallas (Catálogo)
INSERT INTO Talla (numero_talla, clasificacion_talla) VALUES
(23.0, 'Dama / Juvenil'),
(24.0, 'Dama / Juvenil'),
(25.0, 'Dama / Caballero'),
(26.0, 'Caballero'),
(27.0, 'Caballero'),
(28.0, 'Caballero');

-- Ampliacion de Tallas (14 registros adicionales)
INSERT INTO Talla (numero_talla, clasificacion_talla) VALUES
    (18.0, 'Infantil'),
    (19.0, 'Infantil'),
    (20.0, 'Infantil'),
    (21.0, 'Infantil'),
    (22.0, 'Dama / Juvenil'),
    (22.5, 'Dama / Juvenil'),
    (23.5, 'Dama / Juvenil'),
    (24.5, 'Dama / Juvenil'),
    (25.5, 'Dama / Caballero'),
    (26.5, 'Dama / Caballero'),
    (27.5, 'Caballero'),
    (28.5, 'Caballero'),
    (29.5, 'Caballero'),
    (30.0, 'Caballero');

-- Insertar Inventario (10 registros)
INSERT INTO Inventario (id_producto, id_talla, stock_disponible, stock_minimo_alerta, ubicacion_estante_bodega) VALUES
(1, 4, 15, 3, 'Estante A-12'),
(1, 5, 12, 3, 'Estante A-13'),
(2, 5, 8, 2, 'Estante B-05'),
(2, 6, 10, 2, 'Estante B-06'),
(3, 1, 20, 5, 'Estante C-01'),
(3, 2, 18, 5, 'Estante C-02'),
(4, 2, 7, 2, 'Estante D-04'),
(5, 5, 9, 2, 'Estante D-08'),
(6, 3, 25, 5, 'Estante E-01'),
(7, 4, 14, 3, 'Estante F-03');


-- Ampliacion de Inventario (150 existencias: dos tallas por cada modelo nuevo)
-- La relacion se establece mediante codigo del producto y talla.
INSERT INTO Inventario (
    id_producto, id_talla, stock_disponible,
    stock_minimo_alerta, ubicacion_estante_bodega
)
SELECT p.id_producto, t.id_talla, demo.stock, demo.alerta, demo.ubicacion
FROM (VALUES
    ('FLX-DEMO-0001', 22.0, 'Dama / Juvenil', 0, 3, 'DEMO-A-01-1'),
    ('FLX-DEMO-0001', 23.5, 'Dama / Juvenil', 7, 3, 'DEMO-A-01-2'),
    ('FLX-DEMO-0002', 27.5, 'Caballero', 11, 3, 'DEMO-A-02-1'),
    ('FLX-DEMO-0002', 29.5, 'Caballero', 18, 3, 'DEMO-A-02-2'),
    ('FLX-DEMO-0003', 25.5, 'Dama / Caballero', 22, 3, 'DEMO-A-03-1'),
    ('FLX-DEMO-0003', 26.5, 'Dama / Caballero', 5, 3, 'DEMO-A-03-2'),
    ('FLX-DEMO-0004', 25.5, 'Dama / Caballero', 9, 3, 'DEMO-A-04-1'),
    ('FLX-DEMO-0004', 26.5, 'Dama / Caballero', 16, 3, 'DEMO-A-04-2'),
    ('FLX-DEMO-0005', 25.5, 'Dama / Caballero', 20, 3, 'DEMO-A-05-1'),
    ('FLX-DEMO-0005', 26.5, 'Dama / Caballero', 3, 3, 'DEMO-A-05-2'),
    ('FLX-DEMO-0006', 25.5, 'Dama / Caballero', 7, 3, 'DEMO-A-06-1'),
    ('FLX-DEMO-0006', 26.5, 'Dama / Caballero', 14, 3, 'DEMO-A-06-2'),
    ('FLX-DEMO-0007', 25.5, 'Dama / Caballero', 18, 3, 'DEMO-A-07-1'),
    ('FLX-DEMO-0007', 26.5, 'Dama / Caballero', 1, 3, 'DEMO-A-07-2'),
    ('FLX-DEMO-0008', 25.5, 'Dama / Caballero', 5, 3, 'DEMO-A-08-1'),
    ('FLX-DEMO-0008', 26.5, 'Dama / Caballero', 12, 3, 'DEMO-A-08-2'),
    ('FLX-DEMO-0009', 22.0, 'Dama / Juvenil', 16, 3, 'DEMO-A-09-1'),
    ('FLX-DEMO-0009', 23.5, 'Dama / Juvenil', 23, 3, 'DEMO-A-09-2'),
    ('FLX-DEMO-0010', 27.5, 'Caballero', 3, 3, 'DEMO-A-10-1'),
    ('FLX-DEMO-0010', 29.5, 'Caballero', 10, 3, 'DEMO-A-10-2'),
    ('FLX-DEMO-0011', 18.0, 'Infantil', 14, 3, 'DEMO-A-11-1'),
    ('FLX-DEMO-0011', 20.0, 'Infantil', 21, 3, 'DEMO-A-11-2'),
    ('FLX-DEMO-0012', 18.0, 'Infantil', 1, 3, 'DEMO-A-12-1'),
    ('FLX-DEMO-0012', 20.0, 'Infantil', 8, 3, 'DEMO-A-12-2'),
    ('FLX-DEMO-0013', 18.0, 'Infantil', 12, 3, 'DEMO-A-13-1'),
    ('FLX-DEMO-0013', 20.0, 'Infantil', 19, 3, 'DEMO-A-13-2'),
    ('FLX-DEMO-0014', 22.0, 'Dama / Juvenil', 23, 3, 'DEMO-A-14-1'),
    ('FLX-DEMO-0014', 23.5, 'Dama / Juvenil', 6, 3, 'DEMO-A-14-2'),
    ('FLX-DEMO-0015', 27.5, 'Caballero', 10, 3, 'DEMO-A-15-1'),
    ('FLX-DEMO-0015', 29.5, 'Caballero', 17, 3, 'DEMO-A-15-2'),
    ('FLX-DEMO-0016', 25.5, 'Dama / Caballero', 21, 3, 'DEMO-B-01-1'),
    ('FLX-DEMO-0016', 26.5, 'Dama / Caballero', 4, 3, 'DEMO-B-01-2'),
    ('FLX-DEMO-0017', 25.5, 'Dama / Caballero', 8, 3, 'DEMO-B-02-1'),
    ('FLX-DEMO-0017', 26.5, 'Dama / Caballero', 15, 3, 'DEMO-B-02-2'),
    ('FLX-DEMO-0018', 25.5, 'Dama / Caballero', 19, 3, 'DEMO-B-03-1'),
    ('FLX-DEMO-0018', 26.5, 'Dama / Caballero', 2, 3, 'DEMO-B-03-2'),
    ('FLX-DEMO-0019', 25.5, 'Dama / Caballero', 6, 3, 'DEMO-B-04-1'),
    ('FLX-DEMO-0019', 26.5, 'Dama / Caballero', 13, 3, 'DEMO-B-04-2'),
    ('FLX-DEMO-0020', 25.5, 'Dama / Caballero', 17, 3, 'DEMO-B-05-1'),
    ('FLX-DEMO-0020', 26.5, 'Dama / Caballero', 0, 3, 'DEMO-B-05-2'),
    ('FLX-DEMO-0021', 25.5, 'Dama / Caballero', 4, 3, 'DEMO-B-06-1'),
    ('FLX-DEMO-0021', 26.5, 'Dama / Caballero', 11, 3, 'DEMO-B-06-2'),
    ('FLX-DEMO-0022', 22.0, 'Dama / Juvenil', 15, 3, 'DEMO-B-07-1'),
    ('FLX-DEMO-0022', 23.5, 'Dama / Juvenil', 22, 3, 'DEMO-B-07-2'),
    ('FLX-DEMO-0023', 27.5, 'Caballero', 2, 3, 'DEMO-B-08-1'),
    ('FLX-DEMO-0023', 29.5, 'Caballero', 9, 3, 'DEMO-B-08-2'),
    ('FLX-DEMO-0024', 18.0, 'Infantil', 13, 3, 'DEMO-B-09-1'),
    ('FLX-DEMO-0024', 20.0, 'Infantil', 20, 3, 'DEMO-B-09-2'),
    ('FLX-DEMO-0025', 18.0, 'Infantil', 0, 3, 'DEMO-B-10-1'),
    ('FLX-DEMO-0025', 20.0, 'Infantil', 7, 3, 'DEMO-B-10-2'),
    ('FLX-DEMO-0026', 18.0, 'Infantil', 11, 3, 'DEMO-B-11-1'),
    ('FLX-DEMO-0026', 20.0, 'Infantil', 18, 3, 'DEMO-B-11-2'),
    ('FLX-DEMO-0027', 22.0, 'Dama / Juvenil', 22, 3, 'DEMO-B-12-1'),
    ('FLX-DEMO-0027', 23.5, 'Dama / Juvenil', 5, 3, 'DEMO-B-12-2'),
    ('FLX-DEMO-0028', 27.5, 'Caballero', 9, 3, 'DEMO-B-13-1'),
    ('FLX-DEMO-0028', 29.5, 'Caballero', 16, 3, 'DEMO-B-13-2'),
    ('FLX-DEMO-0029', 25.5, 'Dama / Caballero', 20, 3, 'DEMO-B-14-1'),
    ('FLX-DEMO-0029', 26.5, 'Dama / Caballero', 3, 3, 'DEMO-B-14-2'),
    ('FLX-DEMO-0030', 25.5, 'Dama / Caballero', 7, 3, 'DEMO-B-15-1'),
    ('FLX-DEMO-0030', 26.5, 'Dama / Caballero', 14, 3, 'DEMO-B-15-2'),
    ('FLX-DEMO-0031', 25.5, 'Dama / Caballero', 18, 3, 'DEMO-C-01-1'),
    ('FLX-DEMO-0031', 26.5, 'Dama / Caballero', 1, 3, 'DEMO-C-01-2'),
    ('FLX-DEMO-0032', 25.5, 'Dama / Caballero', 5, 3, 'DEMO-C-02-1'),
    ('FLX-DEMO-0032', 26.5, 'Dama / Caballero', 12, 3, 'DEMO-C-02-2'),
    ('FLX-DEMO-0033', 25.5, 'Dama / Caballero', 16, 3, 'DEMO-C-03-1'),
    ('FLX-DEMO-0033', 26.5, 'Dama / Caballero', 23, 3, 'DEMO-C-03-2'),
    ('FLX-DEMO-0034', 25.5, 'Dama / Caballero', 3, 3, 'DEMO-C-04-1'),
    ('FLX-DEMO-0034', 26.5, 'Dama / Caballero', 10, 3, 'DEMO-C-04-2'),
    ('FLX-DEMO-0035', 22.0, 'Dama / Juvenil', 14, 3, 'DEMO-C-05-1'),
    ('FLX-DEMO-0035', 23.5, 'Dama / Juvenil', 21, 3, 'DEMO-C-05-2'),
    ('FLX-DEMO-0036', 27.5, 'Caballero', 1, 3, 'DEMO-C-06-1'),
    ('FLX-DEMO-0036', 29.5, 'Caballero', 8, 3, 'DEMO-C-06-2'),
    ('FLX-DEMO-0037', 18.0, 'Infantil', 12, 3, 'DEMO-C-07-1'),
    ('FLX-DEMO-0037', 20.0, 'Infantil', 19, 3, 'DEMO-C-07-2'),
    ('FLX-DEMO-0038', 18.0, 'Infantil', 23, 3, 'DEMO-C-08-1'),
    ('FLX-DEMO-0038', 20.0, 'Infantil', 6, 3, 'DEMO-C-08-2'),
    ('FLX-DEMO-0039', 18.0, 'Infantil', 10, 3, 'DEMO-C-09-1'),
    ('FLX-DEMO-0039', 20.0, 'Infantil', 17, 3, 'DEMO-C-09-2'),
    ('FLX-DEMO-0040', 22.0, 'Dama / Juvenil', 21, 3, 'DEMO-C-10-1'),
    ('FLX-DEMO-0040', 23.5, 'Dama / Juvenil', 4, 3, 'DEMO-C-10-2'),
    ('FLX-DEMO-0041', 27.5, 'Caballero', 8, 3, 'DEMO-C-11-1'),
    ('FLX-DEMO-0041', 29.5, 'Caballero', 15, 3, 'DEMO-C-11-2'),
    ('FLX-DEMO-0042', 25.5, 'Dama / Caballero', 19, 3, 'DEMO-C-12-1'),
    ('FLX-DEMO-0042', 26.5, 'Dama / Caballero', 2, 3, 'DEMO-C-12-2'),
    ('FLX-DEMO-0043', 25.5, 'Dama / Caballero', 6, 3, 'DEMO-C-13-1'),
    ('FLX-DEMO-0043', 26.5, 'Dama / Caballero', 13, 3, 'DEMO-C-13-2'),
    ('FLX-DEMO-0044', 25.5, 'Dama / Caballero', 17, 3, 'DEMO-C-14-1'),
    ('FLX-DEMO-0044', 26.5, 'Dama / Caballero', 0, 3, 'DEMO-C-14-2'),
    ('FLX-DEMO-0045', 25.5, 'Dama / Caballero', 4, 3, 'DEMO-C-15-1'),
    ('FLX-DEMO-0045', 26.5, 'Dama / Caballero', 11, 3, 'DEMO-C-15-2'),
    ('FLX-DEMO-0046', 25.5, 'Dama / Caballero', 15, 3, 'DEMO-D-01-1'),
    ('FLX-DEMO-0046', 26.5, 'Dama / Caballero', 22, 3, 'DEMO-D-01-2'),
    ('FLX-DEMO-0047', 25.5, 'Dama / Caballero', 2, 3, 'DEMO-D-02-1'),
    ('FLX-DEMO-0047', 26.5, 'Dama / Caballero', 9, 3, 'DEMO-D-02-2'),
    ('FLX-DEMO-0048', 22.0, 'Dama / Juvenil', 13, 3, 'DEMO-D-03-1'),
    ('FLX-DEMO-0048', 23.5, 'Dama / Juvenil', 20, 3, 'DEMO-D-03-2'),
    ('FLX-DEMO-0049', 27.5, 'Caballero', 0, 3, 'DEMO-D-04-1'),
    ('FLX-DEMO-0049', 29.5, 'Caballero', 7, 3, 'DEMO-D-04-2'),
    ('FLX-DEMO-0050', 18.0, 'Infantil', 11, 3, 'DEMO-D-05-1'),
    ('FLX-DEMO-0050', 20.0, 'Infantil', 18, 3, 'DEMO-D-05-2'),
    ('FLX-DEMO-0051', 18.0, 'Infantil', 22, 3, 'DEMO-D-06-1'),
    ('FLX-DEMO-0051', 20.0, 'Infantil', 5, 3, 'DEMO-D-06-2'),
    ('FLX-DEMO-0052', 18.0, 'Infantil', 9, 3, 'DEMO-D-07-1'),
    ('FLX-DEMO-0052', 20.0, 'Infantil', 16, 3, 'DEMO-D-07-2'),
    ('FLX-DEMO-0053', 22.0, 'Dama / Juvenil', 20, 3, 'DEMO-D-08-1'),
    ('FLX-DEMO-0053', 23.5, 'Dama / Juvenil', 3, 3, 'DEMO-D-08-2'),
    ('FLX-DEMO-0054', 27.5, 'Caballero', 7, 3, 'DEMO-D-09-1'),
    ('FLX-DEMO-0054', 29.5, 'Caballero', 14, 3, 'DEMO-D-09-2'),
    ('FLX-DEMO-0055', 25.5, 'Dama / Caballero', 18, 3, 'DEMO-D-10-1'),
    ('FLX-DEMO-0055', 26.5, 'Dama / Caballero', 1, 3, 'DEMO-D-10-2'),
    ('FLX-DEMO-0056', 25.5, 'Dama / Caballero', 5, 3, 'DEMO-D-11-1'),
    ('FLX-DEMO-0056', 26.5, 'Dama / Caballero', 12, 3, 'DEMO-D-11-2'),
    ('FLX-DEMO-0057', 25.5, 'Dama / Caballero', 16, 3, 'DEMO-D-12-1'),
    ('FLX-DEMO-0057', 26.5, 'Dama / Caballero', 23, 3, 'DEMO-D-12-2'),
    ('FLX-DEMO-0058', 25.5, 'Dama / Caballero', 3, 3, 'DEMO-D-13-1'),
    ('FLX-DEMO-0058', 26.5, 'Dama / Caballero', 10, 3, 'DEMO-D-13-2'),
    ('FLX-DEMO-0059', 25.5, 'Dama / Caballero', 14, 3, 'DEMO-D-14-1'),
    ('FLX-DEMO-0059', 26.5, 'Dama / Caballero', 21, 3, 'DEMO-D-14-2'),
    ('FLX-DEMO-0060', 25.5, 'Dama / Caballero', 1, 3, 'DEMO-D-15-1'),
    ('FLX-DEMO-0060', 26.5, 'Dama / Caballero', 8, 3, 'DEMO-D-15-2'),
    ('FLX-DEMO-0061', 22.0, 'Dama / Juvenil', 12, 3, 'DEMO-E-01-1'),
    ('FLX-DEMO-0061', 23.5, 'Dama / Juvenil', 19, 3, 'DEMO-E-01-2'),
    ('FLX-DEMO-0062', 27.5, 'Caballero', 23, 3, 'DEMO-E-02-1'),
    ('FLX-DEMO-0062', 29.5, 'Caballero', 6, 3, 'DEMO-E-02-2'),
    ('FLX-DEMO-0063', 18.0, 'Infantil', 10, 3, 'DEMO-E-03-1'),
    ('FLX-DEMO-0063', 20.0, 'Infantil', 17, 3, 'DEMO-E-03-2'),
    ('FLX-DEMO-0064', 18.0, 'Infantil', 21, 3, 'DEMO-E-04-1'),
    ('FLX-DEMO-0064', 20.0, 'Infantil', 4, 3, 'DEMO-E-04-2'),
    ('FLX-DEMO-0065', 18.0, 'Infantil', 8, 3, 'DEMO-E-05-1'),
    ('FLX-DEMO-0065', 20.0, 'Infantil', 15, 3, 'DEMO-E-05-2'),
    ('FLX-DEMO-0066', 22.0, 'Dama / Juvenil', 19, 3, 'DEMO-E-06-1'),
    ('FLX-DEMO-0066', 23.5, 'Dama / Juvenil', 2, 3, 'DEMO-E-06-2'),
    ('FLX-DEMO-0067', 27.5, 'Caballero', 6, 3, 'DEMO-E-07-1'),
    ('FLX-DEMO-0067', 29.5, 'Caballero', 13, 3, 'DEMO-E-07-2'),
    ('FLX-DEMO-0068', 25.5, 'Dama / Caballero', 17, 3, 'DEMO-E-08-1'),
    ('FLX-DEMO-0068', 26.5, 'Dama / Caballero', 0, 3, 'DEMO-E-08-2'),
    ('FLX-DEMO-0069', 25.5, 'Dama / Caballero', 4, 3, 'DEMO-E-09-1'),
    ('FLX-DEMO-0069', 26.5, 'Dama / Caballero', 11, 3, 'DEMO-E-09-2'),
    ('FLX-DEMO-0070', 25.5, 'Dama / Caballero', 15, 3, 'DEMO-E-10-1'),
    ('FLX-DEMO-0070', 26.5, 'Dama / Caballero', 22, 3, 'DEMO-E-10-2'),
    ('FLX-DEMO-0071', 25.5, 'Dama / Caballero', 2, 3, 'DEMO-E-11-1'),
    ('FLX-DEMO-0071', 26.5, 'Dama / Caballero', 9, 3, 'DEMO-E-11-2'),
    ('FLX-DEMO-0072', 25.5, 'Dama / Caballero', 13, 3, 'DEMO-E-12-1'),
    ('FLX-DEMO-0072', 26.5, 'Dama / Caballero', 20, 3, 'DEMO-E-12-2'),
    ('FLX-DEMO-0073', 25.5, 'Dama / Caballero', 0, 3, 'DEMO-E-13-1'),
    ('FLX-DEMO-0073', 26.5, 'Dama / Caballero', 7, 3, 'DEMO-E-13-2'),
    ('FLX-DEMO-0074', 22.0, 'Dama / Juvenil', 11, 3, 'DEMO-E-14-1'),
    ('FLX-DEMO-0074', 23.5, 'Dama / Juvenil', 18, 3, 'DEMO-E-14-2'),
    ('FLX-DEMO-0075', 27.5, 'Caballero', 22, 3, 'DEMO-E-15-1'),
    ('FLX-DEMO-0075', 29.5, 'Caballero', 5, 3, 'DEMO-E-15-2')
) AS demo (codigo, talla, clasificacion, stock, alerta, ubicacion)
INNER JOIN Producto AS p ON p.codigo = demo.codigo
INNER JOIN Talla AS t
    ON t.numero_talla = demo.talla
   AND t.clasificacion_talla = demo.clasificacion;

GO

-- ====================================================
-- MÓDULO 4: VENTAS Y TRANSACCIONES
-- ====================================================

-- 10. Crear tabla Forma_Pago
CREATE TABLE Forma_Pago (
    id_forma_pago INTEGER NOT NULL IDENTITY(1,1),
    descripcion_pago VARCHAR(30) NOT NULL,
    PRIMARY KEY (id_forma_pago)
);

-- 11. Crear tabla Venta
CREATE TABLE Venta (
    id_venta INTEGER NOT NULL IDENTITY(1,1),
    id_usuario INTEGER NOT NULL,
    id_forma_pago INTEGER NOT NULL,
    fecha_venta DATETIME DEFAULT GETDATE(),
    monto_subtotal DECIMAL(10,2) NOT NULL,
    monto_iva DECIMAL(10,2) NOT NULL,
    monto_total DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_venta),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_forma_pago) REFERENCES Forma_Pago(id_forma_pago)
);

-- 12. Crear tabla Detalle_Venta
CREATE TABLE Detalle_Venta (
    id_detalle_venta INTEGER NOT NULL IDENTITY(1,1),
    id_venta INTEGER NOT NULL,
    id_inventario INTEGER NOT NULL,
    cantidad_vendida INTEGER NOT NULL CHECK(cantidad_vendida >= 1),
    precio_unitario_historico DECIMAL(10,2) NOT NULL,
    subtotal_linea AS (cantidad_vendida * precio_unitario_historico),
    PRIMARY KEY (id_detalle_venta),
    FOREIGN KEY (id_venta) REFERENCES Venta(id_venta),
    FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario)
);
GO

-- Insertar Formas de Pago
INSERT INTO Forma_Pago (descripcion_pago) VALUES
('Efectivo'),
('Tarjeta de Debito'),
('Tarjeta de Credito'),
('Transferencia SPEI'),
('Vale Flexi');

-- Ampliacion de Forma_Pago (3 registros adicionales)
INSERT INTO Forma_Pago (descripcion_pago) VALUES
    ('Pago Mixto'),
    ('Tarjeta Digital'),
    ('Monedero Electronico');

-- Insertar Ventas (10 registros)
INSERT INTO Venta (id_usuario, id_forma_pago, fecha_venta, monto_subtotal, monto_iva, monto_total) VALUES
(3, 1, GETDATE(), 1292.24, 206.76, 1499.00),
(3, 2, GETDATE(), 1119.83, 179.17, 1299.00),
(5, 3, GETDATE(), 1637.07, 261.93, 1899.00),
(3, 1, GETDATE(), 775.00, 124.00, 899.00),
(5, 2, GETDATE(), 1464.66, 234.34, 1699.00),
(3, 1, GETDATE(), 861.21, 137.79, 999.00),
(5, 3, GETDATE(), 2240.52, 358.48, 2599.00),
(3, 2, GETDATE(), 1033.62, 165.38, 1199.00),
(5, 1, GETDATE(), 645.69, 103.31, 749.00),
(3, 4, GETDATE(), 1378.45, 220.55, 1599.00);

-- Insertar Detalle de Venta (10 registros)
INSERT INTO Detalle_Venta (id_venta, id_inventario, cantidad_vendida, precio_unitario_historico) VALUES
(1, 3, 1, 1499.00),
(2, 1, 1, 1299.00),
(3, 8, 1, 1899.00),
(4, 9, 1, 899.00),
(5, 7, 1, 1699.00),
(6, 5, 1, 999.00),
(7, 2, 2, 1299.00),
(8, 10, 1, 1199.00),
(9, 1, 1, 749.00),
(10, 4, 1, 1599.00);
GO

-- ====================================================
-- COMPROBACION FINAL DE REGISTROS
-- ====================================================
-- Conteos esperados al ejecutarse por primera vez:
-- Tipo_Usuario 5 | Usuario 5 | Categoria 17 | Marca 13
-- Linea_Estilo 17 | Estatus_Producto 7 | Producto 85
-- Talla 20 | Inventario 160 | Forma_Pago 8
-- Venta 10 | Detalle_Venta 10 | TOTAL 357

SELECT tabla, registros
FROM (
    SELECT  1 AS orden, 'Tipo_Usuario' AS tabla, COUNT_BIG(*) AS registros FROM Tipo_Usuario
    UNION ALL SELECT  2, 'Usuario', COUNT_BIG(*) FROM Usuario
    UNION ALL SELECT  3, 'Categoria', COUNT_BIG(*) FROM Categoria
    UNION ALL SELECT  4, 'Marca', COUNT_BIG(*) FROM Marca
    UNION ALL SELECT  5, 'Linea_Estilo', COUNT_BIG(*) FROM Linea_Estilo
    UNION ALL SELECT  6, 'Estatus_Producto', COUNT_BIG(*) FROM Estatus_Producto
    UNION ALL SELECT  7, 'Producto', COUNT_BIG(*) FROM Producto
    UNION ALL SELECT  8, 'Talla', COUNT_BIG(*) FROM Talla
    UNION ALL SELECT  9, 'Inventario', COUNT_BIG(*) FROM Inventario
    UNION ALL SELECT 10, 'Forma_Pago', COUNT_BIG(*) FROM Forma_Pago
    UNION ALL SELECT 11, 'Venta', COUNT_BIG(*) FROM Venta
    UNION ALL SELECT 12, 'Detalle_Venta', COUNT_BIG(*) FROM Detalle_Venta
) AS resumen
ORDER BY orden;
GO
