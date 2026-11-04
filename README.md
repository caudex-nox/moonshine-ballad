<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/mb-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/mb-light.svg">
    <img src="assets/mb-light.svg" width="350" alt="Moonshine Ballad">
  </picture>
</p>

<h6 align="center">Notas destiladas a la luz de la luna</h6>

Plataforma de comercio electrónico orientada a la venta de whiskies finos y destilados artesanales, desarrollada como Trabajo Práctico Integrador para la asignatura **Bases de Datos I**. El proyecto incluye gestión de catálogo, control de pedidos y un sistema de control de acceso basado en roles (**Admin** y **Cliente**), respaldado por una arquitectura REST conectada a una base de datos relacional en la nube.

## Acerca del Proyecto

**Moonshine Ballad** surge con el objetivo de diseñar, implementar y desplegar un sistema completo respaldado por una base de datos relacional MySQL.

### Objetivos Principales

* **Diseño Relacional Robusto:** Modelado conceptual (DER) y lógico (pasaje a tablas) enfocado en la integridad de datos, manejo de inventario y trazabilidad de ventas.
* **API Eficiente y Escalable:** Construcción de servicios RESTful utilizando FastAPI para la gestión de productos, órdenes de compra y control de acceso.
* **Control de Acceso Basado en Roles (RBAC):** Implementación de autenticación segura vía JWT para diferenciar los privilegios entre administradores y clientes.
* **Infraestructura en la Nube:** Despliegue continuo con tecnología serverless (Vercel) integrada a un clúster de MySQL administrado en la nube.

## Arquitectura y Tecnologías

* **Backend:** Python 3.11+ / FastAPI
* **ORM y Base de Datos:** SQLAlchemy + PyMySQL / MySQL (TiDB Cloud)
* **Autenticación y Seguridad:** OAuth2 con JWT (JSON Web Tokens) + Passlib (bcrypt)
* **Frontend:** HTML5, CSS3, JavaScript Vanilla / Jinja2 Templates
* **Despliegue:** Vercel (Serverless Functions)

## Estructura del Proyecto

El repositorio está estructurado de manera modular para separar la lógica de negocio, los esquemas de validación, la persistencia de datos y la interfaz de usuario:

```text
moonshine-ballad/
├── .env.example              # Plantilla de variables de entorno requeridas
├── .gitignore                # Reglas de exclusión de Git
├── README.md                 # Documentación del proyecto
├── requirements.txt          # Dependencias de Python
├── vercel.json               # Configuración de despliegue para Vercel
│
├── api/
│   └── index.py              # Punto de entrada para las funciones Serverless de Vercel
│
├── app/
│   ├── main.py               # Inicialización de la app FastAPI, middlewares y rutas
│   ├── config.py              # Configuración global y lectura de variables de entorno
│   ├── database.py           # Conexión a la base de datos MySQL (Engine y Session)
│   │
│   ├── core/                 # Utilidades de infraestructura y seguridad
│   │   ├── deps.py           # Inyección de dependencias (sesión BD, verificación JWT y roles)
│   │   └── security.py       # Lógica de hashing de contraseñas y firma de tokens
│   │
│   ├── models/               # Modelos relacionales ORM (SQLAlchemy)
│   │   ├── product.py        # Tablas de licores, categorías, marcas y stock
│   │   └── user.py           # Tablas de usuarios, roles y autenticación
│   │
│   ├── schemas/              # Validación y serialización de datos (Pydantic)
│   │   ├── auth.py           # Esquemas para login y respuesta de tokens
│   │   ├── product.py        # Esquemas para creación y consulta de productos
│   │   └── user.py           # Esquemas para registro y gestión de usuarios
│   │
│   ├── routers/              # Controladores de endpoints (API REST)
│   │   ├── admin.py          # Endpoints protegidos (CRUD de catálogo, usuarios y reportes)
│   │   ├── auth.py           # Endpoints públicos (/login, /register)
│   │   └── client.py         # Endpoints de cliente (ver catálogo, carrito, órdenes)
│   │
│   └── static/               # Archivos estáticos de la interfaz web
│       ├── css/              # Hojas de estilo
│       │   └── main.css      # Estilos globales de la interfaz
│       └── js/               # Scripts de interacción y consumos de la API
│           └── main.js       # Lógica e interacciones JavaScript    
│
├── assets/                   # Recursos de diseño (branding del repo, banners y logos)
│   ├── gh-dark.svg
│   ├── mb-dark.svg
│   └── mb-light.svg
│
├── db/                       # Entregables técnicos de la materia
│   ├── schema.sql            # Script DDL de creación de tablas y restricciones
│   ├── seed.sql              # Script DML con datos de prueba e inserts iniciales
│   └── queries.sql           # Consultas SQL complejas (JOINs, GROUP BY, subconsultas)
│
├── docs/                     # Documentación y diagramas del TP
│   ├── diagramas/            # DER, pasaje a tablas y diagramas de flujo (imágenes)
│   │   ├── der.png
│   │   └── tablas_relacional.png
│   │ 
│   └── especificacion.md     # Explicación escrita de entidades, cardinalidad y reglas del TP    
│
└── templates/                # Plantillas HTML de la interfaz
    ├── admin_dashboard.html  # Panel de administración
    ├── base.html             # Layout base
    ├── login.html            # Pantalla de acceso
    └── store.html            # Tienda para usuarios
```

## Roles de Usuario

1. **Administrador (`admin`):**
   * Gestión completa del catálogo de whiskies (crear, editar, eliminar productos).
   * Control de stock y categorías.
   * Visualización del histórico de ventas y usuarios registrados.

2. **Cliente (`usuario`):**
   * Exploración del catálogo de productos disponible.
   * Filtrado de whiskies por categoría, tipo o precio.
   * Registro, inicio de sesión y gestión del perfil personal.

## Configuración y Ejecución Local

### 1. Clonar el repositorio e instalar dependencias

```bash
git clone https://github.com/tu-usuario/moonshine-ballad.git
cd moonshine-ballad

python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Variables de entorno

Copia el archivo `.env.example` a `.env` y completa con las credenciales correspondientes:

```bash
cp .env.example .env
```

Configura en `.env`:

```env
DATABASE_URL=mysql+pymysql://usuario:password@host:port/dbname
SECRET_KEY=tu_clave_secreta_super_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 3. Ejecutar el servidor de desarrollo

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`.