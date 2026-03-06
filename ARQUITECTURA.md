# Diagrama de Arquitectura - POO

```
┌─────────────────────────────────────────────────────────────────┐
│                      APLICACIÓN FLASK (app.py)                  │
│  ┌──────────────────  Rutas HTTP ───────────────────┐          │
│  │  GET  /                  GET  /encuesta             │          │
│  │  POST /enviar_caracterizacion                       │          │
│  │  POST /enviar_contacto                              │          │
│  │  GET  /resultados_caracterizacion                   │          │
│  │  GET  /analisis_riesgo                              │          │
│  │  POST /vaciar_caracterizacion                       │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓↓↓
┌─────────────────────────────────────────────────────────────────┐
│              SERVICIOS Y REPOSITORIOS (services.py)             │
│                                                                  │
│  ┌──────────────────────────────────────┐                      │
│  │  CaracterizacionRepository           │                      │
│  │  ─────────────────────────────        │                      │
│  │  - create(caracterizacion)           │                      │
│  │  - get_all()                         │                      │
│  │  - get_by_id(id)                     │                      │
│  │  - delete_all()                      │                      │
│  │  - initialize_table()                │                      │
│  └──────────────────────────────────────┘                      │
│                                                                  │
│  ┌──────────────────────────────────────┐                      │
│  │  ContactoRepository                  │                      │
│  │  ─────────────────────────────        │                      │
│  │  - create(contacto)                  │                      │
│  │  - get_all()                         │                      │
│  │  - delete_all()                      │                      │
│  │  - initialize_table()                │                      │
│  └──────────────────────────────────────┘                      │
│                                                                  │
│  ┌──────────────────────────────────────┐                      │
│  │  RiskAnalysisRepository              │                      │
│  │  ─────────────────────────────        │                      │
│  │  - analyze_all()                     │                      │
│  └──────────────────────────────────────┘                      │
│                                                                  │
│  ┌──────────────────────────────────────┐                      │
│  │  RiskAnalysisService                 │                      │
│  │  ─────────────────────────────        │                      │
│  │  + score_row(row) → (score, level)  │                      │
│  │  + to_float(value)                   │                      │
│  │  + to_int(value)                     │                      │
│  └──────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓↓↓
┌─────────────────────────────────────────────────────────────────┐
│                    MODELOS DE DATOS (models.py)                 │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │               Caracterizacion                      │         │
│  │  ────────────────────────────────                  │         │
│  │  - id: int                                         │         │
│  │  - fecha: datetime                                 │         │
│  │  - genero: str                                     │         │
│  │  - edad: int                                       │         │
│  │  - trabajaja: str                                  │         │
│  │                                                    │         │
│  │  - personal: CaracterizacionPersonal               │         │
│  │  - ubicacion: CaracterizacionUbicacion             │         │
│  │  - socioeconoma: CaracterizacionSocioeconoma       │         │
│  │  - diversidad: CaracterizacionDiversidad           │         │
│  │  - academica: CaracterizacionAcademica             │         │
│  │                                                    │         │
│  │  + from_form_data(form_data)                       │         │
│  │  + to_dict_flat()                                  │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │       CaracterizacionPersonal (Dataclass)          │         │
│  │  ────────────────────────────────                  │         │
│  │  - tipo_documento, identificacion, ...             │         │
│  │  - primer_nombre, segundo_nombre, ...             │         │
│  │  + get_nombre_completo() → str                    │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ┌────────────────────────────────────────┐                    │
│  │  CaracterizacionUbicacion (Dataclass)  │                    │
│  │  ────────────────────────────────      │                    │
│  │  - pais, departamento, ciudad, ...     │                    │
│  │  - correo_electronico, telefono, ...   │                    │
│  └────────────────────────────────────────┘                    │
│                                                                  │
│  ┌────────────────────────────────────────┐                    │
│  │  CaracterizacionSocioeconoma           │                    │
│  │  ────────────────────────────────      │                    │
│  │  - sisben_sn, grupo_sisben             │                    │
│  │  - estrato, acceso                     │                    │
│  └────────────────────────────────────────┘                    │
│                                                                  │
│  ┌────────────────────────────────────────┐                    │
│  │  CaracterizacionDiversidad             │                    │
│  │  ────────────────────────────────      │                    │
│  │  - pueblo_indigena, comunidad_negra    │                    │
│  │  - tiene_discapacidad, ...             │                    │
│  │  - consume_psicoactiva                 │                    │
│  └────────────────────────────────────────┘                    │
│                                                                  │
│  ┌────────────────────────────────────────┐                    │
│  │  Contacto (Dataclass)                  │                    │
│  │  ────────────────────────────────      │                    │
│  │  - id: int                             │                    │
│  │  - nombre, correo, mensaje: str        │                    │
│  └────────────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓↓↓
┌─────────────────────────────────────────────────────────────────┐
│                  GESTIÓN BD (database.py)                       │
│                                                                  │
│  ┌──────────────────────────────────────┐                      │
│  │  DatabaseConfig                      │                      │
│  │  ──────────────────────────────       │                      │
│  │  - host, user, password, database     │                      │
│  │  + get_config()                       │                      │
│  │  + get_server_config()                │                      │
│  └──────────────────────────────────────┘                      │
│                                                                  │
│  ┌──────────────────────────────────────┐                      │
│  │  Database                            │                      │
│  │  ──────────────────────────────       │                      │
│  │  - config: DatabaseConfig             │                      │
│  │  + connect()                          │                      │
│  │  + execute_query(query, params)       │                      │
│  │  + fetch_one(query, params)           │                      │
│  │  + fetch_all(query, params)           │                      │
│  │  + insert(query, params)              │                      │
│  │  + delete(query, params)              │                      │
│  └──────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓↓↓
┌─────────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS MySQL                          │
│                                                                  │
│  ┌────────────────────────────────────────┐                    │
│  │  Tabla: caracterizacion                │                    │
│  │  - id, fecha, tipo_documento, ...      │                    │
│  │  - primer_nombre, primer_apellido, ... │                    │
│  │  - sisben_sn, estrato, acceso, ...     │                    │
│  │  - consume_psicoactiva, etc.           │                    │
│  └────────────────────────────────────────┘                    │
│                                                                  │
│  ┌────────────────────────────────────────┐                    │
│  │  Tabla: contacto_mensajes              │                    │
│  │  - id, fecha, nombre, correo, mensaje  │                    │
│  └────────────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Datos

### 1. Envío de Encuesta
```
Usuario llena formulario
        ↓
app.py: enviar_caracterizacion() recibe POST
        ↓
Caracterizacion.from_form_data(request.form)
        ↓
CaracterizacionRepository.create()
        ↓
Database.insert()
        ↓
MySQL: caracterizacion table
```

### 2. Análisis de Riesgo
```
Usuario accede /analisis_riesgo
        ↓
app.py: analisis_riesgo() GET
        ↓
RiskAnalysisRepository.analyze_all()
        ↓
Itera cada registro
  - RiskAnalysisService.score_row()
  - Calcula score y nivel
        ↓
Retorna lista de resultados
        ↓
Render template con resultados
```

### 3. Exportación de Reportes
```
python analisis_riesgo.py
        ↓
RiskAnalysisExporter.analyze_all()
        ↓
RiskAnalysisExporter.export_to_csv()
        ↓
Genera: reportes/riesgo_desercion.csv
```

## Relaciones entre Clases

```
Database
    ↑
    ├─── DatabaseConfig (Composición)
    └─── Usada por: CaracterizacionRepository, ContactoRepository

CaracterizacionRepository        ContactoRepository
    ├─ Maneja: Caracterizacion      ├─ Maneja: Contacto
    └─ Usa: Database                 └─ Usa: Database
    
RiskAnalysisRepository
    ├─ Usa: CaracterizacionRepository
    └─ Usa: RiskAnalysisService 

Caracterizacion
    ├─ Contiene: CaracterizacionPersonal
    ├─ Contiene: CaracterizacionUbicacion
    ├─ Contiene: CaracterizacionSocioeconoma
    ├─ Contiene: CaracterizacionDiversidad
    └─ Contiene: CaracterizacionAcademica
```

## Principios SOLID Aplicados

✅ **S (Single Responsibility)**
- Cada clase tiene una única responsabilidad
- Database: conexiones
- Repository: CRUD operations
- Service: lógica de negocio

✅ **O (Open/Closed)**
- Abierto para extensión (nuevos repositorios)
- Cerrado para modificación (no cambiar clases existentes)

✅ **L (Liskov Substitution)**
- Los repositorios pueden intercambiarse

✅ **I (Interface Segregation)**
- Métodos específicos en cada clase

✅ **D (Dependency Inversion)**
- Las clases dependem de abstracciones (Database)
- No de implementaciones
