
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
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role
    
    def formato_doc(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role,
        }

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