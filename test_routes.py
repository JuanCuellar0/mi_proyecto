import unittest
from app import app

class TestRoutes(unittest.TestCase):
    """Pruebas para las rutas de la aplicación"""
    
    def setUp(self):
        """Configurar el cliente de prueba antes de cada test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    # Pruebas GET
    def test_home_route(self):
        """Probar ruta principal /"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        print("✓ GET / - OK")
    
    def test_encuesta_route(self):
        """Probar ruta de encuesta"""
        response = self.client.get('/encuesta')
        self.assertEqual(response.status_code, 200)
        print("✓ GET /encuesta - OK")
    
    def test_gracias_route(self):
        """Probar ruta de agradecimiento"""
        response = self.client.get('/gracias_enc')
        self.assertEqual(response.status_code, 200)
        print("✓ GET /gracias_enc - OK")
    
    def test_resultados_route(self):
        """Probar ruta de resultados"""
        response = self.client.get('/resultados_caracterizacion')
        self.assertEqual(response.status_code, 200)
        print("✓ GET /resultados_caracterizacion - OK")
    
    # Pruebas POST
    def test_enviar_caracterizacion(self):
        """Probar envío de formulario de caracterización"""
        data = {
            'nombre': 'Test User',
            'correo': 'test@example.com',
            'edad': '20',
            # Agregar más campos según tu formulario
        }
        response = self.client.post('/enviar_caracterizacion', data=data)
        # Debería redirigir a gracias
        self.assertEqual(response.status_code, 302)
        print("✓ POST /enviar_caracterizacion - OK")
    
    def test_enviar_contacto(self):
        """Probar envío de formulario de contacto"""
        data = {
            'nombre': 'Contact Test',
            'correo': 'contact@example.com',
            'mensaje': 'Mensaje de prueba'
        }
        response = self.client.post('/enviar_contacto', data=data)
        # Debería redirigir a gracias
        self.assertEqual(response.status_code, 302)
        print("✓ POST /enviar_contacto - OK")


if __name__ == '__main__':
    unittest.main()
