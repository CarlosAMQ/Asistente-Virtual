#Instalar la librería pip install google-generativeai

#pip install mysql-connector-pythonfrom flask import Flask, jsonify, request
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde tu frontend

# Conexión a la base de datos MySQL
db_config = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'database': 'asistentevirtual'
}

# Ruta para agendar una cita
@app.route('/agendar-cita', methods=['POST'])
def agendar_cita():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO citas (fecha, hora) VALUES (%s, %s)"
        cursor.execute(query, (date, time))
        conn.commit()

        return jsonify({'message': 'Cita agendada correctamente', 'date': date, 'time': time}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Ruta para editar una cita
@app.route('/editar-cita', methods=['PUT'])
def editar_cita():
    data = request.get_json()
    appointment_id = data.get('appointmentId')
    new_date = data.get('newDate')
    new_time = data.get('newTime')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "UPDATE citas SET fecha = %s, hora = %s WHERE id = %s"
        cursor.execute(query, (new_date, new_time, appointment_id))
        conn.commit()

        return jsonify({'message': 'Cita actualizada correctamente', 'newDate': new_date, 'newTime': new_time}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Ruta para cancelar una cita
@app.route('/cancelar-cita/<int:appointment_id>', methods=['DELETE'])
def cancelar_cita(appointment_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "DELETE FROM citas WHERE id = %s"
        cursor.execute(query, (appointment_id,))
        conn.commit()

        return jsonify({'message': 'Cita cancelada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
