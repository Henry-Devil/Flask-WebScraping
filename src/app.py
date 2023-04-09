from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
import json

from config import config

# Models:
from models.ModelUser import ModelUser

# Entities:
from models.entities.User import User

app = Flask(__name__)
app.secret_key = 'B!1w8NAt1T^%kvhUI*S^'

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

login_manager_app.login_view = 'login'


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña incorrecta")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtén datos de formulario
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Las contraseñas no coinciden')
            return redirect(request.url)

        # Genera una versión cifrada de la contraseña
        hashed_password = generate_password_hash(password)

        # Crea un objeto User con los datos del formulario y la contraseña cifrada
        new_user = User(id=1, username=username,
                        password=hashed_password, fullname=fullname)

        # Ejecuta la consulta SQL para insertar el nuevo usuario en la base de datos
        sql = "INSERT INTO user (fullname, username, password) VALUES (%s, %s, %s)"
        cursor = db.connection.cursor()
        cursor.execute(
            sql, (new_user.fullname, new_user.username, new_user.password))
        db.connection.commit()
        cursor.close()

        flash('¡Cuenta creada exitosamente!')
        return redirect(url_for('login'))
    else:
        return render_template('auth/register.html')


@app.route('/data')
def view_data():
    conn = db.connection
    cur = conn.cursor()
    cur.execute('SELECT * FROM autos_toyota')
    data = cur.fetchall()
    return render_template('auth/data.html', data=data)


@app.route('/new_data', methods=['GET', 'POST'])
def new_data():
    if request.method == 'POST':
        link_href = request.form.get('link_href')
        precio = request.form.get('precio')
        modelo = request.form.get('modelo')
        kilometraje = request.form.get('kilometraje')
        combustible = request.form.get('combustible')

        print(link_href, precio, modelo, kilometraje, combustible)

        if not all([link_href, precio, modelo, kilometraje, combustible]):
            flash('Por favor llene todos los campos')
            return redirect(url_for('new_data'))

        link_href = link_href.strip()
        precio = precio.strip()
        modelo = modelo.strip()
        kilometraje = kilometraje.strip()
        combustible = combustible.strip()

        if not all(isinstance(field, (str, int, float)) for field in [precio, modelo, kilometraje, combustible]):
            flash('Datos inválidos, por favor revise el formulario')
            return redirect(url_for('new_data'))
        cursor = db.connection.cursor()
        cursor.execute('INSERT INTO autos_toyota (link_href, precio, modelo, kilometraje, combustible) VALUES (%s, %s, %s, %s, %s)',
                       (link_href, precio, modelo, kilometraje, combustible))
        db.connection.commit()
        flash('Auto agregado!')
        return redirect(url_for('data'))

    return render_template('auth/new_data.html')


@app.route('/edit_data/<int:id>', methods=['GET', 'POST'])
def edit_data(id):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM autos_toyota WHERE id = %s', (id,))
    auto = cur.fetchone()
    cur.close()

    if request.method == 'POST':
        link_href = request.form['link_href']
        precio = request.form['precio']
        modelo = request.form['modelo']
        kilometraje = request.form['kilometraje']
        combustible = request.form['combustible']

        cur = db.connection.cursor()
        cur.execute("""
            UPDATE autos_toyota
            SET link_href = %s,
                precio = %s,
                modelo = %s,
                kilometraje = %s,
                combustible = %s
            WHERE id = %s
        """, (link_href, precio, modelo, kilometraje, combustible, id))
        db.connection.commit()
        cur.close()
        flash('Auto actualizado exitosamente')
        return redirect(url_for('edit_data', id=id))

    return render_template('auth/edit_data.html', d=auto)


@app.route('/update_data/<int:id>', methods=['POST'])
def update_data(id):
    # Obtener los datos actualizados del formulario
    link_href = request.form['link_href']
    precio = request.form['precio']
    modelo = request.form['modelo']
    kilometraje = request.form['kilometraje']
    combustible = request.form['combustible']

    # Actualizar los datos del registro en la base de datos
    cur = db.connection.cursor()
    cur.execute("""
        UPDATE autos_toyota
        SET link_href = %s,
            precio = %s,
            modelo = %s,
            kilometraje = %s,
            combustible = %s
        WHERE id = %s
    """, (link_href, precio, modelo, kilometraje, combustible, id))
    db.connection.commit()
    cur.close()

    # Obtener los datos actualizados del registro desde la base de datos
    cur = db.connection.cursor()
    cur.execute("""
        SELECT id, link_href, precio, modelo, kilometraje, combustible
        FROM autos_toyota
        WHERE id = %s
    """, (id,))
    data = cur.fetchone()
    cur.close()

    # Pasar los datos actualizados como contexto a la plantilla 'edit_data.html'
    if data:
        return render_template('auth/edit_data.html', d=data)
    else:
        return "No se encontró el registro solicitado"


@app.route('/delete_data/<id>')
def delete_data(id):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM autos_toyota WHERE id = %s', (id,))
    db.connection.commit()
    flash('Auto eliminado exitosamente')
    return redirect(url_for('data'))

@app.route('/dashboard')
def dashboard():

    # Consulta a la base de datos
    cur = db.connection.cursor()
    cur.execute("SELECT modelo, precio, kilometraje, combustible FROM autos_toyota")

    # Obtener los datos de la base de datos
    data = cur.fetchall()

    # Cerrar la conexión a la base de datos
    cur.close()

    # Transformar los datos en una lista de diccionarios
    results = []
    for row in data:
        result = {}
        result['modelo'] = row[0]
        result['precio'] = row[1]
        result['kilometraje'] = row[2]
        result['combustible'] = row[3]
        results.append(result)

    # Convertir los datos a una cadena JSON
    results_json = json.dumps(results)

    # Pasar los datos a la plantilla como una cadena JSON
    return render_template('auth/dashboard.html', results=results_json)

# Endpoint para obtener los datos como un objeto JSON
@app.route('/api/dashboard')
def dashboard_api():

    # Consulta a la base de datos
    cur = db.connection.cursor()
    cur.execute("SELECT modelo, precio, kilometraje, combustible FROM autos_toyota")

    # Obtener los datos de la base de datos
    data = cur.fetchall()

    # Cerrar la conexión a la base de datos
    cur.close()

    # Transformar los datos en una lista de diccionarios
    results = []
    for row in data:
        result = {}
        result['modelo'] = row[0]
        result['precio'] = row[1]
        result['kilometraje'] = row[2]
        result['combustible'] = row[3]
        results.append(result)

    # Devolver los datos como un objeto JSON
    return jsonify(results)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/data')
@login_required
def data():
    return render_template('auth/data.html')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
