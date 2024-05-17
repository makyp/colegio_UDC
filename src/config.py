from pymongo import MongoClient
import certifi
MONGO='mongodb+srv://makyp:Pacho040321@cluster0.yjkbst6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

#Crear el certificado de seguridad
certificado = certifi.where()

#Funcion que nos permitira conectarno con la base de datos
def Conexion():
    try:
        client = MongoClient(MONGO, tlsCAFile=certificado)
        print('Conexión Exitosa')
        return client["bd_Colegio"]  # Cambia "bd_Colegio" por el nombre de tu base de datos
    except ConnectionError:
        print('Error de conexión con la base de datos')
        return None

Conexion();#Inicializarla