"""Módulo de utilidades de contacto - Refactorizado con POO"""
# Este módulo ahora se consolidó en app.py
# Se mantiene para compatibilidad con cualquier import existente

from database import Database, DatabaseConfig

# Configuración para compatibilidad
db_config = DatabaseConfig(
    host="127.0.0.1",
    user="root",
    password="",
    database="mi_proyecto",
    charset="utf8mb4"
)

db = Database(db_config)


def ensure_contact_table_exists():
    """Asegura que la tabla de contacto existe"""
    query = """
        CREATE TABLE IF NOT EXISTS contacto_mensajes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            nombre VARCHAR(150) NOT NULL,
            correo VARCHAR(255) NOT NULL,
            mensaje TEXT NOT NULL
        )
    """
    db.execute_query(query)