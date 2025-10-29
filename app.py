from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length
import os
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

# Backend Java (hardcoded credentials for MVP)
# URL base del backend Java
BACKEND_BASE = os.environ.get('BACKEND_BASE', 'http://localhost:8080')
BACKEND_USER = os.environ.get('BACKEND_USER', 'admin')
BACKEND_PASS = os.environ.get('BACKEND_PASS', '1234')


def backend_url(path: str) -> str:

    return f"{BACKEND_BASE.rstrip('/')}{path}"


def authenticate_backend(username: str, password: str):

    login_url = backend_url('/auth/login')
    try:
        resp = requests.post(
            login_url,
            data={'username': username, 'password': password},
            timeout=6,
        )
    except requests.RequestException as exc:
        return None, f"Error al contactar backend: {exc}"

    if resp.status_code != 200:
        return None, f"Login backend devolvio {resp.status_code}"

    session_id = resp.cookies.get('JSESSIONID')
    try:
        data = resp.json()
        session_id = data.get('sessionId') or session_id
        mensaje = data.get('mensaje')
    except ValueError:
        data = {}
        mensaje = None

    if not session_id:
        return None, 'El backend no devolvio un identificador de sesion'

    return session_id, mensaje or 'Autenticacion correcta'


def backend_request(method: str, path: str, **kwargs):

    cookies = kwargs.pop('cookies', {}) or {}
    session_id = session.get('backend_session_id')
    if session_id:
        cookies['JSESSIONID'] = session_id

    try:
        resp = requests.request(
            method=method.upper(),
            url=backend_url(path),
            cookies=cookies,
            timeout=6,
            **kwargs
        )
        # Si el backend invalida la cookie eliminamos el valor almacenado
        if resp.status_code in (401, 403):
            session.pop('backend_session_id', None)
        return resp
    except requests.RequestException as exc:
        raise RuntimeError(f"Error al contactar backend: {exc}") from exc

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegisterForm(FlaskForm):
    name = StringField('Nombre Completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Rol', choices=[('user', 'Usuario'), ('admin', 'Administrador')], validators=[DataRequired()])
    submit = SubmitField('Registrar Usuario')

# DATOS DE PRUEBA HASTA QUE SE USE LA API REAL
USERS = [
    {
        "id": 1,
        "name": "Admin Principal",
        "email": "admin@legitimoabono.com",
        "password": "admin123",  # En producción usar hash
        "role": "admin"
    }
]

PRODUCTS = [
    {
        "id": 1,
        "name": "Producto 1",
        "price": 29.99,
        "image": "/static/images/product1.jpg",
        "description": "Descripción del producto 1"
    },
    {
        "id": 2,
        "name": "Producto 2", 
        "price": 39.99,
        "image": "/static/images/product2.jpg",
        "description": "Descripción del producto 2"
    }
]

"""
    Esta funcion busca y devuelve (de encontrarlo) 
    un usuario según un email que recibe dentro como
    parámetro.

    Retorna:
        - None si no encontro el email solicitado.
        - El usuario solicitado si el mail existe dentro de la BBDD.
"""
def find_user_by_email(email):
    for user in USERS:
        if user['email'] == email:
            return user
    return None

"""
    Verifica si el rol del usuario es admin o no. Por lo tanto,
    la funcion devolvera un booleano (True o False).
"""
def is_admin():
    return session.get('user_role') == 'admin'

    
def login_required(admin_only=False):
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                flash('Por favor inicia sesión para acceder a esta página', 'error')
                return redirect(url_for('login'))
            if admin_only and not is_admin():
                flash('No tienes permisos para acceder a esta página', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #Se verifica si el usuario esta logueado, de ser asi se dirige al dashboard
    if 'user' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Por favor complete todos los datos', 'error')
            return render_template('login.html', form=form)

        session_id, mensaje = authenticate_backend(username, password)
        if session_id:
            session['backend_session_id'] = session_id
            session['user'] = username
            session['user_name'] = username
            session['user_role'] = 'admin' if username == BACKEND_USER else 'user'
            flash(mensaje or f'Bienvenido {username}!', 'success')
            return redirect(url_for('dashboard'))

        flash('Usuario o contrasena invalidos (backend)', 'error')
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required()
def dashboard():
    return render_template('dashboard.html', 
                         user=session.get('user_name'),
                         role=session.get('user_role'))


@app.route('/users')
@login_required(admin_only=True)
def users():
    """
    Lista los usuarios desde el backend.
    Ahora detecta correctamente los roles provenientes del backend
    (campo 'roles' o 'rol', según formato del JSON).
    """
    try:
        # Llamada al backend Java
        resp = backend_request('GET', '/api/usuario/listar')
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                users_list = []
                for u in data:
                    # --- Detección flexible del rol ---
                    roles = u.get('roles') or []
                    if isinstance(roles, list) and len(roles) > 0:
                        # Si el backend devuelve lista de roles, tomamos el primero
                        rol_nombre = roles[0].get('nombre') or 'ROLE_USER'
                    else:
                        # Si el backend devuelve un campo simple
                        rol_nombre = u.get('rol') or u.get('role') or 'ROLE_USER'

                    # Normalizamos quitando el prefijo ROLE_
                    rol_simple = rol_nombre.replace('ROLE_', '') if isinstance(rol_nombre, str) else 'USER'

                    # --- Construcción del usuario para el frontend ---
                    users_list.append({
                        'id': u.get('idUsuario') or u.get('id') or '',
                        'nombre': u.get('nombre') or u.get('name') or '',
                        'email': u.get('email') or u.get('username') or '',
                        'rol': rol_simple
                    })
                # Render con origen backend
                return render_template('users.html', users=users_list, source='backend')

        # Si la sesión expira, se limpia y se redirige al login
        elif resp.status_code in (401, 403):
            flash('La sesión con el backend expiró. Inicia sesión nuevamente.', 'error')
            session.pop('backend_session_id', None)
            return redirect(url_for('logout'))

    except Exception as exc:
        flash(f"Error al obtener usuarios: {exc}", "error")

    # Si hay error, renderiza la tabla vacía como fallback
    return render_template('users.html', users=[], source='fallback')


@app.route('/users/add', methods=['POST'])
@login_required(admin_only=True)
def add_user():
    """
    Crea un nuevo usuario en el backend Java (POST /api/usuario/add)
    """
    nombre = request.form.get('nombre', '').strip()
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    rol = request.form.get('rol', '').strip()

    if not nombre or not username or not password:
        flash('Todos los campos son obligatorios', 'error')
        return redirect(url_for('users'))

    payload = {'nombre': nombre, 'username': username, 'password': password, 'rol': rol}

    try:
        resp = backend_request('POST', '/api/usuario/add', json=payload)
        if 200 <= resp.status_code < 300:
            flash('Usuario creado correctamente', 'success')
        else:
            flash(f'No se pudo crear el usuario (HTTP {resp.status_code})', 'error')
    except Exception as exc:
        flash(f'Error creando usuario: {exc}', 'error')
    return redirect(url_for('users'))



@app.route('/products')
@login_required()
def products():
    # Try to fetch products from Java backend /api/articulo/listar
    try:
        resp = backend_request('GET', '/api/articulo/listar')
        if resp.status_code == 200:
            try:
                data = resp.json()
            except ValueError:
                data = None
            if isinstance(data, list):
                products_list = []
                for a in data:
                    pid = a.get('idArticulo') or a.get('id') or a.get('id_articulo')
                    name = a.get('nombre') or a.get('name') or f'Articulo {pid}'
                    # Se conserva el flag de disponibilidad para poder editar desde el frontend
                    disponible = a.get('disponible') if 'disponible' in a else a.get('available') if 'available' in a else None
                    price = a.get('price') or a.get('precio') or 0.0
                    description = ('Disponible' if disponible else 'No disponible') if disponible is not None else ''
                    image = a.get('image') or None
                    products_list.append({
                        'id': pid,
                        'name': name,
                        'price': price,
                        'image': image,
                        'description': description,
                        'available': disponible
                    })
                return render_template('products.html', products=products_list, source='backend')
        elif resp.status_code in (401, 403):
            flash('La sesion con el backend expiro. Inicia sesion otra vez.', 'error')
            session.pop('backend_session_id', None)
            return redirect(url_for('logout'))
    except RuntimeError as exc:
        print(f"Backend request error: {exc}")
    except Exception as exc:
        print(f"Failed to fetch products from backend: {exc}")

    # Fallback local: productos de ejemplo (sin disponibilidad editable)
    # Para mantener consistencia en la plantilla, agregamos la clave 'available' como None
    fallback = []
    for p in PRODUCTS:
        q = dict(p)
        q['available'] = None
        fallback.append(q)
    return render_template('products.html', products=fallback, source='fallback')


@app.route('/product/<int:product_id>')
@login_required()
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('products'))
    return render_template('product_detail.html', product=product)


@app.route('/api/products')
@login_required()
def api_products():
    return jsonify(PRODUCTS)


@app.route('/products/add', methods=['POST'])
@login_required(admin_only=True)
def add_product():
    """
    Crea un nuevo articulo en el backend Java utilizando el endpoint
    POST /api/articulo/add. Requiere rol admin.
    """
    nombre = request.form.get('nombre', '').strip()
    disponible = request.form.get('disponible') == 'on'
    if not nombre:
        flash('El nombre es obligatorio', 'error')
        return redirect(url_for('products'))

    payload = {
        'nombre': nombre,
        'disponible': bool(disponible)
    }
    try:
        resp = backend_request('POST', '/api/articulo/add', json=payload)
        if 200 <= resp.status_code < 300:
            flash('Articulo creado correctamente', 'success')
        else:
            flash(f'No se pudo crear el articulo (HTTP {resp.status_code})', 'error')
    except Exception as exc:
        flash(f'Error creando articulo: {exc}', 'error')
    return redirect(url_for('products'))


@app.route('/products/<int:product_id>/update', methods=['POST'])
@login_required(admin_only=True)
def update_product(product_id):
    """
    Actualiza un articulo existente en el backend Java utilizando el endpoint
    PUT /api/articulo/update. Requiere rol admin.
    """
    nombre = request.form.get('nombre', '').strip()
    disponible = request.form.get('disponible') == 'on'
    if not nombre:
        flash('El nombre es obligatorio', 'error')
        return redirect(url_for('products'))

    payload = {
        'idArticulo': product_id,
        'nombre': nombre,
        'disponible': bool(disponible)
    }
    try:
        resp = backend_request('PUT', '/api/articulo/update', json=payload)
        if 200 <= resp.status_code < 300:
            flash('Articulo actualizado correctamente', 'success')
        else:
            flash(f'No se pudo actualizar el articulo (HTTP {resp.status_code})', 'error')
    except Exception as exc:
        flash(f'Error actualizando articulo: {exc}', 'error')
    return redirect(url_for('products'))

@app.route('/logout')
def logout():
    """
    Cierra la sesión tanto en Flask como en el backend Java (si está activa).
    """
    backend_session = session.get('backend_session_id')
    if backend_session:
        try:
            requests.post(
                backend_url('/auth/logout'),
                cookies={'JSESSIONID': backend_session},
                timeout=4
            )
        except requests.RequestException as exc:
            print(f'Backend logout error: {exc}')
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
