# Especificación de la Base de Datos — Moonshine Ballad

Diseño relacional, entidades, atributos, tipos de claves y relaciones que componen la base de datos.

---

## 🎨 Diagrama de Entidades y Relaciones (Mermaid.js)

```mermaid
erDiagram
    ROLES ||--o{ USUARIOS : "asigna rol"
    DOMICILIOS ||--o{ USUARIOS : "reside en"
    CODIGOS_POSTALES ||--o{ DOMICILIOS : "pertenece a"
    USUARIOS ||--o{ VENTAS : "compra (Cliente)"
    USUARIOS ||--o{ VENTAS : "gestiona (Empleado)"
    DOMICILIOS ||--o{ VENTAS : "destino envio"
    DOMICILIOS ||--o{ PROVEEDORES : "ubicacion fiscal"
    
    CATEGORIAS ||--o{ PRODUCTOS : "agrupa"
    MARCAS ||--o{ PRODUCTOS : "marca"
    PROVEEDORES ||--o{ PRODUCTOS : "surtido por"
    
    VENTAS ||--|{ DETALLE_VENTAS : "contiene"
    PRODUCTOS ||--o{ DETALLE_VENTAS : "figura en"

    ROLES {
        int id_rol PK
        string nombre UK
    }

    CODIGOS_POSTALES {
        int id_cod_postal PK
        string codigo_postal UK
        string ciudad
        string provincia
    }

    DOMICILIOS {
        int id_domicilio PK
        int id_cod_postal_fk FK
        string calle
        string numero
        string piso_dpto
    }

    USUARIOS {
        int id_usuario PK
        int id_rol_fk FK
        int id_domicilio_fk FK
        string dni UK
        string nombre
        string apellido
        string email UK
        string tel_fijo
        string tel_movil
        string legajo UK
        string cargo
    }

    CATEGORIAS {
        int id_categoria PK
        string nombre_categoria UK
        string descripcion
    }

    MARCAS {
        int id_marca PK
        string nombre UK
        string pais_origen
    }

    PROVEEDORES {
        int id_proveedor PK
        string razon_social
        string cuit UK
        string email
        string tel_fijo
        string tel_movil
        int id_domicilio_fk FK
    }

    PRODUCTOS {
        int id_producto PK
        int id_categoria_fk FK
        int id_marca_fk FK
        int id_proveedor_fk FK
        string nombre
        string descripcion
        decimal precio
        int stock
        decimal abv
        int volumen_ml
    }

    VENTAS {
        int id_venta PK
        int id_cliente_fk FK
        int id_empleado_fk FK
        int id_domicilio_envio_fk FK
        datetime fecha_venta
        decimal total
        string metodo_pago
        string estado
    }

    DETALLE_VENTAS {
        int id_detalle PK
        int id_venta_fk FK
        int id_producto_fk FK
        int cantidad
    }
```

---

## 📑 Especificación de Tablas y Atributos

### 1. Rol (`roles`)

- **`id_rol`** (PK, INT, Auto-increment)
- **`nombre`** (VARCHAR(30), Unique) — (`Admin`, `Cliente`).

---

### 2. Codigo_Postal (`codigos_postales`)

- **`id_cod_postal`** (PK, INT, Auto-increment)
- **`codigo_postal`** (VARCHAR(15), Unique)
- **`ciudad`** (VARCHAR(30))
- **`provincia`** (VARCHAR(30))

---

### 3. Domicilio (`domicilios`)

- **`id_domicilio`** (PK, INT, Auto-increment)
- **`id_cod_postal_fk`** (FK, INT) — Referencia a `codigos_postales`.
- **`calle`** (VARCHAR(50))
- **`numero`** (VARCHAR(10))
- **`piso_dpto`** (VARCHAR(10), Nullable)

---

### 4. Usuario (`usuarios`)

- **`id_usuario`** (PK, INT, Auto-increment)
- **`id_rol_fk`** (FK, INT) — Referencia a `roles`.
- **`id_domicilio_fk`** (FK, INT) — Referencia a `domicilios`.
- **`dni`** (VARCHAR(20), Unique)
- **`nombre`** (VARCHAR(30))
- **`apellido`** (VARCHAR(30))
- **`email`** (VARCHAR(40), Unique)
- **`tel_fijo`** (VARCHAR(20), Nullable)
- **`tel_movil`** (VARCHAR(20), Nullable)
- **`legajo`** (VARCHAR(20), Unique, Nullable)
- **`cargo`** (VARCHAR(30), Nullable)

---

### 5. Categoria (`categorias`)

- **`id_categoria`** (PK, INT, Auto-increment)
- **`nombre_categoria`** (VARCHAR(30), Unique) — (*Single Malt*, *Bourbon*, *Rye*, *Blended*).
- **`descripcion`** (TEXT, Nullable)

---

### 6. Marca (`marcas`)

- **`id_marca`** (PK, INT, Auto-increment)
- **`nombre`** (VARCHAR(30), Unique)
- **`pais_origen`** (VARCHAR(30))

---

### 7. Proveedor (`proveedores`)

- **`id_proveedor`** (PK, INT, Auto-increment)
- **`razon_social`** (VARCHAR(30))
- **`cuit`** (VARCHAR(20), Unique)
- **`email`** (VARCHAR(40))
- **`tel_fijo`** (VARCHAR(20))
- **`tel_movil`** (VARCHAR(20))
- **`id_domicilio_fk`** (FK, INT, Nullable) — Referencia a `domicilios`.

---

### 8. Producto (`productos`)

- **`id_producto`** (PK, INT, Auto-increment)
- **`id_categoria_fk`** (FK, INT) — Referencia a `categorias`.
- **`id_marca_fk`** (FK, INT) — Referencia a `marcas`.
- **`id_proveedor_fk`** (FK, INT, Nullable) — Referencia a `proveedores`.
- **`nombre`** (VARCHAR(30))
- **`descripcion`** (TEXT)
- **`precio`** (DECIMAL(10, 2))
- **`stock`** (INT)
- **`abv`** (DECIMAL(4, 1)) — Graduación alcohólica (% ABV).
- **`volumen_ml`** (INT)

---

### 9. Venta (`ventas`)

- **`id_venta`** (PK, INT, Auto-increment)
- **`id_cliente_fk`** (FK, INT) — Referencia a `usuarios`.
- **`id_empleado_fk`** (FK, INT, Nullable) — Referencia a `usuarios`.
- **`id_domicilio_envio_fk`** (FK, INT) — Referencia a `domicilios`.
- **`fecha_venta`** (DATETIME)
- **`total`** (DECIMAL(12, 2))
- **`metodo_pago`** (VARCHAR(30)) — (*Efectivo*, *Tarjeta*, *Transferencia*).
- **`estado`** (VARCHAR(20)) — (*Pendiente*, *Pagado*, *Enviado*, *Cancelado*).

---

### 10. Detalle_Venta (`detalle_ventas`)

- **`id_detalle`** (PK, INT, Auto-increment)
- **`id_venta_fk`** (FK, INT) — Referencia a `ventas`.
- **`id_producto_fk`** (FK, INT) — Referencia a `productos`.
- **`cantidad`** (INT)

---

## 🔗 Resumen de Relaciones y Cardinalidades

1. **`roles` 1 : N `usuarios`** — Un rol (Admin/Cliente) asigna permisos a múltiples usuarios.
2. **`codigos_postales` 1 : N `domicilios`** — Un código postal agrupa múltiples domicilios.
3. **`domicilios` 1 : N `usuarios`** — Un domicilio asignado a cada usuario.
4. **`domicilios` 1 : N `proveedores`** — Un domicilio fiscal asociado a un proveedor.
5. **`categorias` 1 : N `productos`** — Una categoría agrupa múltiples whiskies.
6. **`marcas` 1 : N `productos`** — Una marca embotella múltiples whiskies.
7. **`proveedores` 1 : N `productos`** — Un proveedor surte variados licores.
8. **`usuarios` (Cliente) 1 : N `ventas`** — Un cliente realiza cero, una o muchas compras.
9. **`usuarios` (Empleado) 1 : N `ventas`** — Un empleado gestiona cero, una o muchas ventas.
10. **`domicilios` 1 : N `ventas`** — Un domicilio sirve como destino de envío de 0 a N ventas.
11. **`ventas` 1 : N `detalle_ventas`** — Una venta contiene de 1 a N renglones de detalle.
12. **`productos` 1 : N `detalle_ventas`** — Un producto se incluye en múltiples detalles de venta.