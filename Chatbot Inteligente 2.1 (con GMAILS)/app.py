#Instalar la librería pip install google-generativeai

#FUNCIÓN DE NOTIFICACIONES A TRÁVES DE GMAIL

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo_gmail(destinatario, asunto, mensaje_html):
    remitente = 'axelote594@gmail.com'
    password = 'jcqb efjk fxxu efbz'  # La que se generó en gmail
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    msg.attach(MIMEText(mensaje_html, 'html'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, password)
        servidor.send_message(msg)
        servidor.quit()
        print("✅ Correo enviado a", destinatario)
    except Exception as e:
        print("❌ Error al enviar correo:", e)


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
    motivo = data.get('motivo')
    id_medico = data.get('id_medico')

    nombre_completo = data.get('nombre_paciente')  # "Juan Pérez"
    correo = data.get('correo_paciente')    
    if not correo:
        return jsonify({'error': 'El correo del paciente es obligatorio.'}), 400
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Dividir nombre completo
        partes_nombre = nombre_completo.split(" ")
        nombre = partes_nombre[0]
        apellido = " ".join(partes_nombre[1:]) if len(partes_nombre) > 1 else ""

        # Verificar si ya existe un usuario con ese nombre y rol Paciente
        cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre = %s AND rol = 'Paciente'", (nombre,))
        usuario = cursor.fetchone()

        if usuario:
            id_usuario = usuario[0]
        else:
            # Crear nuevo usuario
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, contraseña, rol) 
                VALUES (%s, %s, %s, 'Paciente')
            """, (nombre, correo or 'sincorreo@temporal.com', 'chatbot123'))
            conn.commit()
            id_usuario = cursor.lastrowid

            # Crear paciente asociado
            cursor.execute("""
                INSERT INTO pacientes (id_usuario, apellido, fecha_nacimiento) 
                VALUES (%s, %s, %s)
            """, (id_usuario, apellido, '2015-01-01'))  # fecha por defecto
            conn.commit()

        # Obtener ID del paciente
        cursor.execute("SELECT id_paciente FROM pacientes WHERE id_usuario = %s", (id_usuario,))
        id_paciente = cursor.fetchone()[0]

        # Verificar que no haya conflicto de horario
        cursor.execute("""
            SELECT * FROM citas 
            WHERE fecha = %s AND hora = %s AND id_medico = %s
        """, (date, time, id_medico))
        if cursor.fetchone():
            return jsonify({'error': 'Ya hay una cita para ese médico en esa fecha y hora.'}), 409

        # Crear cita
        cursor.execute("""
            INSERT INTO citas (id_paciente, id_medico, fecha, hora, motivo)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_paciente, id_medico, date, time, motivo))
        conn.commit()
        id_cita = cursor.lastrowid
        # Obtener correo del usuario vinculado al paciente
        cursor.execute("""
            SELECT correo FROM usuarios 
            WHERE id_usuario = %s
        """, (id_usuario,))
        correo_destinatario = cursor.fetchone()[0]

        # Crear y enviar correo de confirmación
        asunto = "Cita médica agendada"
        mensaje_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                color: #333;
            }}
            .container {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                width: 90%;
                max-width: 500px;
                margin: auto;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            h2 {{
                color: #007BFF;
            }}
            p {{
                line-height: 1.6;
            }}
            .info {{
                background-color: #e9f5ff;
                padding: 10px;
                border-left: 4px solid #007BFF;
                margin-bottom: 20px;
            }}
            </style>
        </head>
        <body>
            <div class="container">
            <h2>📅 Confirmación de Cita</h2>
            <p>Hola <strong>{nombre_completo}</strong>,</p>
            <p>Tu cita médica ha sido agendada exitosamente. Aquí están los detalles:</p>
            <div class="info">
                <p><strong>Fecha:</strong> {date}</p>
                <p><strong>Hora:</strong> {time}</p>
                <p><strong>Motivo:</strong> {motivo}</p>
            </div>
            <p>Gracias por confiar en nuestra clínica pediátrica. Si necesitas hacer cambios, responde a este correo o entra al sistema de citas.</p>
            <p style="font-size: 0.9em; color: #555;">Este mensaje fue enviado automáticamente por Medibot, tu asistente virtual pediátrico.</p>
            </div>
        </body>
        </html>
        """
        enviar_correo_gmail(correo_destinatario, asunto, mensaje_html)

        return jsonify({
            'message': 'Cita agendada correctamente',
            'id_cita': id_cita,
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
    new_motivo = data.get('newMotivo')
    nombre_completo = data.get('nombre_paciente')  # Nuevo campo
    correo = data.get('correo_paciente')           # Nuevo campo (opcional)

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Obtener o crear el id_paciente
        partes_nombre = nombre_completo.split(" ")
        nombre = partes_nombre[0]
        apellido = " ".join(partes_nombre[1:]) if len(partes_nombre) > 1 else ""

        cursor.execute("SELECT id_usuario FROM usuarios WHERE nombre = %s AND rol = 'Paciente'", (nombre,))
        usuario = cursor.fetchone()

        if usuario:
            id_usuario = usuario[0]
        else:
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, contraseña, rol) 
                VALUES (%s, %s, %s, 'Paciente')
            """, (nombre, correo or 'sincorreo@temporal.com', 'chatbot123'))
            conn.commit()
            id_usuario = cursor.lastrowid

            cursor.execute("""
                INSERT INTO pacientes (id_usuario, apellido, fecha_nacimiento) 
                VALUES (%s, %s, %s)
            """, (id_usuario, apellido, '2015-01-01'))  # fecha ficticia
            conn.commit()

        cursor.execute("SELECT id_paciente FROM pacientes WHERE id_usuario = %s", (id_usuario,))
        new_id_paciente = cursor.fetchone()[0]
        
        # Actualizar correo si es diferente al actual
        cursor.execute("SELECT correo FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        correo_actual = cursor.fetchone()[0]
        if correo and correo != correo_actual:
            cursor.execute("UPDATE usuarios SET correo = %s WHERE id_usuario = %s", (correo, id_usuario))
            conn.commit()


        # Verificar conflicto de horario
        cursor.execute("""
            SELECT COUNT(*) FROM citas 
            WHERE fecha = %s AND hora = %s AND id_cita != %s
        """, (new_date, new_time, appointment_id))
        count = cursor.fetchone()[0]
        if count > 0:
            return jsonify({'error': 'Ese horario ya está ocupado.'}), 409

        # Actualizar la cita
        cursor.execute("""
            UPDATE citas 
            SET fecha = %s, hora = %s, id_paciente = %s, motivo = %s 
            WHERE id_cita = %s
        """, (new_date, new_time, new_id_paciente, new_motivo, appointment_id))
        conn.commit()
        # Obtener correo del paciente
        cursor.execute("""
            SELECT u.correo FROM usuarios u
            JOIN pacientes p ON u.id_usuario = p.id_usuario
            WHERE p.id_paciente = %s
        """, (new_id_paciente,))
        correo_destinatario = cursor.fetchone()[0]

        # Mensaje y envío
        asunto = "Tu Cita médica ha sido modificada"
        mensaje_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
                color: #333;
            }}
            .container {{
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                width: 90%;
                max-width: 500px;
                margin: auto;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            h2 {{
                color: #ffc107;
            }}
            .info {{
                background-color: #fff9e6;
                padding: 10px;
                border-left: 4px solid #ffc107;
                margin-bottom: 20px;
            }}
            </style>
        </head>
        <body>
            <div class="container">
            <h2>✏️ Modificación de Cita</h2>
            <p>Hola <strong>{nombre_completo}</strong>,</p>
            <p>Tu cita ha sido modificada. Aquí tienes la nueva información:</p>
            <div class="info">
                <p><strong>Fecha:</strong> {new_date}</p>
                <p><strong>Hora:</strong> {new_time}</p>
                <p><strong>Motivo:</strong> {new_motivo}</p>
            </div>
            <p>Gracias por actualizar tu información. Estamos aquí para apoyarte.</p>
            <p style="font-size: 0.9em; color: #555;">Este mensaje fue generado automáticamente por Medibot.</p>
            </div>
        </body>
        </html>
        """
        enviar_correo_gmail(correo_destinatario, asunto, mensaje_html)

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


#Ruta para cancelar/cita para eliminarla y su usuario asociado
@app.route('/cancelar-cita/<int:appointment_id>', methods=['DELETE'])
def cancelar_cita(appointment_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Obtener id_paciente antes de eliminar la cita
        cursor.execute("SELECT id_paciente FROM citas WHERE id_cita = %s", (appointment_id,))
        resultado = cursor.fetchone()
        if not resultado:
            return jsonify({'error': 'Cita no encontrada'}), 404
        id_paciente = resultado[0]

        # Obtener correo del usuario asociado
        cursor.execute("""
            SELECT u.correo, u.nombre
            FROM usuarios u
            JOIN pacientes p ON u.id_usuario = p.id_usuario
            WHERE p.id_paciente = %s
        """, (id_paciente,))
        correo_result = cursor.fetchone()
        if correo_result:
            correo, nombre = correo_result
        else:
            correo = None
            nombre = "Paciente"

        # Eliminar la cita
        cursor.execute("DELETE FROM citas WHERE id_cita = %s", (appointment_id,))
        conn.commit()

        # Revisar si el paciente aún tiene citas
        cursor.execute("SELECT COUNT(*) FROM citas WHERE id_paciente = %s", (id_paciente,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Eliminar paciente y usuario si no tiene más citas
            cursor.execute("SELECT id_usuario FROM pacientes WHERE id_paciente = %s", (id_paciente,))
            id_usuario = cursor.fetchone()[0]

            cursor.execute("DELETE FROM pacientes WHERE id_paciente = %s", (id_paciente,))
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            conn.commit()

        # Enviar correo de cancelación si hay correo
        if correo:
            asunto = "Tu cita fue cancelada"
            mensaje_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f8f9fa;
                    color: #333;
                }}
                .container {{
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    width: 90%;
                    max-width: 500px;
                    margin: auto;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }}
                h2 {{
                    color: #dc3545;
                }}
                .info {{
                    background-color: #fdecea;
                    padding: 10px;
                    border-left: 4px solid #dc3545;
                    margin-bottom: 20px;
                }}
                </style>
            </head>
            <body>
                <div class="container">
                <h2>❌ Cita Cancelada</h2>
                <p>Hola <strong>{nombre}</strong>,</p>
                <p>Tu cita ha sido cancelada exitosamente. Si esto fue un error o deseas reprogramar, por favor contáctanos.</p>
                <div class="info">
                    <p>No se requieren más acciones por tu parte.</p>
                </div>
                <p>Gracias por utilizar Medibot. Esperamos atenderte pronto.</p>
                </div>
            </body>
            </html>
            """

            enviar_correo_gmail(correo, asunto, mensaje_html)

        return jsonify({'message': 'Cita cancelada correctamente'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

#Esta función abre el HTML index del http
from flask import render_template  # Agrega esto arriba

@app.route('/')
def principal():
    return render_template('Principal.html')

# Ruta para mostrar quienes somos
@app.route('/quienes-somos')
def quienes_somos():
    return render_template('Quienes-somos.html')

# Ruta para el chatbot
@app.route('/chatbot')
def chatbot():
    return render_template('index.html')


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
    prompt_context = """
NO USES ASTERISCOS NUNCA, EN NINGUNA OCASIÓN (HACE QUE SE VEA MAL EL TEXTO). TU LENGUAJE DEBE SER PROFESIONAL, CLARO Y CONCISO.

Eres Medibot, un asistente virtual especializado en gestionar citas para una clínica pediátrica, Tu tarea es responder preguntas frecuentes relacionadas con la salud de los niños, brindar orientación a padres y ayudarles a agendar, editar o cancelar citas directamente desde este chat.

Siempre debes solicitar **todos los campos necesarios** desde el inicio. No aceptes información incompleta. No dividas la conversación en múltiples partes.

---

✅ Para **agendar una cita**, solicita:
- Fecha (AAAA-MM-DD)
- Hora (HH:MM)
- Nombre completo del paciente
- Correo electrónico
- Motivo de la consulta

📌 Ejemplo válido:
"Agendar cita 2025-06-01 14:30 para Juan Pérez correo: juan.perez@example.com motivo: chequeo general"

---

✅ Para **editar una cita**, solicita:
- ID de la cita
- Nueva fecha
- Nueva hora
- Nombre completo del paciente
- Correo actualizado
- Motivo actualizado

📌 Ejemplo válido:
"Editar cita id 33 2025-06-01 15:00 para Juan Pérez motivo: seguimiento de fiebre correo: juan@example.com"

---

✅ Para **cancelar una cita**, solicita:
- ID de la cita

📌 Ejemplo válido:
"Cancelar cita id 33"

---

NUNCA digas: "necesito más información". Si el usuario proporciona un mensaje incompleto, muéstrale el formato completo que debe seguir como en los ejemplos anteriores.
Cuando el usuario no proporciona todos los datos necesarios, debes guiarlo con un ejemplo **que incluya siempre el correo del paciente**.
Tu tono debe ser profesional, amigable y claro. Emojis si puedes usar, asteriscos no.
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
