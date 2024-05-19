
class Informacion:
    def __init__(self, quienes_somos, mision, vision, telefono, email):
        self.quienes_somos = quienes_somos
        self.mision = mision
        self.vision = vision
        self.telefono = telefono
        self.email = email
    
    def formato_doc(self):
        return{
            'quienes_somos': self.quienes_somos,
            'mision': self.mision,
            'vision': self.vision,
            'telefono': self.telefono,
            'email': self.email
        }

class Usuario:
    def __init__(self, username, password, role, nombre, materias=None, grado=None):

        self.username = username
        self.password = password
        self.role = role
        self.nombre = nombre
        self.materias = materias
        self.grado = grado
    
    def formato_doc(self):
        username_doc = {
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'nombre': self.nombre,
        }
        if self.materias:
            username_doc['materias'] = self.materias
        if self.grado:
            username_doc['grado'] = self.grado
        return username_doc

class Eventos:
    def __init__(self, fecha, hora, lugar, descripcion):
        self.fecha = fecha
        self.hora = hora
        self.lugar = lugar
        self.descripcion = descripcion
    
    def formato_doc(self):
        return{
            'fecha': self.fecha,
            'hora': self.hora,
            'lugar': self.lugar,
            'descripcion': self.descripcion,

        }
class Estudiante:
    def __init__(self, username, role, nombre = None, documento = None, correo = None, telefono = None, curso= None ):
        self.username = username
        self.role = role
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.curso = curso
    def fomato_doc(self):
        return{
            'username': self.username,
            'role': self.role,
            'nombre': self.nombre,
            'documento': self.documento,
            'correo': self.correo,
            'telefono': self.telefono,
            'curso': self.curso
        }
        

class Docente:
    def __init__(self, username, role, nombre = None, documento = None, correo = None, telefono = None, materias = None):
        self.username = username
        self.role = role
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.materias = materias
    def fomato_doc(self):
        return{
            'username': self.username,
            'role': self.role,
            'nombre': self.nombre,
            'documento': self.documento,
            'correo': self.correo,
            'telefono': self.telefono,
            'materias': self.materias
        }

class Asignatura:
     def __init__(self, nombre, docente, estudiante, calificacion):
         self.nombre = nombre
         self.docente = docente
         self.estudiante = estudiante
         self.calificacion = calificacion
     def fomato_doc(self):
        return{
            'nombre': self.nombre,
            'docente': self.docente,
            'estudiante': self.estudiante,
            'calificacion': self.calificacion
        }    
