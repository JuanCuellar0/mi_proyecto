"""Módulo de modelos de datos"""
from dataclasses import dataclass, asdict
from typing import Optional, List
from datetime import date, datetime


@dataclass
class CaracterizacionPersonal:
    """Datos personales del aspirante"""
    tipo_documento: str = ''
    identificacion: str = ''
    fecha_expedicion: Optional[date] = None
    lugar_expedicion: str = ''
    primer_nombre: str = ''
    segundo_nombre: str = ''
    primer_apellido: str = ''
    segundo_apellido: str = ''
    libreta_militar: str = ''
    distrito_militar: str = ''
    tipo_sanguineo: str = ''
    eps_afiliacion: str = ''
    otra_eps: str = ''
    estado_civil: str = ''
    pais_origen: str = ''
    departamento_origen: str = ''
    ciudad_origen: str = ''
    fecha_nacimiento: Optional[date] = None
    
    def get_nombre_completo(self) -> str:
        """Retorna el nombre completo"""
        nombres = [self.primer_nombre, self.segundo_nombre]
        apellidos = [self.primer_apellido, self.segundo_apellido]
        return f"{' '.join(filter(None, nombres))} {' '.join(filter(None, apellidos))}".strip()


@dataclass
class CaracterizacionUbicacion:
    """Información de ubicación"""
    pais: str = ''
    departamento: str = ''
    ciudad: str = ''
    barrio: str = ''
    direccion: str = ''
    telefono_contacto: str = ''
    telefono_celular: str = ''
    correo_electronico: str = ''
    direccion_correspondencia: str = ''


@dataclass
class CaracterizacionSocioeconoma:
    """Información socioeconómica"""
    sisben_sn: str = ''
    grupo_sisben: str = ''
    estrato: Optional[int] = None
    acceso: str = ''


@dataclass
class CaracterizacionDiversidad:
    """Información de caracterización y diversidad"""
    pueblo_indigena: str = ''
    comunidad_negra: str = ''
    tiene_discapacidad: str = ''
    tipo_discapacidad: str = ''
    capacidad_excepcional: str = ''
    desv_grupos_armados: str = ''
    vulnerabilidad_social: str = ''
    orientacion_sexual: str = ''
    consume_psicoactiva: str = ''


@dataclass
class CaracterizacionAcademica:
    """Información académica"""
    motivo_principal: str = ''
    motivo_otro: str = ''
    promedio: Optional[float] = None
    nivel_manejo: str = ''
    como_entero: List[str] = None
    tiene_titulo_prof: str = ''
    nombre_ies_titulo: str = ''
    
    def __post_init__(self):
        if self.como_entero is None:
            self.como_entero = []


@dataclass
class Caracterizacion:
    """Modelo completo de caracterización"""
    id: Optional[int] = None
    fecha: Optional[datetime] = None
    genero: str = ''
    edad: Optional[int] = None
    residencia: str = ''
    trabaja: str = ''
    
    personal: CaracterizacionPersonal = None
    ubicacion: CaracterizacionUbicacion = None
    socioeconoma: CaracterizacionSocioeconoma = None
    diversidad: CaracterizacionDiversidad = None
    academica: CaracterizacionAcademica = None
    
    def __post_init__(self):
        if self.personal is None:
            self.personal = CaracterizacionPersonal()
        if self.ubicacion is None:
            self.ubicacion = CaracterizacionUbicacion()
        if self.socioeconoma is None:
            self.socioeconoma = CaracterizacionSocioeconoma()
        if self.diversidad is None:
            self.diversidad = CaracterizacionDiversidad()
        if self.academica is None:
            self.academica = CaracterizacionAcademica()
    
    def to_dict_flat(self) -> dict:
        """Convierte el modelo a un diccionario plano para la BD"""
        data = {
            'genero': self.genero,
            'edad': self.edad,
            'residencia': self.residencia,
            'trabaja': self.trabaja,
            'promedio': self.academica.promedio,
            'motivo_principal': self.academica.motivo_principal,
            'motivo_otro': self.academica.motivo_otro,
            'nivel_manejo': self.academica.nivel_manejo,
            'acceso': self.socioeconoma.acceso,
        }
        data.update(asdict(self.personal))
        data.update(asdict(self.ubicacion))
        data.update(asdict(self.socioeconoma))
        data.update(asdict(self.diversidad))
        return data
    
    @staticmethod
    def from_form_data(form_data: dict) -> 'Caracterizacion':
        """Crea una instancia desde datos de formulario"""
        def to_int(v):
            try:
                return int(v) if v else None
            except (ValueError, TypeError):
                return None
        
        def to_float(v):
            try:
                return float(v) if v else None
            except (ValueError, TypeError):
                return None
        
        personal = CaracterizacionPersonal(
            tipo_documento=form_data.get('tipo_documento', ''),
            identificacion=form_data.get('identificacion', ''),
            fecha_expedicion=form_data.get('fecha_expedicion'),
            lugar_expedicion=form_data.get('lugar_expedicion', ''),
            primer_nombre=form_data.get('primer_nombre', ''),
            segundo_nombre=form_data.get('segundo_nombre', ''),
            primer_apellido=form_data.get('primer_apellido', ''),
            segundo_apellido=form_data.get('segundo_apellido', ''),
            libreta_militar=form_data.get('libreta_militar', ''),
            distrito_militar=form_data.get('distrito_militar', ''),
            tipo_sanguineo=form_data.get('tipo_sanguineo', ''),
            eps_afiliacion=form_data.get('eps_afiliacion', ''),
            otra_eps=form_data.get('otra_eps', ''),
            estado_civil=form_data.get('estado_civil', ''),
            pais_origen=form_data.get('pais_origen', ''),
            departamento_origen=form_data.get('departamento_origen', ''),
            ciudad_origen=form_data.get('ciudad_origen', ''),
            fecha_nacimiento=form_data.get('fecha_nacimiento'),
        )
        
        ubicacion = CaracterizacionUbicacion(
            pais=form_data.get('pais', ''),
            departamento=form_data.get('departamento', ''),
            ciudad=form_data.get('ciudad', ''),
            barrio=form_data.get('barrio', ''),
            direccion=form_data.get('direccion', ''),
            telefono_contacto=form_data.get('telefono_contacto', ''),
            telefono_celular=form_data.get('telefono_celular', ''),
            correo_electronico=form_data.get('correo_electronico', ''),
            direccion_correspondencia=form_data.get('direccion_correspondencia', ''),
        )
        
        socioeconoma = CaracterizacionSocioeconoma(
            sisben_sn=form_data.get('sisben_sn', ''),
            grupo_sisben=form_data.get('grupo_sisben', '') if (form_data.get('sisben_sn', '').strip().upper() == 'SI') else '',
            estrato=to_int(form_data.get('estrato')),
            acceso=form_data.get('acceso', ''),
        )
        
        diversidad = CaracterizacionDiversidad(
            pueblo_indigena=form_data.get('pueblo_indigena', ''),
            comunidad_negra=form_data.get('comunidad_negra', ''),
            tiene_discapacidad=form_data.get('tiene_discapacidad', ''),
            tipo_discapacidad=form_data.get('tipo_discapacidad', '') if (form_data.get('tiene_discapacidad', '').strip().upper() == 'SI') else '',
            capacidad_excepcional=form_data.get('capacidad_excepcional', ''),
            desv_grupos_armados=form_data.get('desv_grupos_armados', ''),
            vulnerabilidad_social=form_data.get('vulnerabilidad_social', ''),
            orientacion_sexual=form_data.get('orientacion_sexual', ''),
            consume_psicoactiva=form_data.get('consume_psicoactiva', ''),
        )
        
        academica = CaracterizacionAcademica(
            motivo_principal=form_data.get('motivo_principal', ''),
            motivo_otro=form_data.get('motivo_otro', ''),
            promedio=to_float(form_data.get('promedio')),
            nivel_manejo=form_data.get('nivel_manejo', ''),
            como_entero=form_data.getlist('como_entero') if hasattr(form_data, 'getlist') else [],
            tiene_titulo_prof=form_data.get('tiene_titulo_prof', ''),
            nombre_ies_titulo=form_data.get('nombre_ies_titulo', ''),
        )
        
        return Caracterizacion(
            genero=form_data.get('genero', ''),
            edad=to_int(form_data.get('edad')),
            residencia=form_data.get('residencia', ''),
            trabaja=form_data.get('trabaja', ''),
            personal=personal,
            ubicacion=ubicacion,
            socioeconoma=socioeconoma,
            diversidad=diversidad,
            academica=academica,
        )


@dataclass
class Contacto:
    """Modelo para mensajes de contacto"""
    id: Optional[int] = None
    fecha: Optional[datetime] = None
    nombre: str = ''
    correo: str = ''
    mensaje: str = ''
    
    def to_dict(self) -> dict:
        """Convierte a diccionario"""
        return asdict(self)
