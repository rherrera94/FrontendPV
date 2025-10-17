# Programación de Vanguardia - Universidad de la Ciudad de Buenos Aires.
![GitHub repo size](https://img.shields.io/github/repo-size/rherrera94/FrontendPV?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/rherrera94/FrontendPV?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/rherrera94/FrontendPV?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/rherrera94/FrontendPV?style=for-the-badge)
<br>
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Tabla de contenidos
- [Instalación](#Instalación)
   - [Clonar](#Clonar-el-repositorio)
   - [Instalar dependencias](#Instalar-dependencias)
   - [Iniciar localmente](#Iniciar-el-proyecto-de-manera-local)
- [Caracteristicas principales](#Características-principales)
   - [Estructura](#Estructura)
   - [Módulos del sistema](#Módulos-del-sistema)


# Instalación

El proyecto necesita para funcionar [Python](https://www.python.org/downloads/) preferentemente la última versión.

## Clonar el repositorio

   ```bash
    git clone https://github.com/rherrera94/FrontendPV.git
    cd FrontendPV
   ```
## Instalar dependencias

**Nota: Se desarrollaran los comandos primero para crear un ambiente con el fin de que en ese ambiente se instalen las dependencias
y no afecten las instaladas en el sistema que se utilice. De realizar en producción directamente ir a la instalación de los requerimientos
informados en requirements.txt**

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

