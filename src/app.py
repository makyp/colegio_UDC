import io
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from werkzeug.routing import BuildError
from bson import ObjectId
import gridfs
from informacion import *
from config import *

con_bd = Conexion()
app = Flask(__name__)
app.secret_key = "trwtrtqe3eeeea"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16MB
app.config['UPLOAD_EXTENSIONS'] = ['.pdf', '.jpg', '.jpeg', '.png', '.gif']
# Configuración de Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'

ROLES = {
    "admin": 0,
    "profesor": 1,
    "estudiante": 2
}
fs = gridfs.GridFS(con_bd)
colection_informacion = con_bd['Informacion']
informacion = colection_informacion.find_one()
if informacion:
    texto_quienes_somos = informacion.get('quienes_somos', 'Información no disponible')
    texto_telefono =informacion.get('telefono', 'Información no disponible')
    texto_email = informacion.get('email', 'Informacion no disponible')
    texto_mision = informacion.get('mision', 'Información no disponible')
    texto_vision = informacion.get('vision', 'Información no disponible')
else:
    texto_quienes_somos = 'Información no disponible'
    texto_telefono ='Información no disponible'
    texto_email = 'Informacion no disponible'
    texto_mision = 'Informacion no disponible'
    texto_vision = 'Informacion no disponible'

@app.route('/')
def index():
    return render_template('quienes_somos.html', quienes_somos={'texto': texto_quienes_somos}, telefono={'texto': texto_telefono}, email ={'texto': texto_email})

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    colection_usuarios = con_bd['Usuarios']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if username and password and role:
            objeto_usuario = Usuario(username, password, role)
            colection_usuarios.insert_one(objeto_usuario.formato_doc())
        return redirect(url_for('admin_dashboard'))
    return render_template('inicio_sesion/registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    colection_usuarios = con_bd['Usuarios']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = colection_usuarios.find_one({'username': username, 'password': password})
        if user:
            session['user'] = {key: str(value) if isinstance(value, ObjectId) else value for key, value in user.items()}
            role = user.get('role')
            if role == "admin":
                return redirect(url_for('admin_dashboard'))
            elif role == "profesor":
                return redirect(url_for('profesor_dashboard'))
            elif role == "estudiante":
                return redirect(url_for('estudiante_dashboard'))
        else:
            return render_template('inicio_sesion/login.html', error='Usuario o contraseña incorrectos')
    return render_template('inicio_sesion/login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user' in session and session['user']['role'] == "admin":
        return render_template('admin/admin_dashboard.html')
    else:
        return redirect(url_for('login'))
def cargar_informacion():
    colection_informacion = con_bd['Informacion']
    if colection_informacion.count_documents({}) == 0:
            quienes_somos = "Información por defecto de quiénes somos"
            mision = "Información por defecto de misión"
            vision = "Información por defecto de visión"
            telefono = "3158425715"
            email = "correoUDC@colegioUDC.edu.co"
            object_informacion = Informacion(quienes_somos, mision, vision, telefono, email)
            colection_informacion.insert_one(object_informacion.formato_doc())

@app.route('/editar_informacion', methods=['GET', 'POST'])
def editar_informacion_colegio():
    if 'user' in session and session['user']['role'] == "admin":
        colection_informacion = con_bd['Informacion']
        if request.method == 'POST':
            quienes_somos = request.form.get('quienes_somos')
            mision = request.form.get('mision')
            vision = request.form.get('vision')
            telefono = request.form.get('telefono')
            email = request.form.get('email')
            if quienes_somos and mision and vision and telefono and email:
                colection_informacion.update_one(
                    {}, 
                    {'$set': {'quienes_somos': quienes_somos, 'mision': mision, 'vision': vision, 'telefono': telefono, 'email': email}}
                )
                return redirect(url_for('admin_dashboard'))
            else:
                return "Error, todos los campos son obligatorios"
        
        informacion = colection_informacion.find_one()
        return render_template('admin/editar_informacion.html', informacion=informacion)
    else:
        return redirect(url_for('login'))
    
@app.route('/admin_users', methods=['GET', 'POST'])
def admin_users():
    if 'user' in session and session['user']['role'] == "admin":
        colection_usuarios = con_bd['Usuarios']
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            new_role = request.form.get('new_role')
            if user_id and new_role:
                colection_usuarios.update_one({'_id': ObjectId(user_id)}, {'$set': {'role': new_role}})
                return redirect(url_for('admin_users'))   
        usuarios = colection_usuarios.find()
        return render_template('admin/admin_users.html', usuarios=usuarios)
    else:
        return redirect(url_for('login'))

@app.route('/delete_user/<user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    if 'user' in session and session['user']['role'] == "admin":
        colection_usuarios = con_bd['Usuarios']
        colection_usuarios.delete_one({'_id': ObjectId(user_id)})
        return redirect(url_for('admin_users'))
    else:
        return redirect(url_for('login'))
    
@app.route('/admin_eventos', methods=['GET', 'POST'])
def admin_eventos():
    if 'user' in session and session['user']['role'] == "admin":
        colection_eventos = con_bd['Eventos']
        if request.method == 'POST':
            fecha = request.form['fecha']
            hora = request.form['hora']
            lugar = request.form['lugar']
            descripcion = request.form['descripcion']
            evento = Eventos(fecha, hora, lugar, descripcion)
            colection_eventos.insert_one(evento.formato_doc())
            return redirect(url_for('admin_eventos'))
        eventos = colection_eventos.find()
        return render_template('admin/admin_eventos.html', eventos=eventos)
    else:
        return redirect(url_for('login'))

@app.route('/editar_evento/<evento_id>', methods=['GET', 'POST'])
def editar_evento(evento_id):
    if 'user' in session and session['user']['role'] == "admin":
        colection_eventos = con_bd['Eventos']
        if request.method == 'POST':
            fecha = request.form['fecha']
            hora = request.form['hora']
            lugar = request.form['lugar']
            descripcion = request.form['descripcion']
            colection_eventos.update_one(
                {'_id': ObjectId(evento_id)},
                {'$set': {'fecha': fecha, 'hora': hora, 'lugar': lugar, 'descripcion': descripcion}}
            )
            return redirect(url_for('admin_eventos'))
        evento = colection_eventos.find_one({'_id': ObjectId(evento_id)})
        return render_template('admin/editar_evento.html', evento=evento)
    else:
        return redirect(url_for('login'))

@app.route('/eliminar_evento/<evento_id>', methods=['POST'])
def eliminar_evento(evento_id):
    if 'user' in session and session['user']['role'] == "admin":
        colection_eventos = con_bd['Eventos']
        colection_eventos.delete_one({'_id': ObjectId(evento_id)})
        return redirect(url_for('admin_eventos'))
    else:
        return redirect(url_for('login'))
@app.route('/eventos')
def eventos():
    colection_eventos = con_bd['Eventos']
    eventos_cursor = colection_eventos.find()
    eventos = list(eventos_cursor)
    return render_template('eventos.html', eventos=eventos, quienes_somos={'texto': texto_quienes_somos}, telefono={'texto': texto_telefono}, email ={'texto': texto_email})
# Rutas de subida y previsualización de archivos e imágenes
@app.route('/archivos_institucionales')
def archivos_institucionales():
    if 'user' in session and session['user']['role'] == "admin":
        archivos = list(fs.find())
        return render_template('admin/archivos_institucionales.html', archivos=archivos)
    else:
        return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and any(file.filename.endswith(ext) for ext in app.config['UPLOAD_EXTENSIONS']):
            filename = request.form['filename']
            content_type = file.content_type
            file_id = fs.put(file, filename=filename, content_type=content_type)
            return redirect(url_for('archivos_institucionales'))
        else:
            return "No se pudo cargar el archivo"
    return render_template('admin/upload.html')


@app.route('/archivos')
def listar_archivos():
    archivos = list(con_bd.fs.files.find())  
    return render_template('admin/lista_archivos.html', archivos=archivos)

@app.route('/ver_archivos')
def ver_archivos():
    archivos = list(con_bd.fs.files.find())  
    return render_template('ver_archivos.html', archivos=archivos, telefono={'texto': texto_telefono}, email ={'texto': texto_email})

@app.route('/preview/<file_id>')
def preview_file(file_id):
    try:
        archivo = fs.get(ObjectId(file_id))
        return send_file(
            io.BytesIO(archivo.read()),
            mimetype=archivo.content_type,
            download_name=archivo.filename
        )
    except gridfs.errors.NoFile:
        return "Error al obtener el archivo: no chunk #0"
    except Exception as e:
        return f"Error al obtener el archivo: {str(e)}"

@app.route('/delete/<file_id>', methods=['POST'])
def delete_file(file_id):
    if 'user' in session and session['user']['role'] == "admin":
        try:
            fs.delete(ObjectId(file_id))
            return redirect(url_for('archivos_institucionales'))
        except Exception as e:
            return f"Error al eliminar el archivo: {str(e)}"
    else:
        return redirect(url_for('login'))

@app.route('/mision')
def mision():
    return render_template('mision.html', mision={'texto': texto_mision}, telefono={'texto': texto_telefono}, email ={'texto': texto_email})

@app.route('/vision')
def vision():
    return render_template('vision.html', vision={'texto': texto_vision},telefono={'texto': texto_telefono}, email ={'texto': texto_email} )

@app.route('/profesor_dashboard')
def profesor_dashboard():
    return render_template('profesor/profesor_dashboard.html')

@app.route('/estudiante_dashboard')
def estudiante_dashboard():
    return render_template('estudiante/estudiante_dashboard.html')

@app.errorhandler(BuildError)
def handle_build_error(error):
    return "Error: Could not build URL for endpoint 'dashboard'", 500

if __name__ == '__main__':
    cargar_informacion()
    app.run(debug=True, port=5555)
