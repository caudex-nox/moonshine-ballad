-- =============================================================================
-- TRABAJO PRÁCTICO INTEGRADOR: BASES DE DATOS I
-- PROYECTO: Moonshine Ballad - E-commerce de Whiskies & Licores
-- FICHERO: db/seed.sql
-- DESCRIPCIÓN: Datos de prueba iniciales (DML) para TiDB Cloud
-- =============================================================================

USE `moonshine_ballad`;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE detalle_ventas;
TRUNCATE TABLE ventas;
TRUNCATE TABLE productos;
TRUNCATE TABLE proveedores;
TRUNCATE TABLE marcas;
TRUNCATE TABLE categorias;
TRUNCATE TABLE usuarios;
TRUNCATE TABLE domicilios;
TRUNCATE TABLE codigos_postales;
TRUNCATE TABLE roles;

SET FOREIGN_KEY_CHECKS = 1;

-- 1. Roles
INSERT INTO roles (id_rol, nombre) VALUES 
(1, 'Admin'), 
(2, 'Cliente');

-- 2. Códigos Postales
INSERT INTO codigos_postales (codigo_postal, ciudad, provincia) VALUES 
('S3000', 'Santa Fe', 'Santa Fe'),
('C1001', 'CABA', 'Buenos Aires');

-- 3. Domicilios
INSERT INTO domicilios (id_domicilio, cod_postal_fk, calle, numero, piso, dpto) VALUES 
(1, 'S3000', 'San Martín', '2500', '4', 'B'),
(2, 'S3000', 'Bulevar Gálvez', '1400', NULL, NULL),
(3, 'C1001', 'Av. Corrientes', '800', '12', 'A'),
(4, 'S3000', 'Urquiza', '3100', '1', 'C');

-- 4. Usuarios (Admins y Clientes)
INSERT INTO usuarios (id_usuario, id_rol_fk, id_domicilio_fk, dni, nombre, apellido, email, tel_movil, legajo, cargo) VALUES 
(1, 1, 1, '11111111', 'Franco', 'Admin', 'franco.admin@moonshineballad.com', '3424111222', 'LEG-001', 'Administrador Principal'),
(2, 1, 2, '22222222', 'Carlos', 'Admin', 'carlos.admin@moonshineballad.com', '3424333444', 'LEG-002', 'Administrador de Sistema'),
(3, 2, 3, '33333333', 'Cliente', 'Uno', 'cliente.uno@email.com', '1149998888', NULL, NULL),
(4, 2, 4, '44444444', 'Cliente', 'Dos', 'cliente.dos@email.com', '3424555666', NULL, NULL);

-- 5. Categorías
INSERT INTO categorias (id_categoria, nombre_categoria, descripcion) VALUES 
(1, 'Single Malt', 'Whisky de una sola destilería elaborado 100% con cebada malteada.'),
(2, 'Blended Scotch', 'Mezcla equilibrada de whiskies de grano y malta.'),
(3, 'Bourbon', 'Whisky americano madurado en barricas nuevas de roble blanco quemado.');

-- 6. Marcas
INSERT INTO marcas (id_marca, nombre, pais_origen) VALUES 
(1, 'The Macallan', 'Escocia'),
(2, 'Johnnie Walker', 'Escocia'),
(3, 'Woodford Reserve', 'Estados Unidos');

-- 7. Proveedores
INSERT INTO proveedores (id_proveedor, id_domicilio_fk, razon_social, cuit, email, tel_fijo) VALUES 
(1, 1, 'Distribuidores del Sur S.A.', '30-71122334-8', 'ventas@distsur.com', '01143332211');

-- 8. Productos
INSERT INTO productos (id_producto, id_categoria_fk, id_marca_fk, id_proveedor_fk, nombre, descripcion, precio, stock, abv, volumen_ml) VALUES 
(1, 1, 1, 1, 'Macallan 12 Double Cask', 'Madurado en roble americano y europeo sazonado con jerez.', 125000.00, 12, 40.0, 750),
(2, 2, 2, 1, 'Black Label 12 Year Old', 'Icónico blended scotch con notas a humo, vainilla y fruta dulce.', 45000.00, 30, 40.0, 750),
(3, 3, 3, 1, 'Woodford Reserve Bourbon', 'Bourbon de lote pequeño con matices ricos en especias y fruta.', 88000.00, 8, 43.2, 750);

-- 9. Venta de prueba
INSERT INTO ventas (id_venta, id_cliente_fk, id_empleado_fk, id_domicilio_envio_fk, fecha_venta, metodo_pago, estado) VALUES 
(1, 3, 1, 3, NOW(), 'Tarjeta de Crédito', 'Completada');

-- 10. Detalle de Venta
INSERT INTO detalle_ventas (id_detalle, id_venta_fk, id_producto_fk, cantidad) VALUES 
(1, 1, 1, 1),
(2, 1, 2, 2);

-- Confirmar transacción
COMMIT;