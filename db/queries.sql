-- =============================================================================
-- TRABAJO PRÁCTICO INTEGRADOR: BASES DE DATOS I
-- PROYECTO: Moonshine Ballad - E-commerce de Whiskies & Licores
-- FICHERO: db/queries.sql
-- DESCRIPCIÓN: Consultas SQL nativas para reportes, métricas y operaciones
-- =============================================================================

USE `moonshine_ballad`;

-- -----------------------------------------------------------------------------
-- CONSULTA 1: Listado Detallado de Ventas (JOIN Múltiple)
-- Descripción: Muestra el desglose completo de todas las ventas registradas,
-- asociando cliente, empleado asignado, producto, categoría, marca y cálculo
-- de subtotal por ítem.
-- -----------------------------------------------------------------------------
SELECT 
    v.id_venta,
    v.fecha_venta,
    CONCAT(c.nombre, ' ', c.apellido) AS cliente,
    CONCAT(e.nombre, ' ', e.apellido) AS atendido_por,
    p.nombre AS whisky,
    m.nombre AS marca,
    cat.nombre_categoria AS categoria,
    dv.cantidad,
    p.precio AS precio_unitario,
    (dv.cantidad * p.precio) AS subtotal,
    v.metodo_pago,
    v.estado
FROM ventas v
JOIN usuarios c ON v.id_cliente_fk = c.id_usuario
JOIN usuarios e ON v.id_empleado_fk = e.id_usuario
JOIN detalle_ventas dv ON v.id_venta = dv.id_venta_fk
JOIN productos p ON dv.id_producto_fk = p.id_producto
JOIN marcas m ON p.id_marca_fk = m.id_marca
JOIN categorias cat ON p.id_categoria_fk = cat.id_categoria
ORDER BY v.fecha_venta DESC;


-- -----------------------------------------------------------------------------
-- CONSULTA 2: Acumulado de Facturación por Cliente (GROUP BY + SUM)
-- Descripción: Muestra el gasto total acumulado y la cantidad de compras
-- realizadas por cada cliente registrado en el sistema.
-- -----------------------------------------------------------------------------
SELECT 
    u.id_usuario,
    CONCAT(u.nombre, ' ', u.apellido) AS cliente,
    u.email,
    COUNT(DISTINCT v.id_venta) AS total_compras,
    COALESCE(SUM(dv.cantidad * p.precio), 0) AS total_gastado
FROM usuarios u
LEFT JOIN ventas v ON u.id_usuario = v.id_cliente_fk
LEFT JOIN detalle_ventas dv ON v.id_venta = dv.id_venta_fk
LEFT JOIN productos p ON dv.id_producto_fk = p.id_producto
WHERE u.id_rol_fk = (SELECT id_rol FROM roles WHERE nombre = 'Cliente')
GROUP BY u.id_usuario, u.nombre, u.apellido, u.email
ORDER BY total_gastado DESC;


-- -----------------------------------------------------------------------------
-- CONSULTA 3: Rendimiento y Movimiento de Stock por Producto (LEFT JOIN)
-- Descripción: Calcula las unidades vendidas de cada whisky y las contrasta
-- con el stock actual disponible en depósito.
-- -----------------------------------------------------------------------------
SELECT 
    p.id_producto,
    p.nombre AS whisky,
    m.nombre AS marca,
    c.nombre_categoria AS categoria,
    p.precio,
    p.stock AS stock_actual,
    COALESCE(SUM(dv.cantidad), 0) AS unidades_vendidas
FROM productos p
JOIN marcas m ON p.id_marca_fk = m.id_marca
JOIN categorias c ON p.id_categoria_fk = c.id_categoria
LEFT JOIN detalle_ventas dv ON p.id_producto = dv.id_producto_fk
GROUP BY p.id_producto, p.nombre, m.nombre, c.nombre_categoria, p.precio, p.stock
ORDER BY unidades_vendidas DESC;


-- -----------------------------------------------------------------------------
-- CONSULTA 4: Recaudación por Empleado / Administrador (Auditoría de Ventas)
-- Descripción: Evalúa la cantidad de transacciones atendidas y el volumen de 
-- dinero gestionado por cada miembro del personal.
-- -----------------------------------------------------------------------------
SELECT 
    emp.id_usuario AS id_empleado,
    CONCAT(emp.nombre, ' ', emp.apellido) AS empleado,
    emp.cargo,
    COUNT(DISTINCT v.id_venta) AS ventas_procesadas,
    SUM(dv.cantidad * p.precio) AS total_recaudado
FROM usuarios emp
JOIN ventas v ON emp.id_usuario = v.id_empleado_fk
JOIN detalle_ventas dv ON v.id_venta = dv.id_venta_fk
JOIN productos p ON dv.id_producto_fk = p.id_producto
GROUP BY emp.id_usuario, emp.nombre, emp.apellido, emp.cargo;


-- -----------------------------------------------------------------------------
-- CONSULTA 5: Alerta de Reposición de Stock con Contacto de Proveedor
-- Descripción: Filtra aquellos productos cuyo stock está por debajo del límite
-- crítico (< 10 unidades) e informa el proveedor asignado para compra.
-- -----------------------------------------------------------------------------
SELECT 
    p.nombre AS whisky,
    m.nombre AS marca,
    p.stock,
    pr.razon_social AS proveedor,
    pr.email AS email_proveedor,
    pr.tel_fijo AS telefono_proveedor
FROM productos p
JOIN marcas m ON p.id_marca_fk = m.id_marca
JOIN proveedores pr ON p.id_proveedor_fk = pr.id_proveedor
WHERE p.stock < 10
ORDER BY p.stock ASC;