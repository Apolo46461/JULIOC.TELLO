from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cetpro-julio-tello-2025'

# Programas de estudio
PROGRAMAS = [
    {"nombre": "Informática", "descripcion": "Formación en desarrollo de software, mantenimiento de equipos y redes informáticas.", "duracion": "2 años", "icono": "fas fa-laptop-code"},
    {"nombre": "Mecánica Industrial", "descripcion": "Especialización en mantenimiento industrial, soldadura y control de calidad.", "duracion": "2 años", "icono": "fas fa-tools"},
    {"nombre": "Confección Textil", "descripcion": "Diseño y confección de prendas de vestir, control de calidad textil.", "duracion": "1.5 años", "icono": "fas fa-cut"},
    {"nombre": "Gastronomía", "descripcion": "Arte culinario, panadería, pastelería y servicio de alimentos y bebidas.", "duracion": "1.5 años", "icono": "fas fa-utensils"},
    {"nombre": "Electricidad Industrial", "descripcion": "Instalaciones eléctricas, mantenimiento de sistemas eléctricos industriales.", "duracion": "2 años", "icono": "fas fa-bolt"},
    {"nombre": "Estética Personal", "descripcion": "Cuidado personal, cosmetología, peluquería y técnicas de belleza.", "duracion": "1 año", "icono": "fas fa-spa"},
]

# Imágenes para el slider
SLIDER_IMAGES = [
    "slider1.jpg",
    "slider2.jpg",
    "slider3.jpg",
    "slider4.jpg"
]

@app.route("/")
def landing():
    return render_template(
        "landing.html",
        slider_images=SLIDER_IMAGES,
        programas=PROGRAMAS
    )

@app.route("/inscripcion", methods=["POST"])
def inscripcion():
    nombres = request.form.get("nombres")
    apellidos = request.form.get("apellidos")
    email = request.form.get("email")
    telefono = request.form.get("telefono")
    dni = request.form.get("dni")
    programa = request.form.get("programa")
    mensaje = request.form.get("mensaje")

    # Server-side validation
    errors = []

    # Validate DNI: exactly 8 digits
    if not dni or not dni.isdigit() or len(dni) != 8:
        errors.append("DNI debe tener exactamente 8 dígitos numéricos.")

    # Validate telefono: exactly 9 digits starting with 9
    if not telefono or not telefono.isdigit() or len(telefono) != 9 or not telefono.startswith('9'):
        errors.append("Teléfono debe tener exactamente 9 dígitos numéricos empezando con 9.")

    # Validate email: basic format
    import re
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if not email or not re.match(email_regex, email):
        errors.append("Email debe tener un formato válido.")

    # Validate required fields
    if not nombres or not apellidos or not programa:
        errors.append("Nombres, apellidos y programa son campos obligatorios.")

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for('landing') + "#inscripcion")

    # Determinar saludo basado en la hora de Perú (UTC-5)
    utc_now = datetime.now(timezone.utc)
    peru_time = utc_now - timedelta(hours=5)
    hora = peru_time.hour

    if 6 <= hora < 12:
        saludo = "Buenos días Dr. Camargo"
    elif 12 <= hora < 18:
        saludo = "Buenas tardes Dr. Camargo"
    else:
        saludo = "Buenas noches Dr. Camargo"

    # Crear mensaje para WhatsApp
    mensaje_whatsapp = f"""{saludo}

*Nueva Inscripción CETPRO Julio C. Tello*

👤 *Datos Personales:*
• Nombre: {nombres} {apellidos}
• Email: {email}
• Teléfono: {telefono}
• DNI: {dni}

📚 *Programa de Interés:* {programa}

💬 *Mensaje:* {mensaje if mensaje else 'Sin mensaje adicional'}

---
_Enviado desde el formulario web del CETPRO_"""

    # Codificar el mensaje para URL de WhatsApp
    from urllib.parse import quote
    mensaje_codificado = quote(mensaje_whatsapp)

    # Número de WhatsApp del CETPRO (cambiar por el real)
    numero_whatsapp = "51956099016"  # Este es el número que ya tienes en el botón de WhatsApp

    # URL de WhatsApp con el mensaje pre-llenado
    whatsapp_url = f"https://wa.me/{numero_whatsapp}?text={mensaje_codificado}"

    flash("¡Redirigiendo a WhatsApp para enviar tu inscripción!", "success")

    # Redirigir a WhatsApp en lugar de volver a la página
    return redirect(whatsapp_url)

if __name__ == '__main__':
    app.run(debug=True)
