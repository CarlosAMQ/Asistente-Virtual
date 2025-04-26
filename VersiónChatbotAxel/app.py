#Instalar la librería pip install google-generativeai

#pip install mysql-connector-pythonfrom flask import Flask, jsonify, request
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde el frontend

# Configuración de conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',  # Cambia si usas otro usuario
    'password': 'root',  # Cambia si tu contraseña es distinta
    'database': 'asistentevirtual'
}

# Ruta para agendar una cita
@app.route('/agendar-cita', methods=['POST'])
def agendar_cita():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')
    id_paciente = data.get('id_paciente')
    id_medico = data.get('id_medico')
    motivo = data.get('motivo')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verificar que no haya cita duplicada
        query_check = """
        SELECT * FROM citas 
        WHERE fecha = %s AND hora = %s AND id_medico = %s
        """
        cursor.execute(query_check, (date, time, id_medico))
        if cursor.fetchone():
            return jsonify({'error': 'Ya existe una cita para este médico en esa fecha y hora.'}), 409

        # Insertar cita si no hay conflicto
        query_insert = """
        INSERT INTO citas (id_paciente, id_medico, fecha, hora, motivo)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_insert, (id_paciente, id_medico, date, time, motivo))
        conn.commit()
        appointment_id = cursor.lastrowid

        return jsonify({
            'message': 'Cita agendada correctamente',
            'id_cita': appointment_id,
            'date': date,
            'time': time
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# Ruta para editar una cita
# Ruta para editar una cita
@app.route('/editar-cita', methods=['PUT'])
def editar_cita():
    data = request.get_json()
    appointment_id = data.get('appointmentId')
    new_date = data.get('newDate')
    new_time = data.get('newTime')
    new_id_paciente = data.get('newIdPaciente')
    new_motivo = data.get('newMotivo')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Verificar conflicto de horario para otro paciente
        cursor.execute("""
            SELECT COUNT(*) FROM citas 
            WHERE fecha = %s AND hora = %s AND id_cita != %s
        """, (new_date, new_time, appointment_id))
        count = cursor.fetchone()[0]
        if count > 0:
            return jsonify({'error': 'Ese horario ya está ocupado.'}), 409

        query = """
            UPDATE citas 
            SET fecha = %s, hora = %s, id_paciente = %s, motivo = %s 
            WHERE id_cita = %s
        """
        cursor.execute(query, (new_date, new_time, new_id_paciente, new_motivo, appointment_id))
        conn.commit()

        return jsonify({
            'message': 'Cita actualizada correctamente',
            'newDate': new_date,
            'newTime': new_time
        }), 200
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
        query = "DELETE FROM citas WHERE id_cita = %s"
        cursor.execute(query, (appointment_id,))
        conn.commit()

        return jsonify({'message': 'Cita cancelada correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
#Esta función abre el HTML index del http
from flask import render_template  # Agrega esto arriba

@app.route('/')
def index():
    return render_template('index.html')  # Renderiza el HTML del chatbot

import google.generativeai as genai

# Configura la clave API de Gemini
genai.configure(api_key="AIzaSyAzgTPEg_Y4_qb9TIlRQhHjt9N4TG3grAU")
modelo = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/preguntar', methods=['POST'])
def preguntar():
    data = request.get_json()
    mensaje_usuario = data.get('mensaje')
    print(f"Usuario: {mensaje_usuario}")  # ✅ Verifica que llega el mensaje

    # Definir el contexto para Gemini sobre la clínica pediátrica
    prompt_context =  """
Eres un asistente virtual para una clínica pediátrica. Tu tarea es responder preguntas frecuentes relacionadas con la salud de los niños, brindar orientación a padres y ayudarles a agendar, editar o cancelar citas directamente desde este chat.

Puedes realizar las siguientes acciones:
- Agendar una cita médica si el usuario proporciona la fecha, hora y nombre del paciente.
- Editar una cita existente si el usuario proporciona el ID de la cita, nueva fecha y hora, o el motivo.
- Cancelar una cita si el usuario proporciona el ID de la cita.

No es necesario redirigir al usuario a otra página. El usuario puede escribir comandos como:
- "Agendar cita 2025-04-21 10:00 para María López"
- "Editar cita id 6 2025-04-22 12:00"
- "Cancelar cita id 6"

Cuando el usuario no proporciona todos los datos necesarios, debes guiarlo con un ejemplo claro y ordenado.

Tu tono debe ser profesional, amigable y claro. Nunca uses emojis ni asteriscos.
"""


    # Concatenar el contexto con el mensaje del usuario
    mensaje_con_contexto = prompt_context + "\n\nUsuario: " + mensaje_usuario + "\nAsistente:"

    try:
        # Generar respuesta con Gemini
        respuesta = modelo.generate_content(mensaje_con_contexto)
        mensaje_bot = respuesta.text.strip()
        print(f"Gemini respondió: {mensaje_bot}")  # ✅ Verifica respuesta

        # Guardar en la BD
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO mensajeschatbot (id_usuario, mensaje_usuario, respuesta_chatbot)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (1, mensaje_usuario, mensaje_bot))
        conn.commit()

        return jsonify({'respuesta': mensaje_bot})
    except Exception as e:
        return jsonify({'error': f'Error al generar respuesta: {str(e)}'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/probar-conexion')
def probar_conexion():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # ✅ Esto devuelve un diccionario
        cursor.execute("SELECT * FROM citas LIMIT 1;")
        resultado = cursor.fetchone()

        # Convertimos el resultado a string donde sea necesario
        if resultado:
            for key in resultado:
                if isinstance(resultado[key], (bytes, bytearray)):
                    resultado[key] = resultado[key].decode()
                elif isinstance(resultado[key], (int, float, str)):
                    continue
                else:
                    resultado[key] = str(resultado[key])

        return jsonify({
            "conexion": "exitosa",
            "primer_registro": resultado
        }), 200
    except Exception as e:
        return jsonify({"conexion": "fallida", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
@app.route('/guardar-mensaje', methods=['POST'])
def guardar_mensaje():
    data = request.get_json()
    mensaje_usuario = data.get('mensaje_usuario')
    respuesta_chatbot = data.get('respuesta_chatbot')
    id_usuario = 1  # Valor fijo para pruebas, cámbialo si tienes manejo de sesiones

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO mensajeschatbot (id_usuario, mensaje_usuario, respuesta_chatbot)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (id_usuario, mensaje_usuario, respuesta_chatbot))
        conn.commit()

        return jsonify({'message': 'Mensaje guardado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
