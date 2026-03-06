"""Módulo de gestión de base de datos"""
import pymysql
from typing import Dict, List, Any, Optional


class DatabaseConfig:
    """Configuración de conexión a la base de datos"""
    
    def __init__(self, host: str = "127.0.0.1", user: str = "root", 
                 password: str = "", database: str = "mi_proyecto", 
                 charset: str = "utf8mb4"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
    
    def get_config(self, dict_cursor: bool = False) -> Dict[str, Any]:
        """Retorna configuración de conexión"""
        config = {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "charset": self.charset,
            "cursorclass": pymysql.cursors.DictCursor if dict_cursor else pymysql.cursors.Cursor,
        }
        return config
    
    def get_server_config(self) -> Dict[str, Any]:
        """Retorna configuración sin especificar base de datos"""
        config = {
            "host": self.host,
            "user": self.user,
            "password": self.password,
            "charset": self.charset,
            "cursorclass": pymysql.cursors.Cursor,
        }
        return config


class Database:
    """Gestor de conexiones y operaciones de base de datos"""
    
    def __init__(self, db_config: DatabaseConfig):
        self.config = db_config
    
    def connect(self, dict_cursor: bool = False) -> pymysql.connections.Connection:
        """Crea una conexión a la base de datos"""
        return pymysql.connect(**self.config.get_config(dict_cursor))
    
    def create_database_if_not_exists(self) -> None:
        """Crea la base de datos si no existe"""
        conn = pymysql.connect(**self.config.get_server_config())
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{self.config.database}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
            )
            conn.commit()
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> None:
        """Ejecuta una consulta sin retornar resultados"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
        finally:
            conn.close()
    
    def fetch_one(self, query: str, params: tuple = (), dict_cursor: bool = False) -> Optional[Dict]:
        """Obtiene un registro"""
        conn = self.connect(dict_cursor)
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            conn.close()
    
    def fetch_all(self, query: str, params: tuple = (), dict_cursor: bool = False) -> List[Any]:
        """Obtiene todos los registros"""
        conn = self.connect(dict_cursor)
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            conn.close()
    
    def insert(self, query: str, params: tuple = ()) -> int:
        """Inserta un registro y retorna el ID"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def update(self, query: str, params: tuple = ()) -> int:
        """Actualiza registros y retorna la cantidad actualizada"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()
    
    def delete(self, query: str, params: tuple = ()) -> int:
        """Elimina registros y retorna la cantidad eliminada"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()
