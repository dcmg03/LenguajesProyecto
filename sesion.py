#Inicializar la BD y crear la tabla users
from flask import request, redirect, url_for
from sqlalchemy.sql.functions import user

from flask_login import login_user, logout_user, login_required
from main import db, app

db.create_all()




@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Buscar usuario y verificar password

    if user:
        login_user(user)
        return redirect(url_for('index'))

    return 'Usuario o contraseña incorrectos', 401


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#proteger rutas con  @login_required
@app.route('/profile')
@login_required
def profile():
   return 'Perfil de usuario'