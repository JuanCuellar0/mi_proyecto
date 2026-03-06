"""
Configuración de Swagger/OpenAPI para documentación de API
"""

SWAGGER_CONFIG = {
    "swagger": "2.0",
    "info": {
        "title": "API Mi Proyecto EduRetention",
        "description": "API REST con 24 rutas CRUD para gestionar caracterizaciones, contactos y datos relacionados",
        "contact": {
            "email": "soporte@miproyecto.com"
        },
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": [
        "http"
    ],
    "tags": [
        {
            "name": "Caracterizacion",
            "description": "Gestión de caracterizaciones completas"
        },
        {
            "name": "Contacto",
            "description": "Gestión de mensajes de contacto"
        },
        {
            "name": "Personal",
            "description": "Gestión de datos personales"
        },
        {
            "name": "Ubicacion",
            "description": "Gestión de ubicación y contacto"
        },
        {
            "name": "Socioeconomica",
            "description": "Gestión de datos socioeconómicos"
        },
        {
            "name": "Diversidad",
            "description": "Gestión de diversidad e inclusión"
        }
    ]
}

# Definiciones de esquemas para Swagger
DEFINITIONS = {
    "Caracterizacion": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "fecha": {"type": "string", "format": "date-time"},
            "genero": {"type": "string"},
            "edad": {"type": "integer"},
            "trabaja": {"type": "string"},
            "residencia": {"type": "string"}
        }
    },
    "Contacto": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "fecha": {"type": "string", "format": "date-time"},
            "nombre": {"type": "string"},
            "correo": {"type": "string", "format": "email"},
            "mensaje": {"type": "string"}
        }
    },
    "Personal": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "caracterizacion_id": {"type": "integer"},
            "tipo_documento": {"type": "string"},
            "identificacion": {"type": "string"},
            "fecha_expedicion": {"type": "string", "format": "date"},
            "lugar_expedicion": {"type": "string"},
            "primer_nombre": {"type": "string"},
            "segundo_nombre": {"type": "string"},
            "primer_apellido": {"type": "string"},
            "segundo_apellido": {"type": "string"},
            "libreta_militar": {"type": "string"},
            "distrito_militar": {"type": "string"},
            "tipo_sanguineo": {"type": "string"},
            "eps_afiliacion": {"type": "string"},
            "otra_eps": {"type": "string"},
            "estado_civil": {"type": "string"},
            "pais_origen": {"type": "string"},
            "departamento_origen": {"type": "string"},
            "ciudad_origen": {"type": "string"},
            "fecha_nacimiento": {"type": "string", "format": "date"}
        }
    },
    "Ubicacion": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "caracterizacion_id": {"type": "integer"},
            "pais": {"type": "string"},
            "departamento": {"type": "string"},
            "ciudad": {"type": "string"},
            "barrio": {"type": "string"},
            "direccion": {"type": "string"},
            "telefono_contacto": {"type": "string"},
            "telefono_celular": {"type": "string"},
            "correo_electronico": {"type": "string"},
            "direccion_correspondencia": {"type": "string"}
        }
    },
    "Socioeconomica": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "caracterizacion_id": {"type": "integer"},
            "sisben_sn": {"type": "string"},
            "grupo_sisben": {"type": "string"},
            "estrato": {"type": "string"},
            "acceso": {"type": "string"}
        }
    },
    "Diversidad": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "caracterizacion_id": {"type": "integer"},
            "pueblo_indigena": {"type": "string"},
            "comunidad_negra": {"type": "string"},
            "tiene_discapacidad": {"type": "string"},
            "tipo_discapacidad": {"type": "string"},
            "capacidad_excepcional": {"type": "string"},
            "desv_grupos_armados": {"type": "string"},
            "vulnerabilidad_social": {"type": "string"},
            "orientacion_sexual": {"type": "string"},
            "consume_psicoactiva": {"type": "string"}
        }
    },
    "Academica": {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "caracterizacion_id": {"type": "integer"},
            "motivo_principal": {"type": "string"},
            "motivo_otro": {"type": "string"},
            "promedio": {"type": "number", "format": "float"},
            "nivel_manejo": {"type": "string"}
        }
    }
}
