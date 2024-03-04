from flask import Flask, render_template, request, redirect
import PyPDF2
import re
from PyPDF2 import PdfReader
from requests import session
import bcrypt
from flask_sqlalchemy import SQLAlchemy
# Rutas de autenticación
from flask import request, make_response

app = Flask(__name__, template_folder='templates')
# Crear modelo User y tabla users en la base de datos para guardar los usuarios registrados:
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        return make_response('Login exitoso')

    return make_response('Usuario o contraseña incorrectos', 401)


# Mostramos en formulario de registro
@app.route('/signup')
def show_signup():
    return render_template('signup.html')


# Recibimos el POST del formulario
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']

    # Validaciones

    hashed_pw = bcrypt.generate_password_hash(password)

    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/login')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No ha selecionado un archivo'

    if file:
        file.save(file.filename)
        pdf_file = open(file.filename, 'rb')
        pdf_reader = PdfReader(pdf_file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        pdf_file.close()

        # Expresiones regulares para extraer la información
        cliente_regex = r'Cliente\s+(\w+\s+\w+\s+\w+)'
        nit_cc_regex = r'Nit\.\s*C\.C\.\s*(\d+)'
        direccion_regex = r'Dirección\s+(\w+\s+\w+\s+\w+\s*\d*\s*\-*\s*\d*)'
        ciudad_regex = r'Ciudad\s+(\w+)'
        consumo_regex = r'Consumo en \(KWh\)(\d+)'
        valor_total_regex = r'VALOR TOTAL A PAGAR\s+\$(\d+)'

        consumo_match = re.search(consumo_regex, text)
        if consumo_match:
            consumo = consumo_match.group(1)
        else:
            consumo = "0"  # O cualquier otro valor por defecto que desees
        cliente = re.search(cliente_regex, text).group(1)
        nit_cc = re.search(nit_cc_regex, text).group(1)
        direccion = re.search(direccion_regex, text).group(1)
        ciudad = re.search(ciudad_regex, text).group(1)
        consumo = re.search(consumo_regex, text).group(1)
        valor_total = re.search(valor_total_regex, text).group(1)

        return render_template('tabla.html', cliente=cliente, nit_cc=nit_cc, direccion=direccion,
                               ciudad=ciudad, consumo=consumo, valor_total=valor_total)


print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True)
