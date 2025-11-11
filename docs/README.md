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
- [Miembros del equipo](#Miembros-del-equipo)

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

| Biblioteca | Versión | Descripción |
|-------------|----------|--------------|
| **[Flask](https://flask.palletsprojects.com/en/2.3.x/)** | 2.3.3 | Framework principal para el desarrollo web en Python. |
| **[Flask-WTF](https://flask-wtf.readthedocs.io/en/1.1.x/)** | 1.1.1 | Extensión de Flask que facilita la gestión y validación de formularios. |
| **[WTForms](https://wtforms.readthedocs.io/en/3.0.x/)** | 3.0.1 | Librería para la creación y validación de formularios web. |
| **[Werkzeug](https://werkzeug.palletsprojects.com/en/2.3.x/)** | 2.3.7 | Conjunto de utilidades WSGI para Flask (servidor y manejo de solicitudes HTTP). |
| **[email-validator](https://email-validator.readthedocs.io/en/latest/)** | 1.3.1 | Permite validar direcciones de correo electrónico en formularios. |
| **[python-dotenv](https://saurabh-kumar.com/python-dotenv/)** | 1.0.0 | Carga variables de entorno desde un archivo `.env` para la configuración del proyecto. |


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

- **Productos**: Catálogo completo de los productos disponiobles.
- **Usuarios**: Consulta y gestión de usuarios.
- **Personas**: Consulta y gestión de personas.
- **Roles**: Consulta y gestión de Roles de usuario.
- **Reservas**: Reserva de materiales o salas.
- **Reportes**: Predicción de Reservas.

## Rutas del frontend del sistema

| Ruta | Descripción | Acceso |
|------|--------------|--------|
| `/` | Página principal redirige a `/login` (Login del sistema). | Público |
| `/dashboard` | Panel principal del sistema donde figuraran las diferentes secciones a las cuales se tiene acceso. | Todos los usuarios logueados |
| `/products` | Listado y gestión de productos disponibles. | Todos los usuarios logueados |
| `/user-managemen` | Gestión de usuarios registrados. | Administrador |
| `/register` | Registro de usuarios. | Administrador |
| `/logout` | Cierra la sesión del usuario actual. | Usuarios autenticados |
