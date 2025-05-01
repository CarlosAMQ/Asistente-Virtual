create database asistentevirtual;
use asistentevirtual;

CREATE TABLE usuarios(
id_usuario INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
correo VARCHAR(150) UNIQUE NOT NULL,
contraseña VARCHAR(255) NOT NULL,
telefono VARCHAR(15) NULL,
rol ENUM('Paciente', 'Médico', 'Recepcionista', 'Administrador') NOT NULL,
fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pacientes(
id_paciente INT AUTO_INCREMENT PRIMARY KEY,
id_usuario INT NOT NULL,
apellido VARCHAR(100) NOT NULL,
fecha_nacimiento DATE NOT NULL,
direccion TEXT NULL,
telefono VARCHAR(15) NULL,

FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE medicos(
id_medico INT AUTO_INCREMENT PRIMARY KEY,
id_usuario INT NOT NULL,
especialidad VARCHAR(100) NOT NULL,
horario_disponible TEXT NOT NULL,
telefono VARCHAR(15) NULL,
correo VARCHAR(150) UNIQUE NOT NULL,

FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE citas(
id_cita INT AUTO_INCREMENT PRIMARY KEY,
id_paciente INT NOT NULL,
id_medico INT NOT NULL,
fecha DATE NOT NULL,
hora TIME NOT NULL,
estado ENUM('Pendiente', 'Confirmada', 'Cancelada', 'Completada') NOT NULL DEFAULT 'Pendiente',
motivo TEXT NULL,

FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE CASCADE,
FOREIGN KEY (id_medico) REFERENCES medicos(id_medico) ON DELETE CASCADE
);

CREATE TABLE preguntasfrecuentes(
id_pregunta INT AUTO_INCREMENT PRIMARY KEY,
pregunta TEXT NOT NULL,
respuesta TEXT NOT NULL,
categoria VARCHAR(50) NULL
);

CREATE TABLE rolespermisos(
id_rol INT AUTO_INCREMENT PRIMARY KEY,
rol VARCHAR(50) UNIQUE NOT NULL,
permisos TEXT NOT NULL
);

CREATE TABLE mensajeschatbot(
id_mensaje INT AUTO_INCREMENT PRIMARY KEY,
id_usuario INT NULL,
mensaje_usuario TEXT NOT NULL,
respuesta_chatbot TEXT NOT NULL,
fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE SET NULL
);

CREATE TABLE notificaciones(
id_notificacion INT AUTO_INCREMENT PRIMARY KEY,
id_usuario INT NOT NULL,
tipo ENUM('Cita', 'Recordatorio', 'Aviso Médico', 'General') NOT NULL,
mensaje TEXT NOT NULL,
estado ENUM('No Leído', 'Leído') NOT NULL DEFAULT 'No Leído',
fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- -------------- -- -------------- -------------- --------------
-- FUNCIONES CRUD -- -------------- -------------- --------------
-- -------------- -- -------------- -------------- --------------

-- -------------- -- --------------
-- Insertar Datos -- --------------
-- -------------- -- --------------

-- Insertar un usuario
INSERT INTO Usuarios (nombre, correo, contraseña, telefono, rol) 
VALUES ('Juan Pérez', 'juan@example.com', 'hashed_password', '5551234567', 'Paciente');

-- Insertar un paciente
INSERT INTO Pacientes (id_usuario, apellido, fecha_nacimiento, direccion, telefono) 
VALUES (1, 'Pérez', '2010-05-15', 'Calle 123, CDMX', '5559876543');

-- Insertar un médico
INSERT INTO Medicos (id_usuario, especialidad, horario_disponible, telefono, correo) 
VALUES (2, 'Pediatría', 'Lunes a Viernes 9:00-17:00', '5556789123', 'medico@example.com');

-- Insertar una cita
INSERT INTO Citas (id_paciente, id_medico, fecha, hora, estado, motivo) 
VALUES (1, 1, '2025-04-10', '10:30:00', 'Pendiente', 'Revisión general');

-- Insertar una pregunta frecuente
INSERT INTO PreguntasFrecuentes (pregunta, respuesta, categoria) 
VALUES ('¿Cuáles son los horarios de atención?', 'De lunes a viernes de 8:00 a 18:00.', 'Horarios');

-- Insertar un rol y permisos
INSERT INTO RolesPermisos (rol, permisos) 
VALUES ('Administrador', 'Gestionar usuarios, citas, médicos, pacientes');

-- Insertar un mensaje en el chatbot
INSERT INTO MensajesChatbot (id_usuario, mensaje_usuario, respuesta_chatbot) 
VALUES (1, '¿Cuáles son los horarios?', 'Atendemos de lunes a viernes de 8:00 a 18:00.');

-- Insertar una notificación
INSERT INTO Notificaciones (id_usuario, tipo, mensaje, estado) 
VALUES (1, 'Cita', 'Tienes una cita el 10 de abril a las 10:30 AM.', 'No Leído');

-- -------------- -- --------------
-- Mostrar datos  -- --------------
-- -------------- -- --------------

-- Obtener todos los usuarios
SELECT * FROM Usuarios;

-- Obtener un usuario por ID
SELECT * FROM Usuarios WHERE id_usuario = 1;

-- Obtener todas las citas de un paciente
SELECT * FROM Citas WHERE id_paciente = 1;

-- Obtener preguntas frecuentes de una categoría específica
SELECT * FROM PreguntasFrecuentes WHERE categoria = 'Horarios';

-- Obtener mensajes del chatbot de un usuario específico
SELECT * FROM MensajesChatbot WHERE id_usuario = 1;

-- -------------- -- --------------
-- Actualizar datos- --------------
-- -------------- -- --------------

-- Actualizar información de un usuario
UPDATE Usuarios SET nombre = 'Juan Pérez López', telefono = '5559999999' WHERE id_usuario = 1;

-- Actualizar el estado de una cita
UPDATE Citas SET estado = 'Confirmada' WHERE id_cita = 1;

-- Actualizar una pregunta frecuente
UPDATE PreguntasFrecuentes SET respuesta = 'Nuestro horario es de lunes a sábado de 8:00 a 18:00.' WHERE id_pregunta = 1;

-- Marcar una notificación como "Leído"
UPDATE Notificaciones SET estado = 'Leído' WHERE id_notificacion = 1;

-- -------------- -- --------------
-- Eliminar datos -- --------------
-- -------------- -- --------------

-- Eliminar un usuario (se eliminarán en cascada los registros relacionados si está configurado así)
DELETE FROM Usuarios WHERE id_usuario = 1;

-- Eliminar una cita
DELETE FROM Citas WHERE id_cita = 1;

-- Eliminar una pregunta frecuente
DELETE FROM PreguntasFrecuentes WHERE id_pregunta = 1;

-- Eliminar un mensaje del chatbot
DELETE FROM MensajesChatbot WHERE id_mensaje = 1;

-- Eliminar una notificación
DELETE FROM Notificaciones WHERE id_notificacion = 1;


