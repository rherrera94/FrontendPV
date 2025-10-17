# Programación de Vanguardia - Universidad de la Ciudad de Buenos Aires.
![GitHub repo size](https://img.shields.io/github/repo-size/rherrera94/FrontendPV?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/rherrera94/FrontendPV?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/rherrera94/FrontendPV?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/rherrera94/FrontendPV?style=for-the-badge)
<br>


## Tabla de contenidos
<br>

- [Tecnologías utilizadas](#Tecnologías-utilizadas)
- [Instalación](#Instalación)
   - [Clonar](#Clonar-el-repositorio)
   - [Instalar dependencias](#Instalar-dependencias)
   - [Iniciar localmente](#Iniciar-el-proyecto-de-manera-local)
- [Caracteristicas principales](#Características-principales)
   - [Estructura](#Estructura)
   - [Módulos del sistema](#Módulos-del-sistema)
- [Miembros del equipo](#Miembros-del-equipo)

<br>
# Tecnologías utilizadas
<br>

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

# Miembros del equipo

<a href="https://github.com/rherrera94"><img src="https://avatars.githubusercontent.com/u/67210471?s=400&u=6a2ce8477fd073ddcd6c15add1e92aadbca22a03&v=4" width="80" height="80" /></a><br>
<sub><b>Rafael Herrera</b></sub>
<a href="https://github.com/rherrera94"><img src="https://avatars.githubusercontent.com/u/67210471?s=400&u=6a2ce8477fd073ddcd6c15add1e92aadbca22a03&v=4" width="80" height="80" /></a><br>
<sub><b>Rafael Herrera</b></sub>
