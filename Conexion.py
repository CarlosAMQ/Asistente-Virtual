#pip install mysql-connector-python
import mysql.connector

class Conexion:
    @staticmethod
    def ConexionBaseDeDatos():
        try:
            conexion = mysql.connector.connect(
                user='root',
                password='root',  # vacío si estás usando XAMPP
                host='127.0.0.1',
                database='asistentevirtual',
                port='3306'
            )
            print("✅ Conexión correcta a la base de datos")
            return conexion
        except mysql.connector.Error as error:
            print("❌ Error al conectarse: {}".format(error))
            return None

# Prueba directa
if __name__ == "__main__":
    Conexion.ConexionBaseDeDatos()
