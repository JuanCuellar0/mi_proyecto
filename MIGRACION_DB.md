# 📊 Migración a Base de Datos Normalizada

## Cambios Realizados

La base de datos ha sido normalizada de **1 tabla grande** a **6 tablas relacionadas**:

### Estructura Anterior (Monolítica)
```
caracterizacion (todos los campos en una sola tabla)
```

### Estructura Nueva (Normalizada)
```
caracterizacion (tabla principal)
├── caracterizacion_personal (datos personales)
├── caracterizacion_ubicacion (ubicación)
├── caracterizacion_socioeconomica (datos socioeconómicos)
├── caracterizacion_diversidad (diversidad e inclusión)
└── caracterizacion_academica (datos académicos)
```

---

## 🗑️ Paso 1: Limpiar la Base de Datos Antigua

Necesitas eliminar la tabla antigua antes de usar la aplicación con la nueva estructura:

**Opción A - Via MySQL Workbench o Cliente SQL:**
```sql
DROP TABLE IF EXISTS mi_proyecto.caracterizacion;
```

**Opción B - Via phpMyAdmin:**
1. Abre phpMyAdmin (usualmente en `http://localhost/phpmyadmin`)
2. Selecciona la base de datos `mi_proyecto`
3. Busca la tabla `caracterizacion`
4. Click derecho → "Eliminar"

---

## ✅ Paso 2: Reiniciar la Aplicación

Una vez eliminada la tabla:

```bash
python app.py
```

La aplicación automáticamente:
1. Recreará la base de datos `mi_proyecto`
2. Creará las 6 nuevas tablas con relaciones
3. Estará lista para usar

---

## 📋 Ventajas de la Nueva Estructura

✅ **Mejor organización** - Datos separados por categoría  
✅ **Menos redundancia** - Cada dato se almacena una sola vez  
✅ **Integridad referencial** - Relaciones automáticas entre tablas  
✅ **Más escalable** - Fácil agregar nuevas categorías  
✅ **Análisis de riesgo funciona igual** - Las queries se adaptan automáticamente  

---

## 🔄 Migración Manual de Datos (Opcional)

Si tienes datos antiguos que quieres conservar, puedo crear un script de migración. Contáctame.

---

## 📝 Nota

- La aplicación seguirá funcionando igual desde el interfaz del usuario
- La encuesta sigue siendo la misma
- El análisis de riesgo se calcula de la misma forma
- Solo la estructura interna de la BD cambió

---

**Última actualización:** 5 de marzo de 2026
