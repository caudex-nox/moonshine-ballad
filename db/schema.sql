-- Creación e inicialización de la base de datos
CREATE DATABASE IF NOT EXISTS moonshine_ballad;
USE moonshine_ballad;

-- 1. ROLES
CREATE TABLE IF NOT EXISTS roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE
);

-- 2. CODIGOS POSTALES (codigo_postal como PK)
CREATE TABLE IF NOT EXISTS codigos_postales (
    codigo_postal VARCHAR(15) PRIMARY KEY,
    ciudad VARCHAR(30) NOT NULL,
    provincia VARCHAR(30) NOT NULL
);

-- 3. DOMICILIOS (piso y dpto separados)
CREATE TABLE IF NOT EXISTS domicilios (
    id_domicilio INT AUTO_INCREMENT PRIMARY KEY,
    cod_postal_fk VARCHAR(15) NOT NULL,
    calle VARCHAR(50) NOT NULL,
    numero VARCHAR(10) NOT NULL,
    piso VARCHAR(10),
    dpto VARCHAR(10),
    FOREIGN KEY (cod_postal_fk) REFERENCES codigos_postales(codigo_postal)
);

-- 4. USUARIOS (Clientes y Empleados)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_rol_fk INT NOT NULL,
    id_domicilio_fk INT NOT NULL,
    dni VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(30) NOT NULL,
    apellido VARCHAR(30) NOT NULL,
    email VARCHAR(40) NOT NULL UNIQUE,
    tel_fijo VARCHAR(20),
    tel_movil VARCHAR(20),
    legajo VARCHAR(20) UNIQUE,
    cargo VARCHAR(30),
    FOREIGN KEY (id_rol_fk) REFERENCES roles(id_rol),
    FOREIGN KEY (id_domicilio_fk) REFERENCES domicilios(id_domicilio)
);

-- 5. CATEGORIAS
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(30) NOT NULL UNIQUE,
    descripcion TEXT
);

-- 6. MARCAS
CREATE TABLE IF NOT EXISTS marcas (
    id_marca INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE,
    pais_origen VARCHAR(30) NOT NULL
);

-- 7. PROVEEDORES
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    id_domicilio_fk INT,
    razon_social VARCHAR(30) NOT NULL,
    cuit VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(40) NOT NULL,
    tel_fijo VARCHAR(20),
    tel_movil VARCHAR(20),
    FOREIGN KEY (id_domicilio_fk) REFERENCES domicilios(id_domicilio)
);

-- 8. PRODUCTOS
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    id_categoria_fk INT NOT NULL,
    id_marca_fk INT NOT NULL,
    id_proveedor_fk INT,
    nombre VARCHAR(30) NOT NULL,
    descripcion TEXT,
    imagen_url VARCHAR(500),
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    abv DECIMAL(4, 1) NOT NULL,
    volumen_ml INT NOT NULL,
    FOREIGN KEY (id_categoria_fk) REFERENCES categorias(id_categoria),
    FOREIGN KEY (id_marca_fk) REFERENCES marcas(id_marca),
    FOREIGN KEY (id_proveedor_fk) REFERENCES proveedores(id_proveedor)
);

-- 9. VENTAS (Sin columna total)
CREATE TABLE IF NOT EXISTS ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente_fk INT NOT NULL,
    id_empleado_fk INT,
    id_domicilio_envio_fk INT NOT NULL,
    fecha_venta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metodo_pago VARCHAR(30) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente',
    FOREIGN KEY (id_cliente_fk) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_empleado_fk) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_domicilio_envio_fk) REFERENCES domicilios(id_domicilio)
);

-- 10. DETALLE DE VENTAS
CREATE TABLE IF NOT EXISTS detalle_ventas (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta_fk INT NOT NULL,
    id_producto_fk INT NOT NULL,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_venta_fk) REFERENCES ventas(id_venta) ON DELETE CASCADE,
    FOREIGN KEY (id_producto_fk) REFERENCES productos(id_producto)
);

-- Insertar roles iniciales por defecto
INSERT IGNORE INTO roles (id_rol, nombre) VALUES (1, 'Admin'), (2, 'Cliente');