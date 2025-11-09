from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import json
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
    # Se verifica si el usuario esta logueado, de ser asi se dirige al dashboard
    if 'user' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Por favor complete todos los datos', 'error')
            return render_template('login.html', form=form)

        # Intento de autenticación contra el backend
        session_id, mensaje = authenticate_backend(username, password)
        if not session_id:
            flash('Usuario o contraseña inválidos', 'error')
            return render_template('login.html', form=form)

        # Guardamos la sesión backend
        session['backend_session_id'] = session_id
        session['user'] = username
        session['user_name'] = username

        # === Nuevo bloque: obtener rol real del backend ===
        try:
            resp = backend_request('GET', '/api/usuario/listar')
            if resp.status_code == 200:
                data = resp.json()
                # Buscar el usuario logueado en la lista
                for u in data:
                    if u.get('username') == username:
                        roles = u.get('roles') or []
                        if isinstance(roles, list) and len(roles) > 0:
                            rol_nombre = roles[0].get('nombre') or 'ROLE_USER'
                        else:
                            rol_nombre = 'ROLE_USER'
                        # Guardamos rol sin prefijo
                        session['user_role'] = rol_nombre.replace('ROLE_', '').lower()
                        break
                else:
                    session['user_role'] = 'user'
            else:
                session['user_role'] = 'user'
        except Exception as exc:
            print(f"Error obteniendo roles del backend: {exc}")
            session['user_role'] = 'user'
        # ==================================================

        flash(mensaje or f'Bienvenido {username}!', 'success')
        return redirect(url_for('dashboard'))

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
    Ahora envía correctamente la estructura JSON con el campo 'roles'
    según el formato esperado por el backend Spring.
    """
    nombre = request.form.get('nombre', '').strip()
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    rol = request.form.get('rol', '').strip().upper()  # puede venir como 'ADMIN' o 'USER'

    if not nombre or not username or not password:
        flash('Todos los campos son obligatorios', 'error')
        return redirect(url_for('users'))

    # Mapear el nombre del rol a su estructura esperada
    if rol == 'ADMIN':
        rol_id = 1
        rol_nombre = 'ROLE_ADMIN'
    else:
        rol_id = 2
        rol_nombre = 'ROLE_USER'

    payload = {
        "username": username,
        "password": password,
        "enabled": True,
        "roles": [
            {"id": rol_id, "nombre": rol_nombre}
        ]
    }

    try:
        resp = backend_request('POST', '/api/usuario/add', json=payload)
        if 200 <= resp.status_code < 300:
            flash(f'Usuario {username} creado correctamente con rol {rol_nombre}', 'success')
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

# ---------------------------
#  Reservas (listar/crear/borrar/actualizar)
# ---------------------------

@app.route('/reservas', methods=['GET'])
@login_required()
def reservas():
    """Vista principal de reservas: lista existentes y muestra formulario de creación."""
    reservas_list = []
    personas = []
    salas = []
    articulos = []
    # 1) Traer reservas
    try:
        r = backend_request('GET', '/api/reservas/listar')
        if 200 <= r.status_code < 300:
            try:
                data = r.json() or []
            except ValueError:
                data = []
            for res in data:
                rid = res.get('id')
                persona = res.get('persona') or {}
                sala = res.get('sala') or {}
                articulo = res.get('articulo') or {}
                reservas_list.append({
                    'id': rid,
                    'persona': persona,
                    'sala': sala if sala else None,
                    'articulo': articulo if articulo else None,
                    'inicio': res.get('fechaHoraInicio'),
                    'fin': res.get('fechaHoraFin')
                })
        elif r.status_code in (401, 403):
            flash('Sesión expirada en backend. Vuelve a iniciar sesión.', 'error')
            return redirect(url_for('logout'))
        else:
            flash(f'No se pudieron obtener reservas (HTTP {r.status_code})', 'error')
    except Exception as exc:
        flash(f'Error consultando reservas: {exc}', 'error')

    # 2) Traer datos para selects (si falla, se deja vacío)
    try:
        pr = backend_request('GET', '/api/persona/listar')
        if 200 <= pr.status_code < 300:
            personas = pr.json() or []
    except Exception:
        personas = []
    try:
        sr = backend_request('GET', '/api/salas/listar')
        if 200 <= sr.status_code < 300:
            salas = sr.json() or []
    except Exception:
        salas = []
    try:
        ar = backend_request('GET', '/api/articulo/listar')
        if 200 <= ar.status_code < 300:
            articulos = ar.json() or []
    except Exception:
        articulos = []

    return render_template('reservas.html', reservas=reservas_list, personas=personas, salas=salas, articulos=articulos)


@app.route('/reservas/crear', methods=['POST'])
@login_required()
def reservas_crear():
    """Crea una reserva en el backend (USER/ADMIN)."""
    persona_id = request.form.get('persona_id')
    sala_id = request.form.get('sala_id') or ''
    articulo_id = request.form.get('articulo_id') or ''
    inicio = request.form.get('inicio')  # YYYY-MM-DDTHH:MM
    fin = request.form.get('fin')

    def norm(dt: str) -> str:
        if not dt:
            return dt
        return dt if len(dt) > 16 else dt + ':00'

    payload = {
        'persona': {'idPersona': int(persona_id)} if persona_id else None,
        'sala': {'idSala': int(sala_id)} if sala_id else None,
        'articulo': {'idArticulo': int(articulo_id)} if articulo_id else None,
        'fechaHoraInicio': norm(inicio),
        'fechaHoraFin': norm(fin)
    }

    if not payload['persona']:
        flash('Debe seleccionar una persona', 'error')
        return redirect(url_for('reservas'))
    if bool(payload['sala']) == bool(payload['articulo']):
        flash('Debe seleccionar una sala O un artículo (solo uno).', 'error')
        return redirect(url_for('reservas'))
    if not payload['fechaHoraInicio'] or not payload['fechaHoraFin']:
        flash('Debe indicar inicio y fin', 'error')
        return redirect(url_for('reservas'))

    try:
        resp = backend_request('POST', '/api/reservas/crear', json=payload)
        if 200 <= resp.status_code < 300:
            flash('Reserva creada correctamente', 'success')
        elif resp.status_code in (401, 403):
            flash('No autorizado. Vuelve a iniciar sesión.', 'error')
            return redirect(url_for('logout'))
        else:
            try:
                j = resp.json()
                msg = j.get('message') or j.get('error') or str(j)
            except ValueError:
                msg = resp.text
            flash(f'No se pudo crear la reserva: {msg}', 'error')
    except Exception as exc:
        flash(f'Error creando reserva: {exc}', 'error')
    return redirect(url_for('reservas'))


@app.route('/reservas/<int:reserva_id>/borrar', methods=['POST'])
@login_required(admin_only=True)
def reservas_borrar(reserva_id: int):
    try:
        resp = backend_request('DELETE', f'/api/reservas/borrar/{reserva_id}')
        if 200 <= resp.status_code < 300:
            flash('Reserva eliminada', 'success')
        else:
            flash(f'No se pudo borrar (HTTP {resp.status_code})', 'error')
    except Exception as exc:
        flash(f'Error borrando reserva: {exc}', 'error')
    return redirect(url_for('reservas'))


@app.route('/reservas/<int:reserva_id>/actualizar', methods=['POST'])
@login_required(admin_only=True)
def reservas_actualizar(reserva_id: int):
    persona_id = request.form.get('persona_id')
    sala_id = request.form.get('sala_id') or ''
    articulo_id = request.form.get('articulo_id') or ''
    inicio = request.form.get('inicio')
    fin = request.form.get('fin')

    def norm(dt: str) -> str:
        if not dt:
            return dt
        return dt if len(dt) > 16 else dt + ':00'

    payload = {
        'id': int(reserva_id),
        'persona': {'idPersona': int(persona_id)} if persona_id else None,
        'sala': {'idSala': int(sala_id)} if sala_id else None,
        'articulo': {'idArticulo': int(articulo_id)} if articulo_id else None,
        'fechaHoraInicio': norm(inicio),
        'fechaHoraFin': norm(fin)
    }

    if bool(payload['sala']) == bool(payload['articulo']):
        flash('Debe seleccionar una sala O un artículo (solo uno).', 'error')
        return redirect(url_for('reservas'))

    try:
        resp = backend_request('PUT', f'/api/reservas/actualizar/{reserva_id}', json=payload)
        if 200 <= resp.status_code < 300:
            flash('Reserva actualizada', 'success')
        else:
            try:
                j = resp.json()
                msg = j.get('message') or j.get('error') or str(j)
            except ValueError:
                msg = resp.text
            flash(f'No se pudo actualizar la reserva: {msg}', 'error')
    except Exception as exc:
        flash(f'Error actualizando reserva: {exc}', 'error')
    return redirect(url_for('reservas'))


# ---------------------------
#  Reportes
# ---------------------------

@app.route('/reportes', methods=['GET'])
@login_required()
def reportes():
    """Dashboard de reportes: contadores, calendario y estadísticas.
    Calcula métricas a partir de /api/reservas/listar.
    """
    reservas = []
    try:
        r = backend_request('GET', '/api/reservas/listar')
        if 200 <= r.status_code < 300:
            try:
                reservas = r.json() or []
            except ValueError:
                reservas = []
        elif r.status_code in (401, 403):
            flash('Sesión con backend expirada. Inicia sesión de nuevo.', 'error')
            return redirect(url_for('logout'))
        else:
            flash(f'No se pudieron obtener reservas (HTTP {r.status_code})', 'error')
    except Exception as exc:
        flash(f'Error consultando reservas: {exc}', 'error')

    # Normalización + métricas
    total = len(reservas)
    por_persona = {}
    por_recurso = {}
    por_fecha = {}
    eventos = []

    def inc(d, key):
        if not key:
            key = 'Desconocido'
        d[key] = d.get(key, 0) + 1

    for res in reservas:
        persona = (res.get('persona') or {}).get('nombre') or (res.get('persona') or {}).get('email') or 'N/D'
        sala = (res.get('sala') or {}).get('nombre')
        articulo = (res.get('articulo') or {}).get('nombre')
        inicio = res.get('fechaHoraInicio')
        fin = res.get('fechaHoraFin')

        inc(por_persona, persona)
        if sala:
            recurso_name = "Sala: " + str(sala)
        elif articulo:
            recurso_name = "Artículo: " + str(articulo)
        else:
            recurso_name = 'Recurso: N/D'
        inc(por_recurso, recurso_name)

        if inicio:
            fecha_key = (inicio.split('T')[0] if 'T' in inicio else inicio.split(' ')[0])
            inc(por_fecha, fecha_key)

        # Evento para calendario
        eventos.append({
            'title': f"{persona} - {recurso_name}",
            'start': inicio,
            'end': fin
        })

    # Top N para gráficos
    def topn(d, n=10):
        items = sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:n]
        labels = [k for k, _ in items]
        values = [v for _, v in items]
        return labels, values

    personas_labels, personas_vals = topn(por_persona, 10)
    recurso_labels, recurso_vals = topn(por_recurso, 10)
    fecha_labels = sorted(por_fecha.keys())
    fecha_vals = [por_fecha[k] for k in fecha_labels]

    # Pasar datos como JSON para Chart.js/FullCalendar
    return render_template(
        'reportes.html',
        total=total,
        personas_labels=json.dumps(personas_labels, ensure_ascii=False),
        personas_vals=json.dumps(personas_vals),
        recurso_labels=json.dumps(recurso_labels, ensure_ascii=False),
        recurso_vals=json.dumps(recurso_vals),
        fecha_labels=json.dumps(fecha_labels),
        fecha_vals=json.dumps(fecha_vals),
        eventos=json.dumps(eventos, ensure_ascii=False)
    )

# ---------------------------
#  Personas (listar/crear/actualizar/eliminar)
# ---------------------------

@app.route('/personas')
@login_required()
def personas():
    """Lista personas desde el backend Java."""
    try:
        resp = backend_request('GET', '/api/persona/listar')
        if resp.status_code == 200:
            data = resp.json() or []
            personas_list = []
            for p in data:
                personas_list.append({
                    'idPersona': p.get('idPersona') or p.get('id') or '',
                    'nombre': p.get('nombre') or '',
                    'email': p.get('email') or ''
                })
            return render_template('personas.html', personas=personas_list)
        elif resp.status_code in (401, 403):
            flash('Sesi\u00f3n con backend expirada. Vuelve a iniciar sesi\u00f3n.', 'error')
            return redirect(url_for('logout'))
        else:
            flash(f'No se pudieron obtener personas (HTTP {resp.status_code})', 'error')
    except Exception as exc:
        flash(f'Error consultando personas: {exc}', 'error')
    return render_template('personas.html', personas=[])


@app.route('/personas/add', methods=['POST'])
@login_required(admin_only=True)
def personas_add():
    nombre = request.form.get('nombre', '').strip()
    email = request.form.get('email', '').strip()
    if not nombre or not email:
        flash('Nombre y email son obligatorios', 'error')
        return redirect(url_for('personas'))
    payload = {'nombre': nombre, 'email': email}
    try:
        resp = backend_request('POST', '/api/persona/add', json=payload)
        if 200 <= resp.status_code < 300:
            flash('Persona creada correctamente', 'success')
        else:
            flash(f'No se pudo crear la persona (HTTP {resp.status_code})', 'error')
    except Exception as exc:
        flash(f'Error creando persona: {exc}', 'error')
    return redirect(url_for('personas'))


@app.route('/personas/<int:id_persona>/update', methods=['POST'])
@login_required(admin_only=True)
def personas_update(id_persona: int):
    nombre = request.form.get('nombre', '').strip()
    email = request.form.get('email', '').strip()
    if not nombre or not email:
        flash('Nombre y email son obligatorios', 'error')
        return redirect(url_for('personas'))
    payload = {'idPersona': id_persona, 'nombre': nombre, 'email': email}
    try:
        resp = backend_request('PUT', '/api/persona/actualizar', json=payload)
        if 200 <= resp.status_code < 300:
            flash('Persona actualizada', 'success')
        else:
            flash(f'No se pudo actualizar (HTTP {resp.status_code})', 'error')
    except Exception as exc:
        flash(f'Error actualizando persona: {exc}', 'error')
    return redirect(url_for('personas'))


@app.route('/personas/<int:id_persona>/delete', methods=['POST'])
@login_required(admin_only=True)
def personas_delete(id_persona: int):
    try:
        resp = backend_request('DELETE', f'/api/persona/eliminar/{id_persona}')
        if 200 <= resp.status_code < 300:
            flash('Persona eliminada', 'success')
        else:
            flash(f'No se pudo eliminar (HTTP {resp.status_code})', 'error')
    except Exception as exc:
        flash(f'Error eliminando persona: {exc}', 'error')
    return redirect(url_for('personas'))


if __name__ == '__main__':
    app.run(debug=True)
