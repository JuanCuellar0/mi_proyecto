"""
EJEMPLOS DE USO - Sistema Refactorizado con POO
"""

# ============================================================
# 1. EJEMPLOS DE CONFIGURACIÓN Y INICIALIZACIÓN
# ============================================================

from database import Database, DatabaseConfig
from models import Caracterizacion, Contacto, CaracterizacionPersonal, CaracterizacionAcademica
from services import CaracterizacionRepository, ContactoRepository, RiskAnalysisRepository


# Ejemplo 1: Crear configuración y base de datos
def ejemplo_configuracion():
    """Cómo configurar la base de datos"""
    
    # Crear configuración
    db_config = DatabaseConfig(
        host="127.0.0.1",
        user="root",
        password="",
        database="mi_proyecto",
        charset="utf8mb4"
    )
    
    # Crear instancia de BD
    db = Database(db_config)
    
    # Crear base de datos si no existe
    db.create_database_if_not_exists()
    
    print("✓ Base de datos configurada")
    return db, db_config


# ============================================================
# 2. EJEMPLOS DE REPOSITORIOS
# ============================================================

def ejemplo_repositorio_caracterizacion(db):
    """Cómo usar el repositorio de caracterización"""
    
    # Crear repositorio
    repo = CaracterizacionRepository(db)
    
    # Inicializar tabla
    repo.initialize_table()
    print("✓ Tabla inicializada")
    
    # Crear un nuevo registro
    nueva_caracterizacion = Caracterizacion(
        genero="Masculino",
        edad=22,
        residencia="Urbana",
        trabaja="No",
        personal=CaracterizacionPersonal(
            primer_nombre="Juan",
            primer_apellido="Pérez",
            identificacion="1234567"
        )
    )
    
    id_insertado = repo.create(nueva_caracterizacion)
    print(f"✓ Registro creado con ID: {id_insertado}")
    
    # Obtener todos
    todos = repo.get_all()
    print(f"✓ Total de registros: {len(todos)}")
    
    # Obtener por ID
    registro = repo.get_by_id(id_insertado)
    if registro:
        print(f"✓ Registro encontrado: {registro['primer_nombre']}")
    
    # Eliminar por ID
    eliminados = repo.delete_by_id(id_insertado)
    print(f"✓ Registros eliminados: {eliminados}")


def ejemplo_repositorio_contacto(db):
    """Cómo usar el repositorio de contacto"""
    
    # Crear repositorio
    repo = ContactoRepository(db)
    
    # Inicializar tabla
    repo.initialize_table()
    
    # Crear mensaje
    mensaje = Contacto(
        nombre="María García",
        correo="maria@email.com",
        mensaje="Tengo una pregunta sobre la admisión"
    )
    
    id_mensaje = repo.create(mensaje)
    print(f"✓ Mensaje creado con ID: {id_mensaje}")
    
    # Obtener todos los mensajes
    mensajes = repo.get_all()
    print(f"✓ Total de mensajes: {len(mensajes)}")
    
    # Obtener por ID
    msg = repo.get_by_id(id_mensaje)
    if msg:
        print(f"✓ Mensaje de: {msg['nombre']}")


# ============================================================
# 3. EJEMPLOS DE ANÁLISIS DE RIESGO
# ============================================================

def ejemplo_analisis_riesgo(db):
    """Cómo usar el análisis de riesgo"""
    
    # Crear repositorio de caracterización
    caract_repo = CaracterizacionRepository(db)
    
    # Crear repositorio de análisis
    risk_repo = RiskAnalysisRepository(caract_repo)
    
    # Analizar todos los registros
    resultados = risk_repo.analyze_all()
    
    print(f"✓ Registros analizados: {len(resultados)}")
    
    # Ver resultados
    for resultado in resultados[:5]:  # Primeros 5
        print(f"\n  Nombre: {resultado['nombre']}")
        print(f"  Score: {resultado['score']}")
        print(f"  Nivel: {resultado['nivel']}")
        print(f"  Razones: {resultado['razones']}")


# ============================================================
# 4. EJEMPLOS DE MODELOS
# ============================================================

def ejemplo_modelos():
    """Cómo usar los modelos de datos"""
    
    # Ejemplo 1: Crear caracterización manual
    caracterizacion = Caracterizacion(
        genero="Femenino",
        edad=20,
        residencia="Rural",
        trabaja="Sí"
    )
    
    # Acceder a sub-modelos
    caracterizacion.personal.primer_nombre = "Ana"
    caracterizacion.personal.primer_apellido = "López"
    caracterizacion.personal.identificacion = "9876543"
    
    caracterizacion.ubicacion.ciudad = "Bogotá"
    caracterizacion.ubicacion.departamento = "Cundinamarca"
    
    caracterizacion.socioeconoma.estrato = 2
    caracterizacion.socioeconoma.sisben_sn = "Sí"
    
    caracterizacion.academica.promedio = 3.8
    caracterizacion.academica.motivo_principal = "Mejorar profesionalmente"
    
    # Obtener nombre completo
    nombre = caracterizacion.personal.get_nombre_completo()
    print(f"✓ Nombre completo: {nombre}")
    
    # Convertir a diccionario
    datos_dict = caracterizacion.to_dict_flat()
    print(f"✓ Campos disponibles: {len(datos_dict)}")


def ejemplo_modelos_desde_formulario():
    """Cómo crear modelos desde datos de formulario"""
    
    # Simular datos de formulario
    form_data = {
        'genero': 'Masculino',
        'edad': '25',
        'residencia': 'Urbana',
        'trabaja': 'No',
        'primer_nombre': 'Carlos',
        'primer_apellido': 'Rodríguez',
        'identificacion': '5555555',
        'ciudad': 'Medellín',
        'departamento': 'Antioquia',
        'estrato': '3',
        'sisben_sn': 'No',
        'consume_psicoactiva': 'No',
        'tiene_discapacidad': 'No',
        'promedio': '3.5',
        'acceso': 'Computador e internet',
        'getlist': lambda x: []  # Simulación de getlist
    }
    
    # Crear desde datos
    caracterizacion = Caracterizacion.from_form_data(form_data)
    print(f"✓ Caracterización creada desde formulario")
    print(f"  Nombre: {caracterizacion.personal.get_nombre_completo()}")
    print(f"  Ciudad: {caracterizacion.ubicacion.ciudad}")
    print(f"  Estrato: {caracterizacion.socioeconoma.estrato}")


# ============================================================
# 5. EJEMPLOS DE OPERACIONES CON BD
# ============================================================

def ejemplo_operaciones_bd(db):
    """Cómo ejecutar operaciones directas con BD"""
    
    # Ejecutar query sin retornar resultados
    query = """
        INSERT INTO caracterizacion (primer_nombre, primer_apellido) 
        VALUES (%s, %s)
    """
    db.execute_query(query, ("Pedro", "González"))
    print("✓ Query ejecutado")
    
    # Obtener un registro
    query = "SELECT * FROM caracterizacion LIMIT 1"
    registro = db.fetch_one(query, dict_cursor=True)
    if registro:
        print(f"✓ Registro encontrado: {registro}")
    
    # Obtener múltiples registros
    query = "SELECT * FROM caracterizacion LIMIT 5"
    registros = db.fetch_all(query, dict_cursor=True)
    print(f"✓ Registros encontrados: {len(registros)}")
    
    # Insertar y obtener ID
    query = """
        INSERT INTO características 
        (primer_nombre, primer_apellido) 
        VALUES (%s, %s)
    """
    nuevo_id = db.insert(query, ("Laura", "Martínez"))
    print(f"✓ Registro insertado con ID: {nuevo_id}")
    
    # Eliminar registros
    query = "DELETE FROM caracterizacion WHERE edad < 18"
    eliminados = db.delete(query)
    print(f"✓ Registros eliminados: {eliminados}")


# ============================================================
# 6. EJEMPLOS PRÁCTICOS COMPLETOS
# ============================================================

def ejemplo_completo_insercion_y_analisis():
    """Ejemplo completo: insertar datos y analizarlos"""
    
    # 1. Configurar
    db_config = DatabaseConfig()
    db = Database(db_config)
    db.create_database_if_not_exists()
    
    # 2. Crear repositorios
    caract_repo = CaracterizacionRepository(db)
    caract_repo.initialize_table()
    
    # 3. Crear múltiples caracterizaciones
    datos_test = [
        {
            'primer_nombre': 'Juan',
            'primer_apellido': 'Pérez',
            'estrato': '2',
            'sisben_sn': 'Sí',
            'consume_psicoactiva': 'No',
        },
        {
            'primer_nombre': 'María',
            'primer_apellido': 'García',
            'estrato': '1',
            'sisben_sn': 'No',
            'consume_psicoactiva': 'Sí',  # Alto riesgo
        },
        {
            'primer_nombre': 'Carlos',
            'primer_apellido': 'López',
            'estrato': '4',
            'sisben_sn': 'No',
            'consume_psicoactiva': 'No',
        }
    ]
    
    for datos in datos_test:
        caract = Caracterizacion.from_form_data(datos)
        caract_repo.create(caract)
    
    print("✓ 3 registros insertados")
    
    # 4. Analizar riesgo
    risk_repo = RiskAnalysisRepository(caract_repo)
    resultados = risk_repo.analyze_all()
    
    print("\n📊 ANÁLISIS DE RIESGO:")
    for r in resultados:
        print(f"  {r['nombre']} - {r['nivel']} ({r['score']} pts)")


# ============================================================
# 7. CÓMO CREAR NUEVAS FUNCIONALIDADES
# ============================================================

class MiNuevoRepositorio:
    """Ejemplo de cómo crear un nuevo repositorio"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def crear_tabla_personalizada(self):
        """Crear tabla personalizada"""
        query = """
            CREATE TABLE IF NOT EXISTS mi_tabla (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100),
                valor INT
            )
        """
        self.db.execute_query(query)
    
    def insertar(self, nombre: str, valor: int) -> int:
        """Insertar datos"""
        query = "INSERT INTO mi_tabla (nombre, valor) VALUES (%s, %s)"
        return self.db.insert(query, (nombre, valor))
    
    def obtener_todos(self):
        """Obtener todos los registros"""
        query = "SELECT * FROM mi_tabla"
        return self.db.fetch_all(query, dict_cursor=True)
    
    def obtener_por_nombre(self, nombre: str):
        """Obtener por nombre"""
        query = "SELECT * FROM mi_tabla WHERE nombre = %s"
        return self.db.fetch_all(query, (nombre,), dict_cursor=True)


def ejemplo_nuevo_repositorio():
    """Cómo usar el nuevo repositorio"""
    
    db_config = DatabaseConfig()
    db = Database(db_config)
    
    # Crear repositorio personalizado
    mi_repo = MiNuevoRepositorio(db)
    mi_repo.crear_tabla_personalizada()
    
    # Insertar datos
    id1 = mi_repo.insertar("Python", 10)
    id2 = mi_repo.insertar("Java", 8)
    
    print(f"✓ Datos insertados: {id1}, {id2}")
    
    # Obtener todos
    todos = mi_repo.obtener_todos()
    print(f"✓ Total registros: {len(todos)}")
    
    # Buscar por nombre
    resultado = mi_repo.obtener_por_nombre("Python")
    print(f"✓ Registros encontrados: {len(resultado)}")


# ============================================================
# MAIN - Ejecutar ejemplos
# ============================================================

if __name__ == "__main__":
    print("🚀 EJEMPLOS DE USO DEL SISTEMA CON POO\n")
    
    # Descomentar los ejemplos que quieras ejecutar:
    
    # Ejemplo 1: Configuración
    print("1️⃣  Configuración:")
    db, config = ejemplo_configuracion()
    print()
    
    # Ejemplo 2: Modelos
    print("2️⃣  Modelos:")
    ejemplo_modelos()
    print()
    
    # Ejemplo 3: Repositorios
    # print("3️⃣  Repositorio de Caracterización:")
    # ejemplo_repositorio_caracterizacion(db)
    # print()
    
    # Ejemplo 4: Completo
    # print("4️⃣  Ejemplo Completo:")
    # ejemplo_completo_insercion_y_analisis()
    # print()
    
    # Ejemplo 5: Nuevo repositorio
    # print("5️⃣  Nuevo Repositorio:")
    # ejemplo_nuevo_repositorio()
    # print()
    
    print("\n✅ Ejemplos completados")
