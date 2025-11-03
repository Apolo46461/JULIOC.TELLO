#!/usr/bin/env python3
"""
Script para recrear la base de datos del CETPRO desde cero
"""

import os
import shutil
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime, date

# Crear aplicación temporal
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cetpro-julio-tello-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath("database/cetpro.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir todos los modelos en el mismo archivo
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # director, docente, administrativo, estudiante
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(8), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class CentroEducativo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, default="I.E. CEPTRO JULIO C. TELLO")
    lema = db.Column(db.String(200), default="FORMAR ESTUDIANTES COMPETENTES, PARA INSERTARLOS EN EL MERCADO LABORAL")
    ubicacion = db.Column(db.String(200), default="Urb. El Carmen Panamericana Sur Km 301 San Joaquín, Ica - Perú")
    ano_actual = db.Column(db.String(4), default="2025")
    eslogan_ano = db.Column(db.String(200), default="AÑO DE LA CONSOLIDACIÓN DEL MAR DE GRAU")
    vision = db.Column(db.Text, default="Al 2021 nuestra Institución Educativa será líder en la formación integral de los estudiantes y la excelencia educativa; con moderna infraestructura, equipamiento tecnológico y aulas inteligentes que contribuirán a la realización personal y social del hombre para el gran cambio socio económico y cultural de la comunidad y el país.")
    mision = db.Column(db.Text, default="Somos una Institución Educativa conformada por docentes altamente calificados que enfrentamos los retos del mundo científico y tecnológico a fin de lograr mejores estándares de calidad educativa. Formamos estudiantes competentes que desarrollan sus capacidades utilizando una metodología activa, respetando sus individualidades y su condición de personas a través de la práctica permanente de valores.")
    director_actual = db.Column(db.String(100), default="Prof. Román H. Camargo Alegría")
    capacidad_estudiantes = db.Column(db.Integer, default=350)
    area_terreno = db.Column(db.String(50), default="1,200 m²")
    aulas_talleres = db.Column(db.Integer, default=4)
    servicios_higienicos = db.Column(db.Integer, default=2)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FamiliaProfesional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    color_identificatorio = db.Column(db.String(7))
    icono = db.Column(db.String(50))
    activa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Modulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    duracion_horas = db.Column(db.Integer, default=40)
    familia_id = db.Column(db.Integer, db.ForeignKey('familia_profesional.id'), nullable=False)
    tipo_modulo = db.Column(db.String(20), default='profesional')
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Competencia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)
    tipo_competencia = db.Column(db.String(20), default='especifica')
    nivel_dominio = db.Column(db.String(20), default='basico')
    activa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Horario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)
    dia_semana = db.Column(db.String(20), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    aula = db.Column(db.String(20))
    cupos_maximos = db.Column(db.Integer, default=30)
    cupos_ocupados = db.Column(db.Integer, default=0)
    profesor_id = db.Column(db.Integer, nullable=True)
    periodo_academico = db.Column(db.String(20), default='2025-01')
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Estudiante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    familia_profesional_id = db.Column(db.Integer, db.ForeignKey('familia_profesional.id'))
    procedencia = db.Column(db.String(100))
    motivacion_ingreso = db.Column(db.Text)
    expectativas_laborales = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('estudiante', uselist=False))
    familia_profesional = db.relationship('FamiliaProfesional', backref='estudiantes')

class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    familia_profesional_id = db.Column(db.Integer, db.ForeignKey('familia_profesional.id'))
    titulo_profesional = db.Column(db.String(100))
    experiencia_laboral = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('profesor', uselist=False))
    familia_profesional = db.relationship('FamiliaProfesional', backref='profesores')

class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    familia_profesional_id = db.Column(db.Integer, db.ForeignKey('familia_profesional.id'), nullable=False)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesor.id'), nullable=False)
    horario = db.Column(db.String(50))
    aula = db.Column(db.String(20))
    cupos_maximos = db.Column(db.Integer, default=30)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    familia_profesional = db.relationship('FamiliaProfesional', backref='cursos')
    modulo = db.relationship('Modulo', backref='cursos')
    profesor = db.relationship('Profesor', backref='cursos_asignados')

class Matricula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
    fecha_matricula = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='activo')
    nota_final = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    estudiante = db.relationship('Estudiante', backref='matriculas')
    curso = db.relationship('Curso', backref='matriculas')

class MatriculaModulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)
    horario_id = db.Column(db.Integer, db.ForeignKey('horario.id'), nullable=False)
    fecha_matricula = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='activo')
    nota_final = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    estudiante = db.relationship('Estudiante', backref='matriculas_modulos')

class Evaluacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula_modulo_id = db.Column(db.Integer, db.ForeignKey('matricula_modulo.id'), nullable=False)
    competencia_id = db.Column(db.Integer, db.ForeignKey('competencia.id'), nullable=False)
    tipo_evaluacion = db.Column(db.String(20), default='continua')
    calificacion = db.Column(db.Float, nullable=False)
    observaciones = db.Column(db.Text)
    fecha_evaluacion = db.Column(db.DateTime, default=datetime.utcnow)
    evaluador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    evaluador = db.relationship('User', backref='evaluaciones_realizadas')

class ProyectoProductivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    estudiante_id = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)
    tipo_proyecto = db.Column(db.String(50), default='bien')
    estado = db.Column(db.String(20), default='propuesta')
    ingresos_generados = db.Column(db.Float, default=0.0)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date)
    calificacion = db.Column(db.Float)
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    estudiante = db.relationship('Estudiante', backref='proyectos_productivos')

class ValidacionCampo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tabla_validada = db.Column(db.String(50), nullable=False)
    campo_validado = db.Column(db.String(50), nullable=False)
    valor_validado = db.Column(db.String(200))
    tipo_validacion = db.Column(db.String(50), nullable=False)
    resultado = db.Column(db.Boolean, nullable=False)
    mensaje_error = db.Column(db.String(200))
    fecha_validacion = db.Column(db.DateTime, default=datetime.utcnow)

def crear_usuarios_iniciales():
    """Crear usuarios iniciales del sistema"""
    usuarios = [
        {
            'username': 'director',
            'email': 'director@cetpro.edu.pe',
            'password': 'director123',
            'role': 'director',
            'nombres': 'Román H.',
            'apellidos': 'Camargo Alegría',
            'dni': '12345678',
            'telefono': '999888777',
            'fecha_nacimiento': date(1975, 5, 15)
        },
        {
            'username': 'docente',
            'email': 'docente@cetpro.edu.pe',
            'password': 'docente123',
            'role': 'docente',
            'nombres': 'María Elena',
            'apellidos': 'García López',
            'dni': '87654321',
            'telefono': '999666555',
            'fecha_nacimiento': date(1980, 8, 20)
        },
        {
            'username': 'admin',
            'email': 'admin@cetpro.edu.pe',
            'password': 'admin123',
            'role': 'administrativo',
            'nombres': 'Carlos Alberto',
            'apellidos': 'Rodríguez Mendoza',
            'dni': '11223344',
            'telefono': '999444333',
            'fecha_nacimiento': date(1985, 3, 10)
        },
        {
            'username': 'estudiante',
            'email': 'estudiante@cetpro.edu.pe',
            'password': 'estudiante123',
            'role': 'estudiante',
            'nombres': 'Ana Lucía',
            'apellidos': 'Martínez Quispe',
            'dni': '55667788',
            'telefono': '999222111',
            'fecha_nacimiento': date(2000, 12, 5)
        }
    ]

    for usuario_data in usuarios:
        usuario = User(
            username=usuario_data['username'],
            email=usuario_data['email'],
            role=usuario_data['role'],
            nombres=usuario_data['nombres'],
            apellidos=usuario_data['apellidos'],
            dni=usuario_data['dni'],
            telefono=usuario_data['telefono'],
            fecha_nacimiento=usuario_data['fecha_nacimiento']
        )
        usuario.set_password(usuario_data['password'])
        db.session.add(usuario)

    db.session.commit()

def inicializar_datos_cetpro():
    """Inicializar los datos básicos del CETPRO"""
    # Crear centro educativo
    centro = CentroEducativo.query.first()
    if not centro:
        centro = CentroEducativo()
        db.session.add(centro)

    # Crear familias profesionales
    familias_data = [
        {
            'nombre': 'ESTÉTICA PERSONAL',
            'descripcion': 'Formación en servicios de belleza y cuidado personal',
            'color': '#FF69B4',
            'icono': 'fas fa-cut'
        },
        {
            'nombre': 'HOSTELERÍA Y TURISMO',
            'descripcion': 'Formación en servicios gastronómicos y turísticos',
            'color': '#32CD32',
            'icono': 'fas fa-utensils'
        },
        {
            'nombre': 'ARTESANÍA Y MANUALIDADES',
            'descripcion': 'Desarrollo de habilidades artísticas y manuales',
            'color': '#FFD700',
            'icono': 'fas fa-palette'
        },
        {
            'nombre': 'TEXTILES Y CONFECCIONES',
            'descripcion': 'Diseño y confección de prendas de vestir',
            'color': '#4169E1',
            'icono': 'fas fa-tshirt'
        }
    ]

    for familia_data in familias_data:
        familia = FamiliaProfesional.query.filter_by(nombre=familia_data['nombre']).first()
        if not familia:
            familia = FamiliaProfesional(
                nombre=familia_data['nombre'],
                descripcion=familia_data['descripcion'],
                color_identificatorio=familia_data['color'],
                icono=familia_data['icono']
            )
            db.session.add(familia)

    # Crear módulos
    modulos_data = {
        'ESTÉTICA PERSONAL': ['Corte de cabello', 'Ondulaciones', 'Tinturación', 'Peinados'],
        'HOSTELERÍA Y TURISMO': ['Elaboración de productos de pastelería', 'Elaboración de productos de panadería', 'Acondicionamiento del área de cocina', 'Técnicas culinarias'],
        'ARTESANÍA Y MANUALIDADES': ['Decoración de eventos especiales', 'Estampados', 'Pirograbado'],
        'TEXTILES Y CONFECCIONES': ['Artículos textiles', 'Confección de prendas de vestir de dama', 'Confección de prendas de vestir de niños', 'Confección de prendas de vestir de caballeros']
    }

    for familia_nombre, modulos_lista in modulos_data.items():
        familia = FamiliaProfesional.query.filter_by(nombre=familia_nombre).first()
        if familia:
            for modulo_nombre in modulos_lista:
                modulo = Modulo.query.filter_by(nombre=modulo_nombre, familia_id=familia.id).first()
                if not modulo:
                    modulo = Modulo(
                        nombre=modulo_nombre,
                        descripcion=f"Módulo de {modulo_nombre}",
                        familia_id=familia.id
                    )
                    db.session.add(modulo)

    db.session.commit()

def main():
    print("🔄 Recreando base de datos del CETPRO...")

    # Eliminar base de datos existente si existe
    if os.path.exists('database/cetpro.db'):
        print("🗑️  Eliminando base de datos existente...")
        os.remove('database/cetpro.db')

    # Crear directorio si no existe
    os.makedirs('database', exist_ok=True)

    # Crear todas las tablas
    print("📋 Creando tablas...")
    with app.app_context():
        db.create_all()

        # Crear usuarios iniciales
        print("👥 Creando usuarios iniciales...")
        crear_usuarios_iniciales()

        # Inicializar datos del CETPRO
        print("🏫 Inicializando datos del CETPRO...")
        inicializar_datos_cetpro()

        print("✅ Base de datos recreada exitosamente!")
        print("📝 Usuarios creados:")
        print("   Director: director / director123")
        print("   Docente: docente / docente123")
        print("   Administrativo: admin / admin123")
        print("   Estudiante: estudiante / estudiante123")

if __name__ == '__main__':
    main()
