# 📚 Documentación Completa - 24 Rutas CRUD

## 🎯 Cómo Funciona el API

Tu aplicación Flask ahora tiene **24 rutas CRUD organizadas en 6 tablas**:

### Estructura General:
```
POST   /api/{tabla}              → CREATE (Insertar)
GET    /api/{tabla}/<id>         → READ   (Obtener)
PUT    /api/{tabla}/<id>         → UPDATE (Actualizar)
DELETE /api/{tabla}/<id>         → DELETE (Eliminar)
```

---

## 📋 Las 6 Tablas y sus 24 Rutas

### **TABLA 1: CARACTERIZACION** (Rutas 1-4)
Base de caracterización con info general

| # | Método | Ruta | Función | Status |
|---|--------|------|---------|--------|
| 1 | **POST** | `/api/caracterizaciones` | Crear nueva caracterización | 201 |
| 2 | **GET** | `/api/caracterizaciones/<id>` | Obtener por ID | 200 |
| 3 | **PUT** | `/api/caracterizaciones/<id>` | Actualizar | 200 |
| 4 | **DELETE** | `/api/caracterizaciones/<id>` | Eliminar | 200 |

**Campos principales:**
```json
{
  "genero": "M|F",
  "edad": 20,
  "trabaja": "Si|No",
  "residencia": "Casa|Apto"
}
```

---

### **TABLA 2: CONTACTO** (Rutas 5-8)
Mensajes de contacto de usuarios

| # | Método | Ruta | Función | Status |
|---|--------|------|---------|--------|
| 5 | **POST** | `/api/contactos` | Crear contacto | 201 |
| 6 | **GET** | `/api/contactos/<id>` | Obtener por ID | 200 |
| 7 | **PUT** | `/api/contactos/<id>` | Actualizar | 200 |
| 8 | **DELETE** | `/api/contactos/<id>` | Eliminar | 200 |

**Campos:**
```json
{
  "nombre": "Juan Perez",
  "correo": "juan@example.com",
  "mensaje": "Tengo una pregunta..."
}
```

---

### **TABLA 3: PERSONAL** (Rutas 9-12)
Datos personales detallados del aspirante

| # | Método | Ruta | Función | Status |
|---|--------|------|---------|--------|
| 9 | **POST** | `/api/personal` | Crear datos personales | 201 |
| 10 | **GET** | `/api/personal/<id>` | Obtener por ID | 200 |
| 11 | **PUT** | `/api/personal/<id>` | Actualizar | 200 |
| 12 | **DELETE** | `/api/personal/<id>` | Eliminar | 200 |

**Campos:**
```json
{
  "caracterizacion_id": 1,
  "tipo_documento": "CC|CE|PP",
  "identificacion": "123456789",
  "primer_nombre": "Juan",
  "primer_apellido": "Perez",
  "tipo_sanguineo": "O+",
  "eps_afiliacion": "Salud Total"
}
```

---

### **TABLA 4: UBICACION** (Rutas 13-16)
Información de ubicación y contacto

| # | Método | Ruta | Función | Status |
|---|--------|------|---------|--------|
| 13 | **POST** | `/api/ubicacion` | Crear ubicación | 201 |
| 14 | **GET** | `/api/ubicacion/<id>` | Obtener por ID | 200 |
| 15 | **PUT** | `/api/ubicacion/<id>` | Actualizar | 200 |
| 16 | **DELETE** | `/api/ubicacion/<id>` | Eliminar | 200 |

**Campos:**
```json
{
  "caracterizacion_id": 1,
  "pais": "Colombia",
  "departamento": "Cundinamarca",
  "ciudad": "Bogota",
  "direccion": "Cra 5 # 10-20",
  "telefono_celular": "3001234567",
  "correo_electronico": "juan@example.com"
}
```

---

### **TABLA 5: SOCIOECONOMICA** (Rutas 17-20)
Información socioeconómica del aspirante

| # | Método | Ruta | Función | Status |
|---|--------|------|---------|--------|
| 17 | **POST** | `/api/socioeconomica` | Crear datos socioeco | 201 |
| 18 | **GET** | `/api/socioeconomica/<id>` | Obtener por ID | 200 |
| 19 | **PUT** | `/api/socioeconomica/<id>` | Actualizar | 200 |
| 20 | **DELETE** | `/api/socioeconomica/<id>` | Eliminar | 200 |

**Campos:**
```json
{
  "caracterizacion_id": 1,
  "estrato": 2,
  "sisben_sn": "Si|No",
  "grupo_sisben": "A|B|C|D",
  "acceso": "Internet|Celular|Compartido"
}
```

---

### **TABLA 6: DIVERSIDAD** (Rutas 21-24)
Información de diversidad e inclusión

| # | Método | Ruta | Función | Status |
|---|--------|------|---------|--------|
| 21 | **POST** | `/api/diversidad` | Crear datos diversidad | 201 |
| 22 | **GET** | `/api/diversidad/<id>` | Obtener por ID | 200 |
| 23 | **PUT** | `/api/diversidad/<id>` | Actualizar | 200 |
| 24 | **DELETE** | `/api/diversidad/<id>` | Eliminar | 200 |

**Campos:**
```json
{
  "caracterizacion_id": 1,
  "tiene_discapacidad": "Si|No",
  "tipo_discapacidad": "Motora|Sensorial|Cognitiva",
  "consume_psicoactiva": "Si|No",
  "vulnerabilidad_social": "Desplazado|Víctima|Otra",
  "orientacion_sexual": "Heterosexual|LGBTIQ+"
}
```

---

## 🔧 Cómo Usar las Rutas

### **1. Crear un Registro (POST)**
```powershell
$body = @{
  genero = "M"
  edad = 20
  trabaja = "Si"
  residencia = "Apto"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/caracterizaciones" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```
**Respuesta (201):**
```json
{
  "status": "success",
  "message": "Creado exitosamente",
  "id": 1
}
```

---

### **2. Obtener un Registro (GET)**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/caracterizaciones/1" `
  -Method GET
```
**Respuesta (200):**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "genero": "M",
    "edad": 20,
    "trabaja": "Si",
    "residencia": "Apto",
    "fecha": "2026-03-05 10:30:00"
  }
}
```

---

### **3. Actualizar un Registro (PUT)**
```powershell
$body = @{
  edad = 21
  residencia = "Casa"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/caracterizaciones/1" `
  -Method PUT `
  -Body $body `
  -ContentType "application/json"
```
**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Actualizado exitosamente"
}
```

---

### **4. Eliminar un Registro (DELETE)**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/caracterizaciones/1" `
  -Method DELETE
```
**Respuesta (200):**
```json
{
  "status": "success",
  "message": "Eliminado exitosamente"
}
```

---

## 🔗 Relaciones Entre Tablas

```
caracterizacion (ID: 1)
    ├── personal (caracterizacion_id: 1)
    ├── ubicacion (caracterizacion_id: 1)
    ├── socioeconomica (caracterizacion_id: 1)
    └── diversidad (caracterizacion_id: 1)

contacto (ID: 1) - Tabla independiente
```

**Importante:** Cuando crees datos en `personal`, `ubicacion`, `socioeconomica` o `diversidad`, el `caracterizacion_id` debe existir en la tabla `caracterizacion`.

---

## 📊 Códigos de Respuesta HTTP

| Código | Significado | Caso |
|--------|-------------|------|
| **201** | Created (Creado) | POST exitoso |
| **200** | OK (Correcto) | GET, PUT, DELETE exitosos |
| **400** | Bad Request (Error) | Datos inválidos |
| **404** | Not Found (No existe) | ID no encontrado |
| **500** | Server Error | Error en la BD |

---

## 📍 Acceder a Swagger

Una vez que reinicies Flask, accede a:

```
http://localhost:5000/api/docs
```

Verás la interfaz Swagger interactiva donde puedes probar todas las 24 rutas directamente.

---

## ✅ Resumen

✓ **24 rutas CRUD** en 6 tablas
✓ **Métodos HTTP correctos:** POST (insert), GET (select), PUT (update), DELETE (delete)
✓ **Respuestas JSON estándar:** `{status, message, data}`
✓ **Swagger documentado:** `/api/docs`
✓ **Validación de datos:** Campos requeridos controlados
✓ **Relaciones de BD:** Foreign keys configuradas
