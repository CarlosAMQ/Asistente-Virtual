function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim(); // Eliminamos espacios en blanco

    if (message === "") return; // No enviar mensajes vacíos

    addMessage(message, 'user'); // Agregar mensaje del usuario
    userInput.value = ""; // Limpiar el campo de entrada

    // Simular respuesta del chatbot después de un pequeño retraso
    setTimeout(() => {
        const botResponse = getBotResponse(message);
        addMessage(botResponse, 'bot'); // Agregar mensaje del chatbot
    }, 500);
}

function closeChat() {
    window.location.href = "index.html"; // Cambia esto a la URL de tu página principal
}
// Función que devuelve respuestas del chatbot (simulación)
function getBotResponse(userMessage) {
    userMessage = userMessage.toLowerCase();

    if (userMessage.includes("hola")) {
        return "¡Hola! Soy Medibot, tu asistente virtual pediátrico. ¿En qué puedo ayudarte?";
    } else if (userMessage.includes("cita")) {
        return "Puedo ayudarte a agendar, modificar o cancelar una cita médica. ¿Qué deseas hacer?";
    } else if (userMessage.includes("gracias")) {
        return "¡De nada! Estoy aquí para ayudarte.";
    } else {
        return "Lo siento, no entiendo tu consulta. ¿Podrías reformularla?";
    }
}

// Función para agregar mensajes al chat
function addMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);

    // Crear la burbuja de mensaje
    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('bubble');
    bubbleDiv.textContent = message;

    // Crear la imagen del avatar
    const avatarDiv = document.createElement('img');
    avatarDiv.classList.add('avatar');
    avatarDiv.src = sender === 'user' ? 'imagenes/icono-usuario.jpeg' : 'imagenes/icono chatbot.jpeg'; // Asegúrate de tener estas imágenes

    // Añadir la imagen y la burbuja al mensaje
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(bubbleDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Desplazar hacia abajo
}
// Función para mostrar la respuesta del bot
function botResponse(userInput) {
    let response = '';
    
    // Respuestas básicas de ejemplo
    if (userInput.toLowerCase().includes('agendar cita')) {
        response = '¿Cuándo te gustaría agendar la cita? Por favor, dime la fecha y hora.';
    } else if (userInput.toLowerCase().includes('editar cita')) {
        response = '¿Qué detalles te gustaría cambiar de tu cita?';
    } else if (userInput.toLowerCase().includes('cancelar cita')) {
        response = '¿Cuál es la cita que te gustaría cancelar? Por favor, proporciona los detalles.';
    } else if (userInput.toLowerCase().includes('hola')) {
        response = '¡Hola! ¿En qué puedo ayudarte hoy?';
    } else {
        response = 'Lo siento, no entendí tu mensaje. ¿Puedes reformularlo?';
    }

    addMessage(response, 'bot');
}

// Función para mostrar/ocultar el indicador de carga
function showLoading(isLoading) {
    const loading = document.getElementById('loading');
    loading.style.display = isLoading ? 'block' : 'none';
}

// Función para agendar una cita, conectándose al backend (ejemplo)
function scheduleAppointment(date, time) {
    const appointmentData = { date, time };

    fetch('https://tu-backend-api.com/agendar-cita', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(appointmentData),
    })
    .then(response => response.json())
    .then(data => {
        addMessage(`Tu cita ha sido agendada para el ${data.date} a las ${data.time}.`, 'bot');
    })
    .catch(error => {
        addMessage('Hubo un error al agendar tu cita. Intenta nuevamente.', 'bot');
        console.error('Error:', error);
    });
}

// Función para editar una cita, conectándose al backend (ejemplo)
function editAppointment(appointmentId, newDate, newTime) {
    const updatedData = { appointmentId, newDate, newTime };

    fetch('https://tu-backend-api.com/editar-cita', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData),
    })
    .then(response => response.json())
    .then(data => {
        addMessage(`Tu cita ha sido actualizada para el ${data.newDate} a las ${data.newTime}.`, 'bot');
    })
    .catch(error => {
        addMessage('Hubo un error al editar tu cita. Intenta nuevamente.', 'bot');
        console.error('Error:', error);
    });
}

// Función para cancelar una cita, conectándose al backend (ejemplo)
function cancelAppointment(appointmentId) {
    fetch(`https://tu-backend-api.com/cancelar-cita/${appointmentId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        addMessage('Tu cita ha sido cancelada exitosamente.', 'bot');
    })
    .catch(error => {
        addMessage('Hubo un error al cancelar tu cita. Intenta nuevamente.', 'bot');
        console.error('Error:', error);
    });
}

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim(); // Eliminamos espacios en blanco

    if (message === "") return; // No enviar mensajes vacíos

    addMessage(message, 'user'); // Agregar mensaje del usuario
    userInput.value = ""; // Limpiar el campo de entrada

    // Simular respuesta del chatbot después de un pequeño retraso
    setTimeout(() => {
        const botResponse = getBotResponse(message);
        addMessage(botResponse, 'bot'); // Agregar mensaje del chatbot
    }, 500);
}

function closeChat() {
    window.location.href = "index.html"; // Cambia esto a la URL de tu página principal
}
// Función que devuelve respuestas del chatbot (simulación)
function getBotResponse(userMessage) {
    userMessage = userMessage.toLowerCase();

    if (userMessage.includes("hola")) {
        return "¡Hola! Soy Medibot, tu asistente virtual pediátrico. ¿En qué puedo ayudarte?";
    } else if (userMessage.includes("cita")) {
        return "Puedo ayudarte a agendar, modificar o cancelar una cita médica. ¿Qué deseas hacer?";
    } else if (userMessage.includes("gracias")) {
        return "¡De nada! Estoy aquí para ayudarte.";
    } else {
        return "Lo siento, no entiendo tu consulta. ¿Podrías reformularla?";
    }
}

// Función para agregar mensajes al chat
/**function addMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);

    // Crear la burbuja de mensaje
    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('bubble');
    bubbleDiv.textContent = message;

    // Crear la imagen del avatar
    const avatarDiv = document.createElement('img');
    avatarDiv.classList.add('avatar');
    avatarDiv.src = sender === 'user' ? 'imagenes/icono usuario.jpg' : 'imagenes/icono chatbot.jpeg'; // Asegúrate de tener estas imágenes

    // Añadir la imagen y la burbuja al mensaje
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(bubbleDiv);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Desplazar hacia abajo
}*/
// Función para mostrar la respuesta del bot
function botResponse(userInput) {
    let response = '';
    
    // Respuestas básicas de ejemplo
    if (userInput.toLowerCase().includes('agendar cita')) {
        response = '¿Cuándo te gustaría agendar la cita? Por favor, dime la fecha y hora.';
    } else if (userInput.toLowerCase().includes('editar cita')) {
        response = '¿Qué detalles te gustaría cambiar de tu cita?';
    } else if (userInput.toLowerCase().includes('cancelar cita')) {
        response = '¿Cuál es la cita que te gustaría cancelar? Por favor, proporciona los detalles.';
    } else if (userInput.toLowerCase().includes('hola')) {
        response = '¡Hola! ¿En qué puedo ayudarte hoy?';
    } else {
        response = 'Lo siento, no entendí tu mensaje. ¿Puedes reformularlo?';
    }

    addMessage(response, 'bot');
}

// Función para mostrar/ocultar el indicador de carga
function showLoading(isLoading) {
    const loading = document.getElementById('loading');
    loading.style.display = isLoading ? 'block' : 'none';
}

// Función para agendar una cita, conectándose al backend (ejemplo)
function scheduleAppointment(date, time) {
    const appointmentData = { date, time };

    fetch('https://tu-backend-api.com/agendar-cita', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(appointmentData),
    })
    .then(response => response.json())
    .then(data => {
        addMessage(`Tu cita ha sido agendada para el ${data.date} a las ${data.time}.`, 'bot');
    })
    .catch(error => {
        addMessage('Hubo un error al agendar tu cita. Intenta nuevamente.', 'bot');
        console.error('Error:', error);
    });
}

// Función para editar una cita, conectándose al backend (ejemplo)
function editAppointment(appointmentId, newDate, newTime) {
    const updatedData = { appointmentId, newDate, newTime };

    fetch('https://tu-backend-api.com/editar-cita', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData),
    })
    .then(response => response.json())
    .then(data => {
        addMessage(`Tu cita ha sido actualizada para el ${data.newDate} a las ${data.newTime}.`, 'bot');
    })
    .catch(error => {
        addMessage('Hubo un error al editar tu cita. Intenta nuevamente.', 'bot');
        console.error('Error:', error);
    });
}

// Función para cancelar una cita, conectándose al backend (ejemplo)
function cancelAppointment(appointmentId) {
    fetch(`https://tu-backend-api.com/cancelar-cita/${appointmentId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        addMessage('Tu cita ha sido cancelada exitosamente.', 'bot');
    })
    .catch(error => {
        addMessage('Hubo un error al cancelar tu cita. Intenta nuevamente.', 'bot');
        console.error('Error:', error);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    showCurrentDate();

    // Escuchar clic en el botón Enviar
    document.getElementById("send-button").addEventListener("click", sendMessage);

    // Escuchar tecla Enter en el input
    document.getElementById("user-input").addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});


// Función para mostrar la fecha actual al inicio del chat
function showCurrentDate() {
    const chatBox = document.getElementById('chat-box');
    const dateDiv = document.createElement('div');
    dateDiv.classList.add('date');

    const now = new Date();
    const options = { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    };

    dateDiv.textContent = "Chat iniciado el " + now.toLocaleDateString('es-ES', options);
    chatBox.appendChild(dateDiv);
}

function getTimeAgo(time) {
    const now = new Date();
    const seconds = Math.floor((now - time) / 1000);

    if (seconds < 60) {
        return `hace ${seconds} segundo${seconds !== 1 ? 's' : ''}`;
    }

    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) {
        return `hace ${minutes} minuto${minutes !== 1 ? 's' : ''}`;
    }

    const hours = Math.floor(minutes / 60);
    if (hours < 24) {
        return `hace ${hours} hora${hours !== 1 ? 's' : ''}`;
    }

    const days = Math.floor(hours / 24);
    return `hace ${days} día${days !== 1 ? 's' : ''}`;
}


let lastBotMessageTime = null;

function addMessage(message, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);

    // Crear la imagen del avatar
    const avatarDiv = document.createElement('img');
    avatarDiv.classList.add('avatar');
    avatarDiv.src = sender === 'user' ? 'imagenes/icono-usuario.jpeg' : 'imagenes/icono chatbot.jpeg';

    // Contenedor para la burbuja y el timestamp
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('bubble-container');

    // Crear la burbuja de mensaje
    const bubbleDiv = document.createElement('div');
    bubbleDiv.classList.add('bubble');
    bubbleDiv.textContent = message;

    contentDiv.appendChild(bubbleDiv);

    // Agregar tiempo debajo de la burbuja si es del bot
    if (sender === 'bot') {
        const timeAgoSpan = document.createElement('span');
        timeAgoSpan.classList.add('time-ago');
        const timestamp = new Date();
        timeAgoSpan.setAttribute('data-timestamp', timestamp.getTime());
        timeAgoSpan.textContent = getTimeAgo(timestamp);
        contentDiv.appendChild(timeAgoSpan);

        // Actualizar el tiempo cada 60 segundos
        setInterval(() => {
            timeAgoSpan.textContent = getTimeAgo(new Date(parseInt(timeAgoSpan.getAttribute('data-timestamp'))));
        }, 10000);
    }

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);

    chatBox.appendChild(messageDiv);
    
    // Desplazar hacia abajo solo después de agregar el mensaje
    setTimeout(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 0);  // Ejecutar el scroll después de que el navegador haya agregado el mensaje
}
