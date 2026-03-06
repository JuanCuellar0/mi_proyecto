"""Módulo de servicios de negocio"""
from typing import List, Tuple, Dict, Optional
from database import Database, DatabaseConfig
from models import Caracterizacion, Contacto


class RiskAnalysisService:
    """Servicio para análisis de riesgo de deserción"""
    
    @staticmethod
    def to_float(value, default=None) -> Optional[float]:
        """Convierte valor a float"""
        try:
            return float(value) if value is not None and value != "" else default
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def to_int(value, default=None) -> Optional[int]:
        """Convierte valor a int"""
        try:
            return int(value) if value is not None and value != "" else default
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def score_row(row: dict) -> Tuple[int, str, List[str]]:
        """Calcula el score y nivel de riesgo para un registro"""
        promedio = RiskAnalysisService.to_float(row.get("promedio"))
        estrato = RiskAnalysisService.to_int(row.get("estrato"))
        
        acceso = (row.get("acceso") or "").lower()
        sisben_sn = (row.get("sisben_sn") or "").strip().upper()
        vulnerabilidad_social = (row.get("vulnerabilidad_social") or "").strip()
        tiene_discapacidad = (row.get("tiene_discapacidad") or "").strip().upper()
        consume_psicoactiva = (row.get("consume_psicoactiva") or "").strip().upper()
        
        reasons = []
        
        # Alto riesgo
        if (consume_psicoactiva == "SI" or bool(vulnerabilidad_social)):
            level = "Alto"
            score = 80
            if consume_psicoactiva == "SI":
                reasons.append("Consumo de sustancia psicoactiva")
            if vulnerabilidad_social:
                reasons.append("Vulnerabilidad social/económica")
        
        # Riesgo medio
        elif ((estrato is not None and estrato <= 2)
              or "solo celular" in acceso
              or "limitado" in acceso or "compartido" in acceso
              or sisben_sn == "SI"
              or tiene_discapacidad == "SI"):
            level = "Medio"
            score = 50
            if estrato is not None and estrato <= 2:
                reasons.append("Estrato 1–2")
            if "solo celular" in acceso:
                reasons.append("Solo celular")
            if "limitado" in acceso or "compartido" in acceso:
                reasons.append("Internet limitado/compartido")
            if sisben_sn == "SI":
                reasons.append("Sisbén: SI")
            if tiene_discapacidad == "SI":
                reasons.append("Tiene discapacidad")
        
        # Bajo riesgo
        else:
            level = "Bajo"
            score = 20
            reasons.append("Sin indicadores de riesgo principales")
        
        return score, level, reasons


class CaracterizacionRepository:
    """Repositorio para operaciones de Caracterizacion"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def initialize_table(self) -> None:
        """Crea las tablas normalizadas de caracterización"""
        
        # Tabla principal
        query_base = """
            CREATE TABLE IF NOT EXISTS caracterizacion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                genero VARCHAR(20),
                edad INT,
                trabaja VARCHAR(5),
                residencia VARCHAR(100),
                INDEX idx_fecha (fecha),
                INDEX idx_genero (genero)
            )
        """
        self.db.execute_query(query_base)
        
        # Tabla de datos personales
        query_personal = """
            CREATE TABLE IF NOT EXISTS caracterizacion_personal (
                id INT AUTO_INCREMENT PRIMARY KEY,
                caracterizacion_id INT NOT NULL,
                tipo_documento VARCHAR(50),
                identificacion VARCHAR(50),
                fecha_expedicion DATE,
                lugar_expedicion VARCHAR(255),
                primer_nombre VARCHAR(100),
                segundo_nombre VARCHAR(100),
                primer_apellido VARCHAR(100),
                segundo_apellido VARCHAR(100),
                libreta_militar VARCHAR(50),
                distrito_militar VARCHAR(50),
                tipo_sanguineo VARCHAR(10),
                eps_afiliacion VARCHAR(255),
                otra_eps VARCHAR(255),
                estado_civil VARCHAR(50),
                pais_origen VARCHAR(100),
                departamento_origen VARCHAR(100),
                ciudad_origen VARCHAR(100),
                fecha_nacimiento DATE,
                FOREIGN KEY (caracterizacion_id) REFERENCES caracterizacion(id) ON DELETE CASCADE
            )
        """
        self.db.execute_query(query_personal)
        
        # Tabla de ubicación
        query_ubicacion = """
            CREATE TABLE IF NOT EXISTS caracterizacion_ubicacion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                caracterizacion_id INT NOT NULL,
                pais VARCHAR(100),
                departamento VARCHAR(100),
                ciudad VARCHAR(100),
                barrio VARCHAR(100),
                direccion VARCHAR(255),
                telefono_contacto VARCHAR(50),
                telefono_celular VARCHAR(50),
                correo_electronico VARCHAR(255),
                direccion_correspondencia VARCHAR(255),
                FOREIGN KEY (caracterizacion_id) REFERENCES caracterizacion(id) ON DELETE CASCADE
            )
        """
        self.db.execute_query(query_ubicacion)
        
        # Tabla socioeconómica
        query_socioeconomica = """
            CREATE TABLE IF NOT EXISTS caracterizacion_socioeconomica (
                id INT AUTO_INCREMENT PRIMARY KEY,
                caracterizacion_id INT NOT NULL,
                sisben_sn VARCHAR(5),
                grupo_sisben VARCHAR(50),
                estrato VARCHAR(5),
                acceso VARCHAR(100),
                FOREIGN KEY (caracterizacion_id) REFERENCES caracterizacion(id) ON DELETE CASCADE
            )
        """
        self.db.execute_query(query_socioeconomica)
        
        # Tabla de diversidad
        query_diversidad = """
            CREATE TABLE IF NOT EXISTS caracterizacion_diversidad (
                id INT AUTO_INCREMENT PRIMARY KEY,
                caracterizacion_id INT NOT NULL,
                pueblo_indigena VARCHAR(100),
                comunidad_negra VARCHAR(100),
                tiene_discapacidad VARCHAR(5),
                tipo_discapacidad VARCHAR(255),
                capacidad_excepcional VARCHAR(255),
                desv_grupos_armados VARCHAR(5),
                vulnerabilidad_social VARCHAR(255),
                orientacion_sexual VARCHAR(100),
                consume_psicoactiva VARCHAR(5),
                FOREIGN KEY (caracterizacion_id) REFERENCES caracterizacion(id) ON DELETE CASCADE
            )
        """
        self.db.execute_query(query_diversidad)
        
        # Tabla académica
        query_academica = """
            CREATE TABLE IF NOT EXISTS caracterizacion_academica (
                id INT AUTO_INCREMENT PRIMARY KEY,
                caracterizacion_id INT NOT NULL,
                motivo_principal VARCHAR(255),
                motivo_otro VARCHAR(255),
                promedio FLOAT,
                nivel_manejo VARCHAR(100),
                FOREIGN KEY (caracterizacion_id) REFERENCES caracterizacion(id) ON DELETE CASCADE
            )
        """
        self.db.execute_query(query_academica)
    
    def create(self, caracterizacion: Caracterizacion) -> int:
        """Crea un nuevo registro de caracterización en tablas normalizadas"""
        # 1. Insertar en tabla base
        query_base = "INSERT INTO caracterizacion (genero, edad, trabaja, residencia) VALUES (%s, %s, %s, %s)"
        caracterizacion_id = self.db.insert(query_base, (
            caracterizacion.genero,
            caracterizacion.edad,
            caracterizacion.trabaja,
            caracterizacion.residencia
        ))
        
        # 2. Insertar en tabla personal
        p = caracterizacion.personal
        query_personal = """
            INSERT INTO caracterizacion_personal 
            (caracterizacion_id, tipo_documento, identificacion, fecha_expedicion, lugar_expedicion, 
             primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, libreta_militar, 
             distrito_militar, tipo_sanguineo, eps_afiliacion, otra_eps, estado_civil, 
             pais_origen, departamento_origen, ciudad_origen, fecha_nacimiento)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.db.insert(query_personal, (
            caracterizacion_id, p.tipo_documento, p.identificacion, p.fecha_expedicion, p.lugar_expedicion,
            p.primer_nombre, p.segundo_nombre, p.primer_apellido, p.segundo_apellido, p.libreta_militar,
            p.distrito_militar, p.tipo_sanguineo, p.eps_afiliacion, p.otra_eps, p.estado_civil,
            p.pais_origen, p.departamento_origen, p.ciudad_origen, p.fecha_nacimiento
        ))
        
        # 3. Insertar en tabla ubicación
        u = caracterizacion.ubicacion
        query_ubicacion = """
            INSERT INTO caracterizacion_ubicacion 
            (caracterizacion_id, pais, departamento, ciudad, barrio, direccion, 
             telefono_contacto, telefono_celular, correo_electronico, direccion_correspondencia)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.db.insert(query_ubicacion, (
            caracterizacion_id, u.pais, u.departamento, u.ciudad, u.barrio, u.direccion,
            u.telefono_contacto, u.telefono_celular, u.correo_electronico, u.direccion_correspondencia
        ))
        
        # 4. Insertar en tabla socioeconómica
        s = caracterizacion.socioeconoma
        query_socio = """
            INSERT INTO caracterizacion_socioeconomica 
            (caracterizacion_id, sisben_sn, grupo_sisben, estrato, acceso)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.db.insert(query_socio, (
            caracterizacion_id, s.sisben_sn, s.grupo_sisben, s.estrato, s.acceso
        ))
        
        # 5. Insertar en tabla diversidad
        d = caracterizacion.diversidad
        query_diversidad = """
            INSERT INTO caracterizacion_diversidad 
            (caracterizacion_id, pueblo_indigena, comunidad_negra, tiene_discapacidad, tipo_discapacidad,
             capacidad_excepcional, desv_grupos_armados, vulnerabilidad_social, orientacion_sexual, consume_psicoactiva)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.db.insert(query_diversidad, (
            caracterizacion_id, d.pueblo_indigena, d.comunidad_negra, d.tiene_discapacidad, d.tipo_discapacidad,
            d.capacidad_excepcional, d.desv_grupos_armados, d.vulnerabilidad_social, d.orientacion_sexual, d.consume_psicoactiva
        ))
        
        # 6. Insertar en tabla académica
        a = caracterizacion.academica
        query_academica = """
            INSERT INTO caracterizacion_academica 
            (caracterizacion_id, motivo_principal, motivo_otro, promedio, nivel_manejo)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.db.insert(query_academica, (
            caracterizacion_id, a.motivo_principal, a.motivo_otro, a.promedio, a.nivel_manejo
        ))
        
        return caracterizacion_id
    
    def get_all(self) -> List[dict]:
        """Obtiene todos los registros combinando todas las tablas"""
        query = """
            SELECT c.*, p.*, u.*, s.*, d.*, a.*
            FROM caracterizacion c
            LEFT JOIN caracterizacion_personal p ON c.id = p.caracterizacion_id
            LEFT JOIN caracterizacion_ubicacion u ON c.id = u.caracterizacion_id
            LEFT JOIN caracterizacion_socioeconomica s ON c.id = s.caracterizacion_id
            LEFT JOIN caracterizacion_diversidad d ON c.id = d.caracterizacion_id
            LEFT JOIN caracterizacion_academica a ON c.id = a.caracterizacion_id
            ORDER BY c.fecha DESC
        """
        return self.db.fetch_all(query, dict_cursor=True)
    
    def get_by_id(self, id: int) -> Optional[dict]:
        """Obtiene un registro por ID combinando todas las tablas"""
        query = """
            SELECT c.*, p.*, u.*, s.*, d.*, a.*
            FROM caracterizacion c
            LEFT JOIN caracterizacion_personal p ON c.id = p.caracterizacion_id
            LEFT JOIN caracterizacion_ubicacion u ON c.id = u.caracterizacion_id
            LEFT JOIN caracterizacion_socioeconomica s ON c.id = s.caracterizacion_id
            LEFT JOIN caracterizacion_diversidad d ON c.id = d.caracterizacion_id
            LEFT JOIN caracterizacion_academica a ON c.id = a.caracterizacion_id
            WHERE c.id = %s
        """
        return self.db.fetch_one(query, (id,), dict_cursor=True)
    
    def delete_all(self) -> int:
        """Elimina todos los registros (las tablas secundarias se borran en cascada)"""
        query = "DELETE FROM caracterizacion"
        return self.db.delete(query)
    
    def update(self, id: int, caracterizacion: Caracterizacion) -> int:
        """Actualiza un registro de caracterización en tablas normalizadas"""
        
        # 1. Actualizar tabla base
        query_base = "UPDATE caracterizacion SET genero = %s, edad = %s, trabaja = %s, residencia = %s WHERE id = %s"
        self.db.update(query_base, (
            caracterizacion.genero,
            caracterizacion.edad,
            caracterizacion.trabaja,
            caracterizacion.residencia,
            id
        ))
        
        # 2. Actualizar tabla personal
        p = caracterizacion.personal
        query_personal = """
            UPDATE caracterizacion_personal SET 
            tipo_documento = %s, identificacion = %s, fecha_expedicion = %s, lugar_expedicion = %s,
            primer_nombre = %s, segundo_nombre = %s, primer_apellido = %s, segundo_apellido = %s,
            libreta_militar = %s, distrito_militar = %s, tipo_sanguineo = %s, eps_afiliacion = %s,
            otra_eps = %s, estado_civil = %s, pais_origen = %s, departamento_origen = %s,
            ciudad_origen = %s, fecha_nacimiento = %s
            WHERE caracterizacion_id = %s
        """
        self.db.update(query_personal, (
            p.tipo_documento, p.identificacion, p.fecha_expedicion, p.lugar_expedicion,
            p.primer_nombre, p.segundo_nombre, p.primer_apellido, p.segundo_apellido,
            p.libreta_militar, p.distrito_militar, p.tipo_sanguineo, p.eps_afiliacion,
            p.otra_eps, p.estado_civil, p.pais_origen, p.departamento_origen,
            p.ciudad_origen, p.fecha_nacimiento, id
        ))
        
        # 3. Actualizar tabla ubicación
        u = caracterizacion.ubicacion
        query_ubicacion = """
            UPDATE caracterizacion_ubicacion SET 
            pais = %s, departamento = %s, ciudad = %s, barrio = %s, direccion = %s,
            telefono_contacto = %s, telefono_celular = %s, correo_electronico = %s, 
            direccion_correspondencia = %s
            WHERE caracterizacion_id = %s
        """
        self.db.update(query_ubicacion, (
            u.pais, u.departamento, u.ciudad, u.barrio, u.direccion,
            u.telefono_contacto, u.telefono_celular, u.correo_electronico,
            u.direccion_correspondencia, id
        ))
        
        # 4. Actualizar tabla socioeconómica
        s = caracterizacion.socioeconoma
        query_socio = """
            UPDATE caracterizacion_socioeconomica SET 
            sisben_sn = %s, grupo_sisben = %s, estrato = %s, acceso = %s
            WHERE caracterizacion_id = %s
        """
        self.db.update(query_socio, (s.sisben_sn, s.grupo_sisben, s.estrato, s.acceso, id))
        
        # 5. Actualizar tabla diversidad
        d = caracterizacion.diversidad
        query_diversidad = """
            UPDATE caracterizacion_diversidad SET 
            pueblo_indigena = %s, comunidad_negra = %s, tiene_discapacidad = %s, 
            tipo_discapacidad = %s, capacidad_excepcional = %s, desv_grupos_armados = %s,
            vulnerabilidad_social = %s, orientacion_sexual = %s, consume_psicoactiva = %s
            WHERE caracterizacion_id = %s
        """
        self.db.update(query_diversidad, (
            d.pueblo_indigena, d.comunidad_negra, d.tiene_discapacidad, d.tipo_discapacidad,
            d.capacidad_excepcional, d.desv_grupos_armados, d.vulnerabilidad_social,
            d.orientacion_sexual, d.consume_psicoactiva, id
        ))
        
        # 6. Actualizar tabla académica
        a = caracterizacion.academica
        query_academica = """
            UPDATE caracterizacion_academica SET 
            motivo_principal = %s, motivo_otro = %s, promedio = %s, nivel_manejo = %s
            WHERE caracterizacion_id = %s
        """
        self.db.update(query_academica, (
            a.motivo_principal, a.motivo_otro, a.promedio, a.nivel_manejo, id
        ))
        
        return 1
    
    def delete_by_id(self, id: int) -> int:
        """Elimina un registro por ID"""
        query = "DELETE FROM caracterizacion WHERE id = %s"
        return self.db.delete(query, (id,))


class ContactoRepository:
    """Repositorio para operaciones de Contacto"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def initialize_table(self) -> None:
        """Crea la tabla de contacto"""
        query = """
            CREATE TABLE IF NOT EXISTS contacto_mensajes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                nombre VARCHAR(150) NOT NULL,
                correo VARCHAR(255) NOT NULL,
                mensaje TEXT NOT NULL
            )
        """
        self.db.execute_query(query)
    
    def create(self, contacto: Contacto) -> int:
        """Crea un nuevo mensaje de contacto"""
        query = """
            INSERT INTO contacto_mensajes (nombre, correo, mensaje)
            VALUES (%s, %s, %s)
        """
        return self.db.insert(query, (contacto.nombre, contacto.correo, contacto.mensaje))
    
    def get_all(self) -> List[dict]:
        """Obtiene todos los mensajes"""
        query = "SELECT id, fecha, nombre, correo, mensaje FROM contacto_mensajes ORDER BY fecha DESC"
        return self.db.fetch_all(query, dict_cursor=True)
    
    def get_by_id(self, id: int) -> Optional[dict]:
        """Obtiene un mensaje por ID"""
        query = "SELECT * FROM contacto_mensajes WHERE id = %s"
        return self.db.fetch_one(query, (id,), dict_cursor=True)
    
    def delete_all(self) -> int:
        """Elimina todos los mensajes"""
        query = "DELETE FROM contacto_mensajes"
        return self.db.delete(query)
    
    def update(self, id: int, contacto: Contacto) -> int:
        """Actualiza un mensaje de contacto"""
        query = """
            UPDATE contacto_mensajes SET nombre = %s, correo = %s, mensaje = %s
            WHERE id = %s
        """
        return self.db.update(query, (contacto.nombre, contacto.correo, contacto.mensaje, id))
    
    def delete_by_id(self, id: int) -> int:
        """Elimina un mensaje por ID"""
        query = "DELETE FROM contacto_mensajes WHERE id = %s"
        return self.db.delete(query, (id,))


class RiskAnalysisRepository:
    """Repositorio para análisis de riesgo"""
    
    def __init__(self, caracterizacion_repo: CaracterizacionRepository):
        self.caracterizacion_repo = caracterizacion_repo
    
    def analyze_all(self) -> List[Dict]:
        """Analiza el riesgo de todos los registros"""
        rows = self.caracterizacion_repo.get_all()
        results = []
        
        for row in rows:
            score, level, reasons = RiskAnalysisService.score_row(row)
            
            # No eliminar 'fecha' si no existe
            if 'fecha' in row:
                del row['fecha']
            
            result = {
                "id": row.get("id"),
                "nombre": (row.get("primer_nombre", "").strip() + " " + row.get("primer_apellido", "").strip()).strip(),
                "estrato": row.get("estrato"),
                "acceso": row.get("acceso"),
                "sisben_sn": row.get("sisben_sn"),
                "grupo_sisben": row.get("grupo_sisben"),
                "vulnerabilidad_social": row.get("vulnerabilidad_social"),
                "tiene_discapacidad": row.get("tiene_discapacidad"),
                "consume_psicoactiva": row.get("consume_psicoactiva"),
                "score": score,
                "nivel": level,
                "razones": "; ".join(reasons),
            }
            results.append(result)
        
        return results


class CaracterizacionPersonalRepository:
    """Repositorio para características personales"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def get_by_caracterizacion_id(self, char_id: int) -> Optional[dict]:
        """Obtiene datos personales por ID de caracterización"""
        query = "SELECT * FROM caracterizacion_personal WHERE caracterizacion_id = %s"
        return self.db.fetch_one(query, (char_id,), dict_cursor=True)
    
    def get_by_id(self, id: int) -> Optional[dict]:
        """Obtiene datos personales por ID"""
        query = "SELECT * FROM caracterizacion_personal WHERE id = %s"
        return self.db.fetch_one(query, (id,), dict_cursor=True)
    
    def create(self, char_id: int, datos: dict) -> int:
        """Crea registro de datos personales"""
        query = """
            INSERT INTO caracterizacion_personal 
            (caracterizacion_id, tipo_documento, identificacion, fecha_expedicion, lugar_expedicion,
             primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, libreta_militar,
             distrito_militar, tipo_sanguineo, eps_afiliacion, otra_eps, estado_civil,
             pais_origen, departamento_origen, ciudad_origen, fecha_nacimiento)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (char_id, datos.get('tipo_documento'), datos.get('identificacion'),
                  datos.get('fecha_expedicion'), datos.get('lugar_expedicion'),
                  datos.get('primer_nombre'), datos.get('segundo_nombre'),
                  datos.get('primer_apellido'), datos.get('segundo_apellido'),
                  datos.get('libreta_militar'), datos.get('distrito_militar'),
                  datos.get('tipo_sanguineo'), datos.get('eps_afiliacion'),
                  datos.get('otra_eps'), datos.get('estado_civil'),
                  datos.get('pais_origen'), datos.get('departamento_origen'),
                  datos.get('ciudad_origen'), datos.get('fecha_nacimiento'))
        return self.db.insert(query, values)
    
    def update(self, id: int, datos: dict) -> int:
        """Actualiza registro de datos personales"""
        query = """
            UPDATE caracterizacion_personal SET
            tipo_documento=%s, identificacion=%s, fecha_expedicion=%s, lugar_expedicion=%s,
            primer_nombre=%s, segundo_nombre=%s, primer_apellido=%s, segundo_apellido=%s,
            libreta_militar=%s, distrito_militar=%s, tipo_sanguineo=%s, eps_afiliacion=%s,
            otra_eps=%s, estado_civil=%s, pais_origen=%s, departamento_origen=%s,
            ciudad_origen=%s, fecha_nacimiento=%s
            WHERE id = %s
        """
        values = (datos.get('tipo_documento'), datos.get('identificacion'),
                  datos.get('fecha_expedicion'), datos.get('lugar_expedicion'),
                  datos.get('primer_nombre'), datos.get('segundo_nombre'),
                  datos.get('primer_apellido'), datos.get('segundo_apellido'),
                  datos.get('libreta_militar'), datos.get('distrito_militar'),
                  datos.get('tipo_sanguineo'), datos.get('eps_afiliacion'),
                  datos.get('otra_eps'), datos.get('estado_civil'),
                  datos.get('pais_origen'), datos.get('departamento_origen'),
                  datos.get('ciudad_origen'), datos.get('fecha_nacimiento'), id)
        return self.db.update(query, values)
    
    def delete(self, id: int) -> int:
        """Elimina registro de datos personales"""
        query = "DELETE FROM caracterizacion_personal WHERE id = %s"
        return self.db.delete(query, (id,))


class CaracterizacionUbicacionRepository:
    """Repositorio para datos de ubicación"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[dict]:
        """Obtiene datos de ubicación por ID"""
        query = "SELECT * FROM caracterizacion_ubicacion WHERE id = %s"
        return self.db.fetch_one(query, (id,), dict_cursor=True)
    
    def create(self, char_id: int, datos: dict) -> int:
        """Crea registro de ubicación"""
        query = """
            INSERT INTO caracterizacion_ubicacion
            (caracterizacion_id, pais, departamento, ciudad, barrio, direccion,
             telefono_contacto, telefono_celular, correo_electronico, direccion_correspondencia)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (char_id, datos.get('pais'), datos.get('departamento'),
                  datos.get('ciudad'), datos.get('barrio'), datos.get('direccion'),
                  datos.get('telefono_contacto'), datos.get('telefono_celular'),
                  datos.get('correo_electronico'), datos.get('direccion_correspondencia'))
        return self.db.insert(query, values)
    
    def update(self, id: int, datos: dict) -> int:
        """Actualiza registro de ubicación"""
        query = """
            UPDATE caracterizacion_ubicacion SET
            pais=%s, departamento=%s, ciudad=%s, barrio=%s, direccion=%s,
            telefono_contacto=%s, telefono_celular=%s, correo_electronico=%s,
            direccion_correspondencia=%s
            WHERE id = %s
        """
        values = (datos.get('pais'), datos.get('departamento'), datos.get('ciudad'),
                  datos.get('barrio'), datos.get('direccion'), datos.get('telefono_contacto'),
                  datos.get('telefono_celular'), datos.get('correo_electronico'),
                  datos.get('direccion_correspondencia'), id)
        return self.db.update(query, values)
    
    def delete(self, id: int) -> int:
        """Elimina registro de ubicación"""
        query = "DELETE FROM caracterizacion_ubicacion WHERE id = %s"
        return self.db.delete(query, (id,))


class CaracterizacionSocioeconomicaRepository:
    """Repositorio para datos socioeconómicos"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[dict]:
        """Obtiene datos socioeconómicos por ID"""
        query = "SELECT * FROM caracterizacion_socioeconomica WHERE id = %s"
        return self.db.fetch_one(query, (id,), dict_cursor=True)
    
    def create(self, char_id: int, datos: dict) -> int:
        """Crea registro socioeconómico"""
        query = """
            INSERT INTO caracterizacion_socioeconomica
            (caracterizacion_id, sisben_sn, grupo_sisben, estrato, acceso)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (char_id, datos.get('sisben_sn'), datos.get('grupo_sisben'),
                  datos.get('estrato'), datos.get('acceso'))
        return self.db.insert(query, values)
    
    def update(self, id: int, datos: dict) -> int:
        """Actualiza registro socioeconómico"""
        query = """
            UPDATE caracterizacion_socioeconomica SET
            sisben_sn=%s, grupo_sisben=%s, estrato=%s, acceso=%s
            WHERE id = %s
        """
        values = (datos.get('sisben_sn'), datos.get('grupo_sisben'),
                  datos.get('estrato'), datos.get('acceso'), id)
        return self.db.update(query, values)
    
    def delete(self, id: int) -> int:
        """Elimina registro socioeconómico"""
        query = "DELETE FROM caracterizacion_socioeconomica WHERE id = %s"
        return self.db.delete(query, (id,))


class CaracterizacionDiversidadRepository:
    """Repositorio para datos de diversidad"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[dict]:
        """Obtiene datos de diversidad por ID"""
        query = "SELECT * FROM caracterizacion_diversidad WHERE id = %s"
        return self.db.fetch_one(query, (id,), dict_cursor=True)
    
    def create(self, char_id: int, datos: dict) -> int:
        """Crea registro de diversidad"""
        query = """
            INSERT INTO caracterizacion_diversidad
            (caracterizacion_id, pueblo_indigena, comunidad_negra, tiene_discapacidad,
             tipo_discapacidad, capacidad_excepcional, desv_grupos_armados,
             vulnerabilidad_social, orientacion_sexual, consume_psicoactiva)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (char_id, datos.get('pueblo_indigena'), datos.get('comunidad_negra'),
                  datos.get('tiene_discapacidad'), datos.get('tipo_discapacidad'),
                  datos.get('capacidad_excepcional'), datos.get('desv_grupos_armados'),
                  datos.get('vulnerabilidad_social'), datos.get('orientacion_sexual'),
                  datos.get('consume_psicoactiva'))
        return self.db.insert(query, values)
    
    def update(self, id: int, datos: dict) -> int:
        """Actualiza registro de diversidad"""
        query = """
            UPDATE caracterizacion_diversidad SET
            pueblo_indigena=%s, comunidad_negra=%s, tiene_discapacidad=%s,
            tipo_discapacidad=%s, capacidad_excepcional=%s, desv_grupos_armados=%s,
            vulnerabilidad_social=%s, orientacion_sexual=%s, consume_psicoactiva=%s
            WHERE id = %s
        """
        values = (datos.get('pueblo_indigena'), datos.get('comunidad_negra'),
                  datos.get('tiene_discapacidad'), datos.get('tipo_discapacidad'),
                  datos.get('capacidad_excepcional'), datos.get('desv_grupos_armados'),
                  datos.get('vulnerabilidad_social'), datos.get('orientacion_sexual'),
                  datos.get('consume_psicoactiva'), id)
        return self.db.update(query, values)
    
    def delete(self, id: int) -> int:
        """Elimina registro de diversidad"""
        query = "DELETE FROM caracterizacion_diversidad WHERE id = %s"
        return self.db.delete(query, (id,))
