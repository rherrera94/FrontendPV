# Programación de Vanguardia - Universidad de la Ciudad de Buenos Aires.

<br>
<br>

<h1 align="center" style="font-weight: bold;"> Plataforma de Gestión de Reservas 💻 </h1>

![GitHub repo size](https://img.shields.io/github/repo-size/rherrera94/FrontendPV?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/rherrera94/FrontendPV?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/rherrera94/FrontendPV?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/rherrera94/FrontendPV?style=for-the-badge)

<br>
<br>


## Tabla de contenidos
<br>

- [Tecnologías utilizadas](#Tecnologías-utilizadas)
- [Instalación](#Instalación)
   - [Clonar](#Clonar-el-repositorio)
   - [Instalar dependencias](#Instalar-dependencias)
   - [Iniciar localmente](#Iniciar-el-proyecto-de-manera-local)
- [Caracteristicas principales](#Características-principales)
   - [Dependencias utilizadas](#Dependencias-utilizadas)
   - [Estructura](#Estructura)
   - [Módulos del sistema](#Módulos-del-sistema)
   - [Rutas del frontend del sistema](#Rutas-del-frontend-del-sistema)
      - [Rutas del Frontend](#Rutas-del-Frontend)
      - [Dashboard](#Dashboard)
      - [Gestión de usuarios](#Gestión-de-Usuarios)
      - [Productos](#Productos)
      - [Personas](#Personas)
      - [Reservas](#Reservas)
      - [Salas](#Salas)
      - [Reportes](#Reportes)
      - [Prediccion de reservas](#Predicción-de-Reservas)

<br>

# Tecnologías utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)


<br>

- **Python** – Lógica del frontend y conexión con backend Java.
- **Flask** – Framework web principal.
- **HTML5 / CSS3 / JavaScript** – Estructura y estilo del sitio.
- **Bootstrap** – Diseño responsivo y componentes visuales.


# Instalación

 
El proyecto necesita para funcionar [Python](https://www.python.org/downloads/) preferentemente la última versión.


## Clonar el repositorio

   ```bash
    git clone https://github.com/rherrera94/FrontendPV.git
    cd FrontendPV
   ```
## Instalar dependencias

<br>

> [!NOTE] 
> **Se desarrollaran los comandos primero para crear un ambiente con el fin de que en ese ambiente se instalen las dependencias
> y no afecten las instaladas en el sistema que se utilice. De realizar en producción directamente ir a la instalación de los >requerimientos
>informados en requirements.txt**
<br>

```bash
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

```

## Iniciar el proyecto de manera local

```bash
python app.py
```
# Características principales

## Dependencias utilizadas

## Dependencias utilizadas

| Biblioteca | Versión | Descripción |
|-------------|----------|--------------|
| **[Flask](https://flask.palletsprojects.com/en/2.3.x/)** | 2.3.3 | Framework principal para el desarrollo web en Python. |
| **[Flask-WTF](https://flask-wtf.readthedocs.io/en/1.1.x/)** | 1.1.1 | Extensión de Flask para manejo y validación de formularios. |
| **[WTForms](https://wtforms.readthedocs.io/en/3.0.x/)** | 3.0.1 | Librería para creación y validación de formularios. |
| **[Werkzeug](https://werkzeug.palletsprojects.com/en/2.3.x/)** | 2.3.7 | Utilidades WSGI para Flask. |
| **[email-validator](https://email-validator.readthedocs.io/en/latest/)** | 1.3.1 | Validación de direcciones de correo electrónico. |
| **[python-dotenv](https://saurabh-kumar.com/python-dotenv/)** | 1.0.0 | Manejo de variables de entorno mediante archivos `.env`. |
| **[Requests](https://requests.readthedocs.io/en/latest/)** | 2.31.0 | Consumo de API REST del backend Java. |
| **[NumPy](https://numpy.org/)** | 1.26.4 | Procesamiento numérico utilizado para análisis estadístico. |
| **[Pandas](https://pandas.pydata.org/)** | 2.2.3 | Manipulación y preparación de datos históricos de reservas. |
| **[Statsmodels](https://www.statsmodels.org/stable/index.html)** | 0.14.2 | Implementación del modelo ARIMA para la predicción de reservas. |


## Estructura

```
frontendpv/
├── static/              # Archivos de configuración visual
│     ├── css/
│     └── js/   
├── templates/           # Archivos HTML
└── docs/                # Documentación del sistema
```

## Módulos del sistema

- **Productos**: Catálogo completo de los productos disponibles.
- **Usuarios**: Consulta y gestión de usuarios.
- **Personas**: Consulta y gestión de personas.
- **Roles**: Consulta y gestión de Roles de usuario.
- **Reservas**: Reserva de materiales o salas.
- **Reportes**: Reportes de Reservas.

## Rutas del frontend del sistema

## Rutas del Frontend

| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/` | Redirige a `/login`. | Público |
| `/login` (GET) | Muestra el formulario de inicio de sesión. | Público |
| `/login` (POST) | Valida credenciales contra el backend Java. | Público |
| `/logout` | Cierra la sesión en Flask y en el backend Java. | Usuarios autenticados |

---

## Dashboard
| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/dashboard` | Panel principal del sistema. Muestra el menú con módulos según rol. | USER y ADMIN |

---

## Gestión de Usuarios
| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/users` | Lista usuarios desde `/api/usuario/listar`. | ADMIN |
| `/users/add` (POST) | Agrega un usuario mediante `/api/usuario/add`. | ADMIN |

---

## Productos
| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/products` | Lista artículos desde `/api/articulo/listar`. | USER y ADMIN |
| `/product/<id>` | Vista de un producto local (fallback). | USER y ADMIN |
| `/api/products` | Endpoint interno con productos locales. | USER y ADMIN |
| `/products/add` (POST) | Crea un artículo (`/api/articulo/add`). | ADMIN |
| `/products/<id>/update` (POST) | Actualiza un artículo (`/api/articulo/update`). | ADMIN |

---

## Personas
| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/personas` | Lista personas desde `/api/persona/listar`. | USER y ADMIN |
| `/personas/add` (POST) | Crea persona (`/api/persona/add`). | ADMIN |
| `/personas/<id>/update` (POST) | Actualiza persona (`/api/persona/actualizar`). | ADMIN |
| `/personas/<id>/delete` (POST) | Elimina persona (`/api/persona/eliminar/{id}`). | ADMIN |

---

## Reservas
| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/reservas` | Lista reservas, salas, personas y artículos. | USER y ADMIN |
| `/reservas/crear` (POST) | Crea una reserva (`/api/reservas/crear`). | USER y ADMIN |
| `/reservas/<id>/borrar` (POST) | Elimina una reserva (`/api/reservas/borrar/{id}`). | ADMIN |
| `/reservas/<id>/actualizar` (POST) | Actualiza una reserva (`/api/reservas/actualizar/{id}`). | ADMIN |

---

## Salas
| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/salas` | Lista salas desde `/api/salas/listar`. | USER y ADMIN |
| `/salas/add` (POST) | Crea sala (`/api/salas/crear`). | ADMIN |
| `/salas/<id>/update` (POST) | Actualiza sala (`/api/salas/actualizar`). | ADMIN |
| `/salas/<id>/delete` (POST) | Elimina sala (`/api/salas/borrar/{id}`). | ADMIN |

---

## Reportes
| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/reportes` | Dashboard con estadísticas del sistema. | USER y ADMIN |

---

## Predicción de Reservas
| Ruta | Descripción | Acceso |
|------|-------------|--------|
| `/prediccion` | Genera predicción usando ARIMA a partir de `/api/reservas/listar`. Muestra gráfico + tabla de proyección. | USER y ADMIN |
