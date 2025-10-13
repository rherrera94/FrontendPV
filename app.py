from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

# Forms
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegisterForm(FlaskForm):
    name = StringField('Nombre Completo', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Rol', choices=[('user', 'Usuario'), ('admin', 'Administrador')], validators=[DataRequired()])
    submit = SubmitField('Registrar Usuario')

# Mock data - en producción usarías una base de datos
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

# Helper functions
def find_user_by_email(email):
    return next((user for user in USERS if user['email'] == email), None)

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

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user_by_email(form.email.data)
        if user and user['password'] == form.password.data:  # En producción usar hash
            session['user'] = user['email']
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            session['user_id'] = user['id']
            flash(f'Bienvenido {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@login_required(admin_only=True)
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Verificar si el usuario ya existe
        if find_user_by_email(form.email.data):
            flash('Este email ya está registrado', 'error')
            return render_template('register.html', form=form)
        
        # Crear nuevo usuario
        new_user = {
            "id": len(USERS) + 1,
            "name": form.name.data,
            "email": form.email.data,
            "password": form.password.data,  # En producción usar hash
            "role": form.role.data
        }
        USERS.append(new_user)
        flash(f'Usuario {form.name.data} registrado exitosamente', 'success')
        return redirect(url_for('user_management'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required()
def dashboard():
    return render_template('dashboard.html', 
                         user=session.get('user_name'),
                         role=session.get('user_role'))

@app.route('/user-management')
@login_required(admin_only=True)
def user_management():
    return render_template('user_management.html', users=USERS)

@app.route('/products')
@login_required()
def products():
    return render_template('products.html', products=PRODUCTS)

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

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)