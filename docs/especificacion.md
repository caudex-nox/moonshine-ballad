# Especificación de la Base de Datos

Diseño relacional, entidades, atributos, tipos de claves y relaciones que componen la base de datos.

---

## 📋 Entidades y Atributos

### 1. Clientes
Almacena la información personal y de contacto de los compradores.

* **`id_cliente`** (PK, INT, Auto-increment) — Identificador único del cliente.
* **`nombre`** (VARCHAR(100)) — Nombre(s) del cliente.
* **`apellido`** (VARCHAR(100)) — Apellido(s) del cliente.
* **`dni_cuit`** (VARCHAR(20), Unique) — Documento o CUIT para facturación.
* **`email`** (VARCHAR(150), Unique) — Correo electrónico (utilizado para inicio de sesión).
* **`telefono`** (VARCHAR(20)) — Teléfono de contacto.
* **`id_domicilio`** (FK, INT) — Referencia a la tabla `Domicilios`.
* **`id_obra_social`** (FK, INT, Nullable) — Referencia opcional a `Obras_Sociales`.
* **`fecha_registro`** (DATETIME) — Fecha de creación de la cuenta.

---

### 2. Productos (Whiskies y Destilados)
Contiene la información técnica, comercial e inventario de los productos a la venta.

* **`id_producto`** (PK, INT, Auto-increment) — Identificador único del producto.
* **`nombre`** (VARCHAR(150)) — Nombre comercial del whisky.
* **`descripcion`** (TEXT) — Descripción, notas de cata y origen.
* **`precio`** (DECIMAL(10, 2)) — Precio unitario de venta.
* **`stock`** (INT) — Cantidad disponible en inventario.
* **`graduacion_alcoholica`** (DECIMAL(4, 1)) — Porcentaje de alcohol (ej: 43.0).
* **`volumen_ml`** (INT) — Volumen en mililitros (ej: 750).
* **`id_categoria`** (FK, INT) — Referencia a la tabla `Categorias`.
* **`id_proveedor`** (FK, INT) — Referencia a la tabla `Proveedores`.

---

### 3. Proveedores
Registra las empresas o distribuidores que abastecen la tienda.

* **`id_proveedor`** (PK, INT, Auto-increment) — Identificador único del proveedor.
* **`razon_social`** (VARCHAR(150)) — Nombre o razón social de la empresa.
* **`cuit`** (VARCHAR(20), Unique) — CUIT comercial del proveedor.
* **`email`** (VARCHAR(150)) — Correo electrónico comercial.
* **`telefono`** (VARCHAR(20)) — Teléfono de contacto.
* **`id_domicilio`** (FK, INT) — Referencia a la tabla `Domicilios`.

---

### 4. Empleados
Información del personal involucrado en la gestión de la tienda y procesamiento de ventas.

* **`id_empleado`** (PK, INT, Auto-increment) — Identificador único del empleado.
* **`nombre`** (VARCHAR(100)) — Nombre del empleado.
* **`apellido`** (VARCHAR(100)) — Apellido del empleado.
* **`legajo`** (VARCHAR(20), Unique) — Número de legajo interno.
* **`cargo`** (VARCHAR(50)) — Rol ocupacional (ej: Vendedor, Encargado, Administrador).
* **`email`** (VARCHAR(150), Unique) — Correo institucional.
* **`telefono`** (VARCHAR(20)) — Teléfono de contacto.
* **`id_domicilio`** (FK, INT) — Referencia a la tabla `Domicilios`.
* **`id_obra_social`** (FK, INT, Nullable) — Referencia a la tabla `Obras_Sociales`.
* **`fecha_ingreso`** (DATE) — Fecha de contratación.

---

### 5. Ventas (Cabecera de Factura / Pedido)
Registra cada transacción realizada en la plataforma.

* **`id_venta`** (PK, INT, Auto-increment) — Identificador único de la transacción.
* **`fecha_venta`** (DATETIME) — Fecha y hora de emisión.
* **`total`** (DECIMAL(12, 2)) — Monto total acumulado de la venta.
* **`metodo_pago`** (VARCHAR(50)) — Método utilizado (Efectivo, Tarjeta, Transferencia).
* **`estado`** (VARCHAR(30)) — Estado del pedido (Pendiente, Pagado, Enviado, Cancelado).
* **`id_cliente`** (FK, INT) — Cliente que realiza la compra.
* **`id_empleado`** (FK, INT) — Empleado que procesa o valida la transacción.

---

### 6. Detalle_Ventas (Tabla Intermedia)
Desglosa los items o productos asociados a cada cabecera de venta.

* **`id_detalle`** (PK, INT, Auto-increment) — Identificador del renglón de detalle.
* **`id_venta`** (FK, INT) — Venta a la que pertenece el detalle.
* **`id_producto`** (FK, INT) — Producto comprado.
* **`cantidad`** (INT) — Unidades adquiridas.
* **`precio_unitario`** (DECIMAL(10, 2)) — Precio histórico del producto al momento de la venta.
* **`subtotal`** (DECIMAL(10, 2)) — Cálculo (`cantidad` * `precio_unitario`).

---

## Tablas Auxiliares y Entidades de Soporte

### 7. Domicilios
Desacopla la ubicación física para su reutilización en Clientes, Empleados y Proveedores.

* **`id_domicilio`** (PK, INT, Auto-increment) — Identificador de dirección.
* **`calle`** (VARCHAR(100)) — Nombre de la calle.
* **`numero`** (VARCHAR(10)) — Numeración de la finca.
* **`piso_depto`** (VARCHAR(10), Nullable) — Datos de departamento o piso.
* **`barrio`** (VARCHAR(100)) — Barrio / Localidad.
* **`ciudad`** (VARCHAR(100)) — Ciudad principal.
* **`provincia`** (VARCHAR(100)) — Provincia / Estado.
* **`codigo_postal`** (VARCHAR(15)) — Código postal.

---

### 8. Obras_Sociales
Almacena las entidades prestadoras de servicios de salud para el personal.

* **`id_obra_social`** (PK, INT, Auto-increment) — Identificador de la obra social.
* **`nombre_obra_social`** (VARCHAR(150)) — Nombre o razón social de la entidad.
* **`cuit`** (VARCHAR(20), Unique) — CUIT de la institución médica.
* **`cobertura_plan`** (VARCHAR(100)) — Tipo o código de plan contratado.

---

### 9. Categorias
Clasifica los productos según el tipo de destilado o procedencia.

* **`id_categoria`** (PK, INT, Auto-increment) — Identificador de categoría.
* **`nombre_categoria`** (VARCHAR(100)) — Ej: *Single Malt, Bourbon, Blended, Rye*.
* **`descripcion`** (TEXT) — Breve reseña del estilo de whisky.

---

## 🔗 Resumen de Relaciones y Cardinalidades

1. **Domicilios 1 : N Clientes** — Un domicilio puede estar asociado a varios clientes (ej: grupo familiar), pero un cliente pertenece a un único domicilio registrado.
2. **Domicilios 1 : N Empleados** — Un domicilio puede pertenecer a uno o más empleados.
3. **Domicilios 1 : N Proveedores** — Un domicilio asignado por proveedor.
4. **Obras_Sociales 1 : N Empleados** — Una obra social cubre a uno o varios empleados.
5. **Categorias 1 : N Productos** — Una categoría agrupa múltiples whiskies.
6. **Proveedores 1 : N Productos** — Un proveedor surte varios tipos de whiskies.
7. **Clientes 1 : N Ventas** — Un cliente realiza cero, una o muchas compras.
8. **Empleados 1 : N Ventas** — Un empleado gestiona cero, una o múltiples ventas.
9. **Ventas 1 : N Detalle_Ventas** — Una venta contiene de 1 a N renglones de detalle.
10. **Productos 1 : N Detalle_Ventas** — Un producto puede figurar en varios detalles de venta.