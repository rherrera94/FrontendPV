# Programación de Vanguardia - Universidad de la Ciudad de Buenos Aires.

EN ÉSTA SECCION SE ENCUENTRA EL FRONTEND DEL SISTEMA A DESARROLLAR.


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
# Características Principales

## Estructura

```
frontendpv/
├── static/              # Archivos de configuración visual
├── templates/           # Archivos HTML
└── docs/                # Documentación del sistema
```
## Módulos del Sistema
- **Productos**: Catálogo completo de los productos disponiobles.
- **Usuarios**: Consulta y gestión de usuarios.
- **Personas**: Consulta y gestión de personas.
- **Roles**: Consulta y gestión de Roles de usuario.
- **Reservas**: Reserva de materiales o salas.
- **Reportes**: Predicción de Reservas.