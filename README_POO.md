# Documentación - Refactorización con POO

## Descripción General

Tu proyecto ha sido reorganizado siguiendo principios de **Programación Orientada a Objetos (POO)**. La estructura ahora es más modular, mantenible y escalable.
 
## Estructura de Archivos

```
Mi Proyecto/
├── app.py                    # Aplicación Flask refactorizada
├── database.py              # Gestión de conexiones BD
├── models.py                # Modelos de datos
├── services.py              # Servicios y repositorios
├── contacto.py              # Blueprint de contacto
├── analisis_riesgo.py       # Análisis de riesgos
├── templates/               # Plantillas HTML
├── static/                  # Archivos estáticos
└── reportes/                # Reportes generados
```

## Componentes Principales

### 1. **database.py** - Gestión de Base de Datos
Clases para gestionar conexiones y operaciones:

```python
# Configuración
db_config = DatabaseConfig(
    host="127.0.0.1",
    user="root",
    password="",
    database="mi_proyecto",
    charset="utf8mb4"
)

# Instancia de BD
db = Database(db_config)

# Operaciones
db.fetch_all(query, dict_cursor=True)  # Obtener múltiples registros
db.fetch_one(query)                    # Obtener un registro
db.insert(query, params)               # Insertar
db.delete(query, params)               # Eliminar
```

**Ventajas:**
- Centraliza toda la lógica de conexión
- Evita duplicación de código
- Facilita cambios en BD en el futuro

### 2. **models.py** - Modelos de Datos
Modelos dataclass para estructurar datos:

```python
# Ejemplo: Crear desde datos de formulario
caracterizacion = Caracterizacion.from_form_data(request.form)

# Acceder a datos específicos
nombre_completo = caracterizacion.personal.get_nombre_completo()
estrato = caracterizacion.socioeconoma.estrato

# Convertir a diccionario para BD
data_dict = caracterizacion.to_dict_flat()
```

**Submodelos disponibles:**
- `CaracterizacionPersonal` - Datos personales
- `CaracterizacionUbicacion` - Ubicación
- `CaracterizacionSocioeconoma` - Info socioeconómica
- `CaracterizacionDiversidad` - Diversidad e inclusión
- `CaracterizacionAcademica` - Datos académicos
- `Contacto` - Mensajes de contacto

### 3. **services.py** - Servicios y Repositorios
Lógica de negocio y acceso a datos:

```python
# Instanciar repositorios
db = Database(db_config)
caracterizacion_repo = CaracterizacionRepository(db)
contacto_repo = ContactoRepository(db)
risk_analysis_repo = RiskAnalysisRepository(caracterizacion_repo)

# Usar repositorios
caracterizacion_repo.create(caracterizacion)      # Crear
caracterizacion_repo.get_all()                    # Obtener todos
caracterizacion_repo.get_by_id(id)                # Obtener por ID
caracterizacion_repo.delete_all()                 # Eliminar todos
```

**Clases principales:**

- **CaracterizacionRepository** - CRUD de caracterizaciones
- **ContactoRepository** - CRUD de contactos
- **RiskAnalysisService** - Lógica de análisis de riesgo
- **RiskAnalysisRepository** - Análisis de todos los registros

### 4. **app.py** - Aplicación Flask Refactorizada
Código más limpio y organizado:

```python
# Inicialización centralizada
app = Flask(__name__)
db_config = DatabaseConfig(...)
db = Database(db_config)
caracterizacion_repo = CaracterizacionRepository(db)
contacto_repo = ContactoRepository(db)
risk_analysis_repo = RiskAnalysisRepository(caracterizacion_repo)

# Rutas simplificadas
@app.route('/enviar_caracterizacion', methods=['POST'])
def enviar_caracterizacion():
    caracterizacion = Caracterizacion.from_form_data(request.form)
    caracterizacion_repo.create(caracterizacion)
    return redirect(url_for('gracias_enc'))
```

**Rutas disponibles:**

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Página de inicio |
| `/encuesta` | GET | Formulario de encuesta |
| `/enviar_caracterizacion` | POST | Procesar encuesta |
| `/enviar_contacto` | POST | Enviar mensaje contacto |
| `/resultados_caracterizacion` | GET | Ver resultados |
| `/contactos_listado` | GET | Ver mensajes contacto |
| `/analisis_riesgo` | GET | Análisis de riesgo |
| `/vaciar_caracterizacion` | POST | Limpiar datos |
| `/vaciar_contactos` | POST | Limpiar contactos |

### 5. **contacto.py** - Blueprint de Contacto
Módulo separado para rutas de contacto:

```python
# Ya no necesita conexiones directas a BD
# Usa las clases de services.py
```

### 6. **analisis_riesgo.py** - Análisis de Riesgo
Exportar resultados de análisis:

```python
# Para usar desde terminal
python analisis_riesgo.py

# Genera:
# - Resumen en consola
# - Archivo CSV: reportes/riesgo_desercion.csv
```

## Mejoras Implementadas

### ✅ **Separación de Responsabilidades**
- Cada clase tiene una única responsabilidad
- Facilita testing y mantenimiento

### ✅ **Reutilización de Código**
- Las funciones se comparten mediante clases
- Evita duplicación

### ✅ **Mantenibilidad**
- Código más organizado y legible
- Fácil agregar nuevas funcionalidades

### ✅ **Escalabilidad**
- Fácil agregar nuevos repositorios
- Fácil cambiar BD en el futuro

### ✅ **Type Hints**
- Mejor autocompletado en IDEs
- Código autodocumentado

## Cómo Usar

### Iniciar la aplicación:
```bash
python app.py
```

### Analizar riesgos (desde terminal):
```bash
python analisis_riesgo.py
```

### Crear nuevas funcionalidades:

**Ejemplo: Agregar nuevo repositorio**
```python
# En services.py
class MiNuevoRepositorio:
    def __init__(self, db: Database):
        self.db = db
    
    def create(self, datos):
        # Lógica de inserción
        pass

# En app.py
mi_repo = MiNuevoRepositorio(db)

@app.route('/ruta', methods=['POST'])
def mi_ruta():
    mi_repo.create(datos)
    return ...
```

## Configuración de Base de Datos

Cambiar credenciales en **app.py**:
```python
db_config = DatabaseConfig(
    host="127.0.0.1",      # Host
    user="root",           # Usuario
    password="",           # Contraseña
    database="mi_proyecto", # BD
    charset="utf8mb4"      # Charset
)
```

## Mejoras Futuras Sugeridas

1. **Testing Unitario** - Agregar tests con pytest
2. **Validación** - Crear clases de validadores
3. **Logging** - Registrar operaciones
4. **Caché** - Cachear resultados frecuentes
5. **Autenticación** - Agregar login/permisos
6. **API REST** - Exponer como API
7. **Documentación API** - Swagger/OpenAPI

## Contacto / Soporte

Si tienes dudas sobre cómo usar las nuevas clases, revisa los docstrings en cada módulo.
