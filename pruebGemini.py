import google.generativeai as genai

# Configura tu API Key (reemplaza con la tuya o usa una variable de entorno)
genai.configure(api_key="AIzaSyAzgTPEg_Y4_qb9TIlRQhHjt9N4TG3grAU")

# Usa el modelo correcto y compatible
model = genai.GenerativeModel('gemini-1.5-flash')

# Envía el mensaje
response = model.generate_content("¿Qué es la varicela?")

# Muestra la respuesta
print(response.text)