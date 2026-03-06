from flask import Flask, render_template, request, redirect, url_for
from flasgger import Flasgger
from swagger_config import SWAGGER_CONFIG, DEFINITIONS
from database import Database, DatabaseConfig
from models import Caracterizacion, Contacto
from services import (
  CaracterizacionRepository, 
  ContactoRepository, 
  RiskAnalysisRepository,
  CaracterizacionPersonalRepository,
  CaracterizacionUbicacionRepository,
  CaracterizacionSocioeconomicaRepository,
  CaracterizacionDiversidadRepository
)


# Configuración
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Inicializar Flasgger para Swagger
swagger_template = SWAGGER_CONFIG.copy()
swagger_template["definitions"] = DEFINITIONS

swagger = Flasgger(app, template=swagger_template)

db_config = DatabaseConfig(
  host="127.0.0.1",
  user="root",
  password="",
  database="mi_proyecto",
  charset="utf8mb4"
)

db = Database(db_config)
caracterizacion_repo = CaracterizacionRepository(db)
contacto_repo = ContactoRepository(db)
risk_analysis_repo = RiskAnalysisRepository(caracterizacion_repo)

# Repositorios para tablas secundarias de caracterización
personal_repo = CaracterizacionPersonalRepository(db)
ubicacion_repo = CaracterizacionUbicacionRepository(db)
socioeconomica_repo = CaracterizacionSocioeconomicaRepository(db)
diversidad_repo = CaracterizacionDiversidadRepository(db)



class AppInitializer:
  """Inicializa la aplicación y base de datos"""
  
  @staticmethod
  def initialize():
    """Inicializa todo lo necesario"""
    db.create_database_if_not_exists()
    caracterizacion_repo.initialize_table()
    contacto_repo.initialize_table()


# ============ RUTAS PRINCIPALES ============

@app.route('/')
def home():
  """Página de inicio"""
  return render_template('index.html')


@app.route('/encuesta')
def encuesta():
  """Página del formulario de encuesta"""
  return render_template('encuesta.html', caracterizacion=None)


# ============ PROCESAMIENTO DE FORMULARIOS ============

@app.route('/enviar_caracterizacion', methods=['POST'])
def enviar_caracterizacion():
  """Procesa y guarda el formulario de caracterización"""
  try:
    # Crear instancia desde datos del formulario
    caracterizacion = Caracterizacion.from_form_data(request.form)
    
    # Guardar en base de datos
    caracterizacion_repo.create(caracterizacion)
    
    return redirect(url_for('gracias_enc'))
  except Exception as e:
    print(f"Error al guardar caracterizacion: {e}")
    return redirect(url_for('gracias_enc'))


@app.route('/enviar_contacto', methods=['POST'])
def enviar_contacto():
  """Procesa y guarda un mensaje de contacto"""
  try:
    contacto = Contacto(
      nombre=request.form.get('nombre', '').strip(),
      correo=request.form.get('correo', '').strip(),
      mensaje=request.form.get('mensaje', '').strip()
    )
    if contacto.nombre and contacto.correo and contacto.mensaje:
      contacto_repo.create(contacto)
    return redirect(url_for('gracias_enc'))
  except Exception as e:
    print(f"Error al guardar contacto: {e}")
    return redirect(url_for('gracias_enc'))


# ============ PÁGINAS DE CONFIRMACIÓN Y RESULTADOS ============

@app.route('/gracias_enc')
def gracias_enc():
  """Página de agradecimiento"""
  return render_template('gracias.html')


@app.route('/resultados_caracterizacion')
def resultados_caracterizacion():
  """Muestra el análisis de riesgo de deserción"""
  resultados = risk_analysis_repo.analyze_all()
  return render_template('resultados.html', filas=resultados)


@app.route('/contactos_listado')
def contactos_listado():
  """Muestra el listado de mensajes de contacto"""
  contactos = contacto_repo.get_all()
  return render_template('resultados.html', filas=contactos)


# ============ ANÁLISIS DE RIESGO ============

@app.route('/analisis_riesgo')
def analisis_riesgo():
  """Muestra el análisis de riesgo de deserción"""
  resultados = risk_analysis_repo.analyze_all()
  return render_template('resultados.html', filas=resultados)


# ============ RUTAS CRUD TABLA 1: CARACTERIZACION ============

# 1. POST /api/caracterizaciones - INSERT
@app.route('/api/caracterizaciones', methods=['POST'])
def api_create_caracterizacion():
  """
  Crear nueva caracterización
  ---
  tags:
    - Caracterizacion
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          genero:
            type: string
            example: "M"
          edad:
            type: integer
            example: 20
          trabaja:
            type: string
            example: "Si"
          residencia:
            type: string
            example: "Casa"
  responses:
    201:
      description: Caracterización creada exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
          message:
            type: string
          id:
            type: integer
  """
  try:
    datos = request.get_json()
    caracterizacion = Caracterizacion(
      genero=datos.get('genero', ''),
      edad=datos.get('edad'),
      residencia=datos.get('residencia', ''),
      trabaja=datos.get('trabaja', '')
    )
    result_id = caracterizacion_repo.create(caracterizacion)
    return {'status': 'success', 'message': 'Creado exitosamente', 'id': result_id}, 201
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 2. GET /api/caracterizaciones/<id> - SELECT
@app.route('/api/caracterizaciones/<int:id>', methods=['GET'])
def api_get_caracterizacion(id):
  """
  Obtener caracterización por ID
  ---
  tags:
    - Caracterizacion
  parameters:
    - in: path
      name: id
      type: integer
      required: true
  responses:
    200:
      description: Datos de la caracterización
  """
  try:
    resultado = caracterizacion_repo.get_by_id(id)
    if resultado:
      return {'status': 'success', 'data': resultado}, 200
    return {'status': 'error', 'message': 'No encontrado'}, 404
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 500


# 3. PUT /api/caracterizaciones/<id> - UPDATE
@app.route('/api/caracterizaciones/<int:id>', methods=['PUT'])
def api_update_caracterizacion(id):
  """
  Actualizar caracterización
  ---
  tags:
    - Caracterizacion
  parameters:
    - in: path
      name: id
      type: integer
      required: true
    - in: body
      name: body
      schema:
        type: object
        properties:
          genero:
            type: string
          edad:
            type: integer
          trabaja:
            type: string
          residencia:
            type: string
  responses:
    200:
      description: Actualizado exitosamente
  """
  try:
    datos = request.get_json()
    char_dict = caracterizacion_repo.get_by_id(id)
    if not char_dict:
      return {'status': 'error', 'message': 'No encontrado'}, 404
    caracterizacion = Caracterizacion(
      genero=datos.get('genero', char_dict.get('genero', '')),
      edad=datos.get('edad', char_dict.get('edad')),
      residencia=datos.get('residencia', char_dict.get('residencia', '')),
      trabaja=datos.get('trabaja', char_dict.get('trabaja', ''))
    )
    caracterizacion_repo.update(id, caracterizacion)
    return {'status': 'success', 'message': 'Actualizado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 4. DELETE /api/caracterizaciones/<id> - DELETE
@app.route('/api/caracterizaciones/<int:id>', methods=['DELETE'])
def api_delete_caracterizacion(id):
  """
  Eliminar caracterización
  ---
  tags:
    - Caracterizacion
  parameters:
    - in: path
      name: id
      type: integer
      required: true
  responses:
    200:
      description: Eliminado exitosamente
  """
  try:
    caracterizacion_repo.delete_by_id(id)
    return {'status': 'success', 'message': 'Eliminado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# ============ RUTAS CRUD TABLA 2: CONTACTO ============

# 5. POST /api/contactos - INSERT
@app.route('/api/contactos', methods=['POST'])
def api_create_contacto():
  """
  Crear nuevo contacto
  ---
  tags:
    - Contacto
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          nombre:
            type: string
          correo:
            type: string
          mensaje:
            type: string
  responses:
    201:
      description: Contacto creado exitosamente
  """
  try:
    datos = request.get_json()
    contacto = Contacto(
      nombre=datos.get('nombre', '').strip(),
      correo=datos.get('correo', '').strip(),
      mensaje=datos.get('mensaje', '').strip()
    )
    if contacto.nombre and contacto.correo and contacto.mensaje:
      contacto_repo.create(contacto)
      return {'status': 'success', 'message': 'Creado exitosamente'}, 201
    return {'status': 'error', 'message': 'Campos requeridos vacíos'}, 400
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 6. GET /api/contactos/<id> - SELECT
@app.route('/api/contactos/<int:id>', methods=['GET'])
def api_get_contacto(id):
  """
  Obtener contacto por ID
  ---
  tags:
    - Contacto
  parameters:
    - in: path
      name: id
      type: integer
      required: true
  responses:
    200:
      description: Datos del contacto
  """
  try:
    resultado = contacto_repo.get_by_id(id)
    if resultado:
      return {'status': 'success', 'data': resultado}, 200
    return {'status': 'error', 'message': 'No encontrado'}, 404
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 500


# 7. PUT /api/contactos/<id> - UPDATE
@app.route('/api/contactos/<int:id>', methods=['PUT'])
def api_update_contacto(id):
  """
  Actualizar contacto
  ---
  tags:
    - Contacto
  parameters:
    - in: path
      name: id
      type: integer
      required: true
    - in: body
      name: body
      schema:
        type: object
        properties:
          nombre:
            type: string
          correo:
            type: string
          mensaje:
            type: string
  responses:
    200:
      description: Actualizado exitosamente
  """
  try:
    datos = request.get_json()
    contacto_dict = contacto_repo.get_by_id(id)
    if not contacto_dict:
      return {'status': 'error', 'message': 'No encontrado'}, 404
    contacto = Contacto(
      nombre=datos.get('nombre', contacto_dict.get('nombre', '')).strip(),
      correo=datos.get('correo', contacto_dict.get('correo', '')).strip(),
      mensaje=datos.get('mensaje', contacto_dict.get('mensaje', '')).strip()
    )
    contacto_repo.update(id, contacto)
    return {'status': 'success', 'message': 'Actualizado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 8. DELETE /api/contactos/<id> - DELETE
@app.route('/api/contactos/<int:id>', methods=['DELETE'])
def api_delete_contacto(id):
  """
  Eliminar contacto
  ---
  tags:
    - Contacto
  parameters:
    - in: path
      name: id
      type: integer
      required: true
  responses:
    200:
      description: Eliminado exitosamente
  """
  try:
    contacto_repo.delete_by_id(id)
    return {'status': 'success', 'message': 'Eliminado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# ============ RUTAS CRUD TABLA 3: CARACTERIZACION_PERSONAL ============

# 9. POST - INSERT
@app.route('/api/personal', methods=['POST'])
def api_create_personal():
  """
  Crear datos personales
  ---
  tags:
    - Personal
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          caracterizacion_id:
            type: integer
            example: 1
          tipo_documento:
            type: string
            example: "CC"
          identificacion:
            type: string
            example: "123456789"
          primer_nombre:
            type: string
            example: "Juan"
          primer_apellido:
            type: string
            example: "Perez"
          tipo_sanguineo:
            type: string
            example: "O+"
          fecha_expedicion:
            type: string
            format: date
            example: "2010-01-01"
          lugar_expedicion:
            type: string
            example: "Bogotá"
          segundo_nombre:
            type: string
            example: "Carlos"
          segundo_apellido:
            type: string
            example: "Gomez"
          libreta_militar:
            type: string
            example: "Si"
          distrito_militar:
            type: string
            example: "12"
          eps_afiliacion:
            type: string
            example: "Sura"
          otra_eps:
            type: string
            example: ""
          estado_civil:
            type: string
            example: "Soltero"
          pais_origen:
            type: string
            example: "Colombia"
          departamento_origen:
            type: string
            example: "Antioquia"
          ciudad_origen:
            type: string
            example: "Medellín"
          fecha_nacimiento:
            type: string
            format: date
            example: "1995-05-15"
  responses:
    201:
      description: Datos personales creados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Creado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    datos = request.get_json()
    char_id = datos.get('caracterizacion_id')
    personal_repo.create(char_id, datos)
    return {'status': 'success', 'message': 'Creado exitosamente'}, 201
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 10. GET - SELECT
@app.route('/api/personal/<int:id>', methods=['GET'])
def api_get_personal(id):
  """
  Obtener datos personales por ID
  ---
  tags:
    - Personal
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro de datos personales
  responses:
    200:
      description: Datos personales obtenidos exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          data:
            type: object
    404:
      description: Registro no encontrado
    500:
      description: Error en el servidor
  """
  try:
    resultado = personal_repo.get_by_id(id)
    if resultado:
      return {'status': 'success', 'data': resultado}, 200
    return {'status': 'error', 'message': 'No encontrado'}, 404
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 500


# 11. PUT - UPDATE
@app.route('/api/personal/<int:id>', methods=['PUT'])
def api_update_personal(id):
  """
  Actualizar datos personales
  ---
  tags:
    - Personal
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro a actualizar
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          tipo_documento:
            type: string
            example: "CC"
          identificacion:
            type: string
            example: "12345678"
          primer_nombre:
            type: string
            example: "Juan"
          primer_apellido:
            type: string
            example: "Perez"
          tipo_sanguineo:
            type: string
            example: "O+"
  responses:
    200:
      description: Datos personales actualizados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Actualizado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    datos = request.get_json()
    personal_repo.update(id, datos)
    return {'status': 'success', 'message': 'Actualizado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 12. DELETE - DELETE
@app.route('/api/personal/<int:id>', methods=['DELETE'])
def api_delete_personal(id):
  """
  Eliminar datos personales
  ---
  tags:
    - Personal
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro a eliminar
  responses:
    200:
      description: Datos personales eliminados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Eliminado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    personal_repo.delete(id)
    return {'status': 'success', 'message': 'Eliminado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# ============ RUTAS CRUD TABLA 4: CARACTERIZACION_UBICACION ============

# 13. POST - INSERT
@app.route('/api/ubicacion', methods=['POST'])
def api_create_ubicacion():
  """
  Crear datos de ubicación
  ---
  tags:
    - Ubicacion
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          caracterizacion_id:
            type: integer
            example: 1
          pais:
            type: string
            example: "Colombia"
          departamento:
            type: string
            example: "Antioquia"
          ciudad:
            type: string
            example: "Medellín"
          barrio:
            type: string
            example: "Poblado"
          direccion:
            type: string
            example: "Calle 10 # 43A-30"
          telefono_contacto:
            type: string
            example: "3101234567"
          telefono_celular:
            type: string
            example: "3101234567"
          correo_electronico:
            type: string
            example: "test@test.com"
          direccion_correspondencia:
            type: string
            example: "Calle 10 # 43A-30"
  responses:
    201:
      description: Datos de ubicación creados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Creado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    datos = request.get_json()
    char_id = datos.get('caracterizacion_id')
    ubicacion_repo.create(char_id, datos)
    return {'status': 'success', 'message': 'Creado exitosamente'}, 201
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 14. GET - SELECT
@app.route('/api/ubicacion/<int:id>', methods=['GET'])
def api_get_ubicacion(id):
  """
  Obtener datos de ubicación por ID
  ---
  tags:
    - Ubicacion
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro de ubicación
  responses:
    200:
      description: Datos de ubicación obtenidos exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          data:
            type: object
    404:
      description: Registro no encontrado
    500:
      description: Error en el servidor
  """
  try:
    resultado = ubicacion_repo.get_by_id(id)
    if resultado:
      return {'status': 'success', 'data': resultado}, 200
    return {'status': 'error', 'message': 'No encontrado'}, 404
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 500


# 15. PUT - UPDATE
@app.route('/api/ubicacion/<int:id>', methods=['PUT'])
def api_update_ubicacion(id):
  """
  Actualizar datos de ubicación
  ---
  tags:
    - Ubicacion
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro a actualizar
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          pais:
            type: string
            example: "Colombia"
          departamento:
            type: string
            example: "Antioquia"
          municipio:
            type: string
            example: "Medellín"
  responses:
    200:
      description: Datos de ubicación actualizados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Actualizado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    datos = request.get_json()
    ubicacion_repo.update(id, datos)
    return {'status': 'success', 'message': 'Actualizado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 16. DELETE - DELETE
@app.route('/api/ubicacion/<int:id>', methods=['DELETE'])
def api_delete_ubicacion(id):
  """
  Eliminar datos de ubicación
  ---
  tags:
    - Ubicacion
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro a eliminar
  responses:
    200:
      description: Datos de ubicación eliminados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Eliminado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    ubicacion_repo.delete(id)
    return {'status': 'success', 'message': 'Eliminado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# ============ RUTAS CRUD TABLA 5: CARACTERIZACION_SOCIOECONOMICA ============

# 17. POST - INSERT
@app.route('/api/socioeconomica', methods=['POST'])
def api_create_socioeconomica():
  """
  Crear datos socioeconómicos
  ---
  tags:
    - Socioeconomica
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          caracterizacion_id:
            type: integer
            example: 1
          sisben_sn:
            type: string
            example: "Si"
          grupo_sisben:
            type: string
            example: "A1"
          estrato:
            type: string
            example: "1"
          acceso:
            type: string
            example: "Computador con internet"
  responses:
    201:
      description: Datos socioeconómicos creados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Creado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    datos = request.get_json()
    char_id = datos.get('caracterizacion_id')
    socioeconomica_repo.create(char_id, datos)
    return {'status': 'success', 'message': 'Creado exitosamente'}, 201
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 18. GET - SELECT
@app.route('/api/socioeconomica/<int:id>', methods=['GET'])
def api_get_socioeconomica(id):
  """
  Obtener datos socioeconómicos por ID
  ---
  tags:
    - Socioeconomica
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro de datos socioeconómicos
  responses:
    200:
      description: Datos socioeconómicos obtenidos exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          data:
            type: object
    404:
      description: Registro no encontrado
    500:
      description: Error en el servidor
  """
  try:
    resultado = socioeconomica_repo.get_by_id(id)
    if resultado:
      return {'status': 'success', 'data': resultado}, 200
    return {'status': 'error', 'message': 'No encontrado'}, 404
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 500


# 19. PUT - UPDATE
@app.route('/api/socioeconomica/<int:id>', methods=['PUT'])
def api_update_socioeconomica(id):
  """
  Actualizar datos socioeconómicos
  ---
  tags:
    - Socioeconomica
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro a actualizar
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          ingresos:
            type: string
            example: "Menos de 1 SMLV"
          ocupacion:
            type: string
            example: "Empleado"
          vivienda:
            type: string
            example: "Casa propia"
  responses:
    200:
      description: Datos socioeconómicos actualizados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Actualizado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    datos = request.get_json()
    socioeconomica_repo.update(id, datos)
    return {'status': 'success', 'message': 'Actualizado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 20. DELETE - DELETE
@app.route('/api/socioeconomica/<int:id>', methods=['DELETE'])
def api_delete_socioeconomica(id):
  """
  Eliminar datos socioeconómicos
  ---
  tags:
    - Socioeconomica
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro a eliminar
  responses:
    200:
      description: Datos socioeconómicos eliminados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Eliminado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    socioeconomica_repo.delete(id)
    return {'status': 'success', 'message': 'Eliminado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# ============ RUTAS CRUD TABLA 6: CARACTERIZACION_DIVERSIDAD ============

# 21. POST - INSERT
@app.route('/api/diversidad', methods=['POST'])
def api_create_diversidad():
  """
  Crear datos de diversidad
  ---
  tags:
    - Diversidad
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          caracterizacion_id:
            type: integer
            example: 1
          pueblo_indigena:
            type: string
            example: "Ninguno"
          comunidad_negra:
            type: string
            example: "Ninguna"
          tiene_discapacidad:
            type: string
            example: "No"
          tipo_discapacidad:
            type: string
            example: ""
          capacidad_excepcional:
            type: string
            example: "No"
          desv_grupos_armados:
            type: string
            example: "No"
          vulnerabilidad_social:
            type: string
            example: "Ninguna"
          orientacion_sexual:
            type: string
            example: "Heterosexual"
          consume_psicoactiva:
            type: string
            example: "No"
  responses:
    201:
      description: Datos de diversidad creados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Creado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    datos = request.get_json()
    char_id = datos.get('caracterizacion_id')
    diversidad_repo.create(char_id, datos)
    return {'status': 'success', 'message': 'Creado exitosamente'}, 201
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 22. GET - SELECT
@app.route('/api/diversidad/<int:id>', methods=['GET'])
def api_get_diversidad(id):
  """
  Obtener datos de diversidad por ID
  ---
  tags:
    - Diversidad
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro de datos de diversidad
  responses:
    200:
      description: Datos de diversidad obtenidos exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          data:
            type: object
    404:
      description: Registro no encontrado
    500:
      description: Error en el servidor
  """
  try:
    resultado = diversidad_repo.get_by_id(id)
    if resultado:
      return {'status': 'success', 'data': resultado}, 200
    return {'status': 'error', 'message': 'No encontrado'}, 404
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 500


# 23. PUT - UPDATE
@app.route('/api/diversidad/<int:id>', methods=['PUT'])
def api_update_diversidad(id):
  """
  Actualizar datos de diversidad
  ---
  tags:
    - Diversidad
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro a actualizar
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          discapacidad:
            type: string
            example: "No"
          pertenencia_etnica:
            type: string
            example: "Mestizo"
          orientacion_sexual:
            type: string
            example: "Heterosexual"
  responses:
    200:
      description: Datos de diversidad actualizados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Actualizado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    datos = request.get_json()
    diversidad_repo.update(id, datos)
    return {'status': 'success', 'message': 'Actualizado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# 24. DELETE - DELETE
@app.route('/api/diversidad/<int:id>', methods=['DELETE'])
def api_delete_diversidad(id):
  """
  Eliminar datos de diversidad
  ---
  tags:
    - Diversidad
  parameters:
    - in: path
      name: id
      type: integer
      required: true
      description: ID del registro a eliminar
  responses:
    200:
      description: Datos de diversidad eliminados exitosamente
      schema:
        type: object
        properties:
          status:
            type: string
            example: "success"
          message:
            type: string
            example: "Eliminado exitosamente"
    400:
      description: Error en la solicitud
  """
  try:
    diversidad_repo.delete(id)
    return {'status': 'success', 'message': 'Eliminado exitosamente'}, 200
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# ============ RUTAS CRUD TABLA 7: CARACTERIZACION_ACADEMICA ============

# 25. POST - INSERT
@app.route('/api/academica', methods=['POST'])
def api_create_academica():
  """
  Crear datos académicos
  ---
  tags:
    - CaracterizacionAcademica
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          caracterizacion_id:
            type: integer
            example: 1
          motivo_principal:
            type: string
            example: "Superación personal"
          motivo_otro:
            type: string
            example: ""
          promedio:
            type: number
            format: float
            example: 4.5
          nivel_manejo:
            type: string
            example: "Alto"
  responses:
    201:
      description: Datos académicos creados exitosamente
  """
  try:
    datos = request.get_json()
    char_id = datos.get('caracterizacion_id')
    # Aquí deberías tener un academica_repo.create(char_id, datos)
    return {'status': 'success', 'message': 'Creado exitosamente'}, 201
  except Exception as e:
    return {'status': 'error', 'message': str(e)}, 400


# ============ OPERACIONES DE ADMINISTRACIÓN ============

@app.route('/vaciar_caracterizacion', methods=['POST'])
def vaciar_caracterizacion():
  """Elimina todos los registros de caracterización"""
  try:
    caracterizacion_repo.delete_all()
  except Exception as e:
    print(f"Error al vaciar caracterizacion: {e}")
  
  return redirect(url_for('resultados_caracterizacion'))


@app.route('/vaciar_contactos', methods=['POST'])
def vaciar_contactos():
  """Elimina todos los mensajes de contacto"""
  try:
    contacto_repo.delete_all()
  except Exception as e:
    print(f"Error al vaciar contactos: {e}")
  
  return redirect(url_for('contactos_listado'))


# ============ INICIO DE LA APLICACIÓN ============

# Importar funciones de compatibilidad (si es necesario)
from contacto import ensure_contact_table_exists

if __name__ == '__main__':
  AppInitializer.initialize()
  ensure_contact_table_exists()
  app.run(debug=True)

#este es mi app.py