import unittest
from flask_sqlalchemy import SQLAlchemy

from server import create_app
from models import setup_db, Pelicula, Funcion, Sala, Entrada
import json

class TestCaseTodoApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app() # Instancia de la aplicación.
        self.client = self.app.test_client
        self.database_name = 'peliculasdb_test'
        self.database_path = 'postgresql://{}:{}@localhost:{}/{}'.format('postgres', 'Magdalena150', 5432,self.database_name)

        setup_db(self.app, self.database_path)

        self.new_pelicula = {
            'nombre_pelicula': 'Nueva pelicula',
            'duracion_pelicula': 10,
            'calificacion_pelicula': 10,
            'idioma_pelicula': 'Nuevo idioma'
        }
    @unittest.skip('TEST PASS')
    def test_get_peliculas_success(self):
        res = self.client().get('/peliculas')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_peliculas'])
        self.assertTrue(len(data['peliculas']))
        pass

    @unittest.skip('TEST PASS')
    def test_get_peliculas_sent_requesting_beyond_valid_page_404(self):
        res = self.client().get('/peliculas?page=10000000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])
        pass
        
    @unittest.skip('TEST PASS')
    def test_search_peliculas_by_nombre(self):
        res = self.client().get('/peliculas/Primera pelicula')
        data = json.loads(res.data)
        #print('data:', data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['nombre_pelicula'], 'Primera pelicula')
        self.assertTrue(data['idioma_pelicula'])
        pass

    @unittest.skip('TEST PASS')
    def test_update_pelicula_success(self):
        res0 = self.client().post('/peliculas', json=self.new_pelicula)
        data0 = json.loads(res0.data)
        #print('data: ', data0)

        updated_id = data0['created']
        
        res = self.client().patch('/peliculas/{}'.format(updated_id), json={'nombre_pelicula': 'update test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], str(updated_id))
        self.assertTrue(data['nombre_pelicula'])
        #print('actualiced_data: ', data)
        pass

    @unittest.skip('TEST PASS')
    def test_update_pelicula_failed(self):
        res = self.client().patch('/peliculas/-1000', json={'nombre_pelicula': 'update test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])
        pass


    @unittest.skip('TEST PASS')
    def test_delete_pelicula_success(self):
        res0 = self.client().post('/peliculas', json=self.new_pelicula)
        data0 = json.loads(res0.data)
        print('data_a_eliminar: ', data0)

        eliminar_id = data0['created']
        
        res = self.client().delete('/peliculas/{}'.format(eliminar_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(str(data0['created']), data['deleted'])
        self.assertTrue(data['peliculas'])
        
    @unittest.skip('TEST PASS')
    def test_delete_pelicula_failed(self):
        eliminar_id = -10
        
        res = self.client().delete('/peliculas/{}'.format(eliminar_id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        self.assertFalse(data['success'])
        

    @unittest.skip('TEST PASS')
    def test_create_pelicula_success(self):
        res = self.client().post('/peliculas', json=self.new_pelicula)
        data = json.loads(res.data)
        

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_peliculas'])

    @unittest.skip('TEST PASS')
    def test_create_pelicula_failed(self):
        res = self.client().post('/peliculas', json={'nombre_pelicula': 'Nueva pelicula'})
        data = json.loads(res.data)
        

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertFalse(data['success'])

    def tearDown(self):
        pass
    



