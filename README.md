# CETPRO - Sistema de Gestión Educativa

Un sistema completo de gestión para Centros de Educación Técnica Productiva (CETPRO) desarrollado con Flask y SQLite.

## 🚀 Características

- **Gestión de Usuarios**: Sistema de autenticación con roles (Estudiante, Profesor, Administrador)
- **Panel de Control**: Dashboard personalizado según el rol del usuario
- **Gestión de Estudiantes**: Registro, edición y seguimiento de estudiantes
- **Gestión de Profesores**: Administración del personal docente
- **Gestión de Cursos**: Creación y administración de cursos por nivel y grado
- **Sistema de Matrículas**: Inscripción de estudiantes en cursos
- **Base de Datos SQLite**: Almacenamiento local y confiable
- **Interfaz Moderna**: Diseño responsivo con Bootstrap 5
- **Funcionalidades Avanzadas**: Búsqueda, filtros, exportación de datos

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. **Clonar o descargar el proyecto**:
   ```bash
   # Si tienes git instalado
   git clone [url-del-repositorio]
   cd CETPRO
   ```

2. **Crear y activar el entorno virtual**:
   ```bash
   # Crear entorno virtual
   python -m venv cetpro_env

   # Activar entorno virtual (Windows)
   cetpro_env\Scripts\activate

   # Activar entorno virtual (Linux/Mac)
   source cetpro_env/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**:
   ```bash
   # La base de datos se creará automáticamente al ejecutar la aplicación
   # No es necesario ningún comando adicional
   ```

## 🚀 Ejecución

1. **Activar el entorno virtual** (si no está activado):
   ```bash
   # Windows
   cetpro_env\Scripts\activate

   # Linux/Mac
   source cetpro_env/bin/activate
   ```

2. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```

3. **Acceder al sistema**:
   - Abrir el navegador web
   - Ir a: `http://localhost:5000`
   - Iniciar sesión con las credenciales de administrador

## 👥 Usuarios por Defecto

### Administrador
- **Usuario**: admin
- **Contraseña**: admin123
- **Rol**: Administrador (acceso completo al sistema)

### Profesor
- **Usuario**: profesor
- **Contraseña**: profesor123
- **Rol**: Profesor (gestión de cursos y estudiantes)

### Estudiante
- **Usuario**: estudiante
- **Contraseña**: estudiante123
- **Rol**: Estudiante (visualización de cursos y matrículas)

## 📁 Estructura del Proyecto

```
CETPRO/
├── app/                          # Código de la aplicación
│   ├── __init__.py              # Configuración de Flask
│   ├── models.py                # Modelos de base de datos
│   └── routes/                  # Rutas de la aplicación
│       ├── __init__.py
│       ├── auth.py              # Rutas de autenticación
│       ├── dashboard.py         # Rutas del dashboard
│       ├── estudiantes.py       # Rutas de gestión de estudiantes
│       ├── profesores.py        # Rutas de gestión de profesores
│       └── cursos.py            # Rutas de gestión de cursos
├── database/                    # Base de datos SQLite
├── static/                      # Archivos estáticos
│   ├── css/
│   │   └── styles.css           # Estilos personalizados
│   ├── js/
│   │   └── scripts.js           # Funcionalidades JavaScript
│   └── images/                  # Imágenes del sistema
├── templates/                   # Plantillas HTML
│   ├── base.html               # Plantilla base
│   ├── login.html              # Página de inicio de sesión
│   ├── dashboard_admin.html    # Dashboard administrador
│   ├── dashboard_profesor.html # Dashboard profesor
│   └── dashboard_estudiante.html # Dashboard estudiante
├── app.py                      # Archivo principal
├── requirements.txt            # Dependencias de Python
├── .gitignore                  # Archivos a ignorar en git
└── README.md                   # Documentación del proyecto
```

## 🎨 Características de la Interfaz

- **Diseño Responsivo**: Se adapta a dispositivos móviles y tablets
- **Tema Moderno**: Interfaz limpia y profesional
- **Navegación Intuitiva**: Menús organizados por roles
- **Feedback Visual**: Notificaciones y alertas informativas
- **Accesibilidad**: Cumple con estándares de accesibilidad web

## 🔧 Funcionalidades Avanzadas

### Para Estudiantes
- Visualización de información personal
- Exploración de cursos disponibles
- Matrícula en cursos
- Seguimiento de progreso académico

### Para Profesores
- Gestión de cursos asignados
- Visualización de estudiantes matriculados
- Estadísticas de rendimiento
- Perfil profesional

### Para Administradores
- Gestión completa de usuarios
- Creación y edición de cursos
- Asignación de profesores
- Reportes y estadísticas
- Configuración del sistema

## 📊 Base de Datos

El sistema utiliza SQLite con las siguientes tablas principales:

- **users**: Información de usuarios del sistema
- **estudiantes**: Datos específicos de estudiantes
- **profesores**: Información del personal docente
- **cursos**: Catálogo de cursos disponibles
- **matriculas**: Registro de inscripciones

## 🔒 Seguridad

- **Autenticación**: Sistema de login seguro
- **Autorización**: Control de acceso por roles
- **Validación**: Validación de datos en cliente y servidor
- **Encriptación**: Contraseñas encriptadas
- **Protección CSRF**: Prevención de ataques CSRF

## 🌐 Compatibilidad

- **Navegadores**: Chrome, Firefox, Safari, Edge
- **Dispositivos**: Desktop, tablets, móviles
- **Sistemas Operativos**: Windows, Linux, macOS

## 📝 Notas de Desarrollo

- El sistema está desarrollado con Flask 2.3.3
- Utiliza SQLAlchemy para la gestión de la base de datos
- Bootstrap 5 para la interfaz de usuario
- Font Awesome para iconografía
- JavaScript vanilla para funcionalidades interactivas

## 🐛 Solución de Problemas

### Error común: "Module not found"
```bash
# Asegurarse de que el entorno virtual esté activado
cetpro_env\Scripts\activate  # Windows
source cetpro_env/bin/activate  # Linux/Mac

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error de base de datos
```bash
# Eliminar la base de datos existente
rm database/cetpro.db

# Reiniciar la aplicación
python app.py
```

## 📞 Soporte

Para soporte técnico o reportar problemas:
- Crear un issue en el repositorio
- Contactar al equipo de desarrollo
- Consultar la documentación

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## 👨‍💻 Desarrollado por

Equipo de Desarrollo CETPRO
- Framework: Flask
- Base de datos: SQLite
- Frontend: Bootstrap 5
- Versión: 1.0.0

---

**¡Gracias por usar CETPRO - Sistema de Gestión Educativa!** 🎓
