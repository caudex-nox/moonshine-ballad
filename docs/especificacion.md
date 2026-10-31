# Especificación de la Base de Datos — Moonshine Ballad

Diseño relacional, entidades, atributos, tipos de claves y relaciones que componen la base de datos.

---

## 📋 Entidades y Atributos

### 1. Cliente

- **`id_cliente`** (PK, INT, Auto-increment)
- **`dni`** (VARCHAR(20), Unique)
- **`nombre`** (VARCHAR(30))
- **`apellido`** (VARCHAR(30))
- **`email`** (VARCHAR(40), Unique)
- **`tel_fijo`** (VARCHAR(20))
- **`tel_movil`** (VARCHAR(20))
- **`id_domicilio_fk`** (FK, INT) — Referencia a `Domicilio`
- **`id_obra_social_fk`** (FK, INT, Nullable) — Referencia a `Obra_Social`

---

### 2. Producto

- **`id_producto`** (PK, INT, Auto-increment) 
- **`nombre`** (VARCHAR(30))
- **`descripcion`** (TEXT) 
- **`precio`** (DECIMAL(10, 2))
- **`stock`** (INT)
- **`abv`** (DECIMAL(4, 1)) — Graduación alcohólica
- **`volumen_ml`** (INT)
- **`id_categoria_fk`** (FK, INT) — Referencia a `Categoria`
- **`id_proveedor_fk`** (FK, INT) — Referencia a `Proveedor`

---

### 3. Proveedor

- **`id_proveedor`** (PK, INT, Auto-increment) 
- **`razon_social`** (VARCHAR(30)) 
- **`cuit`** (VARCHAR(20), Unique)
- **`email`** (VARCHAR(40))
- **`tel_fijo`** (VARCHAR(20))
- **`tel_movil`** (VARCHAR(20))
- **`id_domicilio_fk`** (FK, INT) — Referencia a `Domicilio`

---

### 4. Empleado

- **`id_empleado`** (PK, INT, Auto-increment)
- **`dni`** (VARCHAR(20), Unique)
- **`nombre`** (VARCHAR(30))
- **`apellido`** (VARCHAR(30))
- **`legajo`** (VARCHAR(20), Unique)
- **`cargo`** (VARCHAR(30))
- **`email`** (VARCHAR(40), Unique)
- **`tel_fijo`** (VARCHAR(20))
- **`tel_movil`** (VARCHAR(20))
- **`id_domicilio_fk`** (FK, INT) — Referencia a `Domicilio`
- **`id_obra_social_fk`** (FK, INT, Nullable) — Referencia a `Obra_Social`

---

### 5. Venta

- **`id_venta`** (PK, INT, Auto-increment)
- **`fecha_venta`** (DATETIME)
- **`total`** (DECIMAL(12, 2))
- **`metodo_pago`** (VARCHAR(30)) — Efectivo, Tarjeta, Transferencia
- **`estado`** (VARCHAR(20)) — Pendiente, Pagado, Enviado, Cancelado
- **`id_cliente_fk`** (FK, INT) — Referencia a `Cliente`
- **`id_empleado_fk`** (FK, INT) — Referencia a `Empleado`

---

### 6. Detalle_Venta

- **`id_detalle`** (PK, INT, Auto-increment)
- **`id_venta_fk`** (FK, INT) — Referencia a `Venta`
- **`id_producto_fk`** (FK, INT) — Referencia a `Producto`
- **`cantidad`** (INT)
- **`precio_unitario`** (DECIMAL(10, 2))
- **`subtotal`** (DECIMAL(10, 2))

---

## 🛠️ Tablas Auxiliares y Entidades de Soporte

### 7. Domicilio

- **`id_domicilio`** (PK, INT, Auto-increment)
- **`calle`** (VARCHAR(50))
- **`numero`** (VARCHAR(10))
- **`ciudad`** (VARCHAR(30))
- **`provincia`** (VARCHAR(30))
- **`codigo_postal`** (VARCHAR(15))

---

### 8. Obra_Social

- **`id_obra_social`** (PK, INT, Auto-increment)
- **`nombre_obra_social`** (VARCHAR(50))
- **`cuit`** (VARCHAR(20), Unique)

---

### 9. Categoria

- **`id_categoria`** (PK, INT, Auto-increment)
- **`nombre_categoria`** (VARCHAR(30)) — Single Malt, Bourbon, Blended, Rye
- **`descripcion`** (TEXT)

---

## 🔗 Resumen de Relaciones y Cardinalidades

1. **Domicilio 1 : N Cliente** — Un domicilio puede estar asociado a varios clientes, pero un cliente pertenece a un único domicilio.
2. **Domicilio 1 : N Empleado** — Un domicilio puede pertenecer a uno o más empleados.
3. **Domicilio 1 : N Proveedor** — Un domicilio asignado por proveedor.
4. **Obra_Social 1 : N Cliente** — Una obra social cubre a cero o varios clientes.
5. **Obra_Social 1 : N Empleado** — Una obra social cubre a uno o varios empleados.
6. **Categoria 1 : N Producto** — Una categoría agrupa múltiples whiskies.
7. **Proveedor 1 : N Producto** — Un proveedor surte varios tipos de whiskies.
8. **Cliente 1 : N Venta** — Un cliente realiza cero, una o muchas compras.
9. **Empleado 1 : N Venta** — Un empleado gestiona cero, una o múltiples ventas.
10. **Venta 1 : N Detalle_Venta** — Una venta contiene de 1 a N renglones de detalle.
11. **Producto 1 : N Detalle_Venta** — Un producto puede figurar en varios detalles de venta.