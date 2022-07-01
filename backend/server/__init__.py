import json
from flask import (
    Flask,
    jsonify,
    abort,
    request
)
from flask_cors import CORS
from itsdangerous import NoneAlgorithm

from models import setup_db, Pelicula, Sala, Funcion, Entrada

TODOS_PER_PAGE=5

def pagination_todos(request, selection, isDescendent):
    if isDescendent:
        start =  len(selection) - TODOS_PER_PAGE
        end = len(selection)
    else:
        page = request.args.get('page', 1, type=int)
        start = (page-1)*TODOS_PER_PAGE
        end = start + TODOS_PER_PAGE
    
    todos = [todo.format() for todo in selection]
    current_todos = todos[start:end]
    return current_todos


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, origins=['https://utec.edu.pe', 'http://127.0.0.1:5001', 'http://127.0.0.1:5000'], max_age=10)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorizations, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/peliculas', methods=['POST'])
    def create_pelicula():
        body = request.get_json()
        nombre_pelicula = body.get('nombre_pelicula', None)
        duracion_pelicula = body.get('duracion_pelicula', None)
        calificacion_pelicula = body.get('calificacion_pelicula', None)
        idioma_pelicula = body.get('idioma_pelicula', None)

        if nombre_pelicula is None or duracion_pelicula is None or calificacion_pelicula is None or idioma_pelicula is None:
            abort(422)

        try:
            pelicula = Pelicula(nombre_pelicula=nombre_pelicula, duracion_pelicula=duracion_pelicula, calificacion_pelicula=calificacion_pelicula , idioma_pelicula=idioma_pelicula)
            new_pelicula_id = pelicula.insert()

            selection = Pelicula.query.order_by('id_pelicula').all()
            peliculas = pagination_todos(request, selection, True)

            return jsonify({
                'success': True,
                'created': new_pelicula_id,
                'peliculas': peliculas,
                'total_peliculas': len(selection)
            })
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/peliculas', methods=['GET'])
    def get_peliculas():
        selection = Pelicula.query.order_by('id_pelicula').all()
        peliculas = pagination_todos(request, selection, False)

        if len(peliculas) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'peliculas': peliculas,
            'total_peliculas': len(selection)
        })

    @app.route('/peliculas/<nombre_pelicula>', methods=['GET'])
    def get_peliculas_by_nombre(nombre_pelicula):
        pelicula = Pelicula.query.filter(Pelicula.nombre_pelicula == nombre_pelicula).one_or_none()
        #print('Data: ',pelicula)
        #print('Type: ', type(pelicula))
        if pelicula is None:
            abort(404)

        return jsonify({
            'success': True,
            'nombre_pelicula': pelicula.nombre_pelicula,
            'idioma_pelicula': pelicula.idioma_pelicula
        })

    @app.route('/peliculas/<id_pelicula>', methods=['PATCH'])
    def update_pelicula(id_pelicula):
        error_404 = False
        try:
            pelicula = Pelicula.query.filter(Pelicula.id_pelicula == id_pelicula).one_or_none()
            if pelicula is None:
                error_404 = True
                abort(404)
            

            body = request.get_json()
            if 'nombre_pelicula' in body:
                pelicula.nombre_pelicula = body.get('nombre_pelicula')

            pelicula.update()
            
            return jsonify({
                'success': True,
                'id': id_pelicula,
                'nombre_pelicula': body.get('nombre_pelicula')
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)

    


    @app.route('/peliculas/<id_pelicula>', methods=['DELETE'])
    def delete_pelicula(id_pelicula):
        error_404 = False
        try:
            pelicula = Pelicula.query.filter(Pelicula.id_pelicula == id_pelicula).one_or_none()
            if pelicula is None:
                error_404 = True
                abort(404)
            eliminado = pelicula.nombre_pelicula
            pelicula.delete()

            selection = Pelicula.query.order_by('id_pelicula').all()
            peliculas = pagination_todos(request, selection, True)

            return jsonify({
                'success': True,
                'deleted': id_pelicula,
                'pelicula_eliminada': eliminado,
                'peliculas': peliculas,
                'total_peliculas': len(selection)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)


#---------------Sala---------------
    @app.route('/salas', methods=['GET'])
    def get_salas():
        selection = Sala.query.order_by('id_sala').all()
        salas = pagination_todos(request, selection, False)

        if len(salas) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'salas': salas,
            'total_salas': len(salas)
        })

    @app.route('/salas', methods=['POST'])
    def create_sala():
        body = request.get_json()
        capacidad_sala = body.get('capacidad_sala', None)
        numero_sala = body.get('numero_sala', None)

        if capacidad_sala is None or numero_sala is None:
            abort(422)

        try:
            sala = Sala(capacidad_sala=capacidad_sala, numero_sala=numero_sala)
            new_sala_id = sala.insert()

            selection = Sala.query.order_by('id_sala').all()
            salas = pagination_todos(request, selection, True)

            return jsonify({
                'success': True,
                'created': new_sala_id,
                'salas': salas,
                'total_salas': len(salas)
            })
        except Exception as e:
            print(e)
            abort(500)

    
    @app.route('/salas/<id_sala>', methods=['PATCH'])
    def update_sala(id_sala):
        error_404 = False
        try:
            sala = Sala.query.filter(Sala.id_sala == id_sala).one_or_none()
            if sala is None:
                error_404 = True
                abort(404)
            

            body = request.get_json()
            if 'capacidad_sala' in body:
                sala.capacidad_sala = body.get('capacidad_sala')

            sala.update()
            
            return jsonify({
                'success': True,
                'id_sala': id_sala
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)


    @app.route('/salas/<id_sala>', methods=['DELETE'])
    def delete_sala_by_id(id_sala):
        error_404 = False
        try:
            sala = Sala.query.filter(Sala.id_sala == id_sala).one_or_none()
            if sala is None:
                error_404 = True
                abort(404)
            eliminado = sala.id_sala
            sala.delete()

            selection = Sala.query.order_by('id_sala').all()
            salas = pagination_todos(request, selection, True)

            return jsonify({
                'success': True,
                'deleted': id_sala,
                'sala_eliminada': eliminado,
                'salas': salas,
                'total_peliculas': len(selection)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)


    #---------------Funcion---------------
    @app.route('/funciones', methods=['GET'])
    def get_funciones():
        selection = Funcion.query.order_by('id_funcion').all()
        funciones = pagination_todos(request, selection, False)

        if len(funciones) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'funciones': funciones,
            'total_funciones': len(funciones)
        })

    @app.route('/funciones', methods=['POST'])
    def create_funciones():
        body = request.get_json()
        id_funcion_sala = body.get('id_funcion_sala', None)
        id_funcion_pelicula = body.get('id_funcion_pelicula', None)
        dia = body.get('dia', None)
        hora = body.get('hora', None)
        

        if id_funcion_sala is None or id_funcion_pelicula is None or dia is None or hora is None:
            abort(422)

        try:
            funcion = Funcion(id_funcion_sala=id_funcion_sala, id_funcion_pelicula=id_funcion_pelicula, dia=dia, hora=hora)
            new_funcion_id = funcion.insert()

            selection = Funcion.query.order_by('id_funcion').all()
            funciones = pagination_todos(request, selection, True)

            return jsonify({
                'success': True,
                'created': new_funcion_id,
                'funciones': funciones,
                'total_funciones': len(funciones)
            })
        except Exception as e:
            print(e)
            abort(500)

    
    @app.route('/funciones/<id_funcion>', methods=['PATCH'])
    def update_funcion(id_funcion):
        error_404 = False
        try:
            funcion = Funcion.query.filter(Funcion.id_funcion == id_funcion).one_or_none()
            if funcion is None:
                error_404 = True
                abort(404)
            

            body = request.get_json()
            if 'dia' in body:
                funcion.dia = body.get('dia')

            funcion.update()
            
            return jsonify({
                'success': True,
                'id_funcion': id_funcion
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)


    @app.route('/funciones/<id_funcion>', methods=['DELETE'])
    def delete_funcion_by_id(id_funcion):
        error_404 = False
        try:
            funcion = Funcion.query.filter(Funcion.id_funcion == id_funcion).one_or_none()
            if funcion is None:
                error_404 = True
                abort(404)
            eliminado = funcion.id_funcion
            funcion.delete()

            selection = Funcion.query.order_by('id_funcion').all()
            funciones = pagination_todos(request, selection, True)

            return jsonify({
                'success': True,
                'deleted': id_funcion,
                'funcion_eliminada': eliminado,
                'funciones': funciones,
                'total_funciones': len(funciones)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)


    #---------------Entrada---------------
    @app.route('/entradas', methods=['GET'])
    def get_entradas():
        selection = Entrada.query.order_by('id_entrada').all()
        entradas = pagination_todos(request, selection, False)

        if len(entradas) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'entradas': entradas,
            'total_entradas': len(entradas)
        })

    @app.route('/entradas', methods=['POST'])
    def create_entrada():
        body = request.get_json()
        id_entrada_funcion = body.get('id_entrada_funcion', None)
        precio = body.get('precio', None)
        fecha = body.get('fecha', None)
        hora = body.get('hora', None)
        

        if id_entrada_funcion is None or precio is None or fecha is None or hora is None:
            abort(422)

        try:
            entrada = Entrada(id_entrada_funcion=id_entrada_funcion, precio=precio, fecha=fecha, hora=hora)
            new_entrada_id = entrada.insert()

            selection = Entrada.query.order_by('id_entrada').all()
            entradas = pagination_todos(request, selection, True)

            return jsonify({
                'success': True,
                'created': new_entrada_id,
                'entradas': entradas,
                'total_entradas': len(entradas)
            })
        except Exception as e:
            print(e)
            abort(500)

    
    @app.route('/entradas/<id_entrada>', methods=['PATCH'])
    def update_entrada(id_entrada):
        error_404 = False
        try:
            entrada = Entrada.query.filter(Entrada.id_entrada == id_entrada).one_or_none()
            if entrada is None:
                error_404 = True
                abort(404)
            

            body = request.get_json()
            if 'precio' in body:
                entrada.precio = body.get('precio')

            entrada.update()
            
            return jsonify({
                'success': True,
                'id_entrada': id_entrada
            })
        except:
            if error_404:
                abort(404)
            else:
                abort(500)


    @app.route('/entradas/<id_entrada>', methods=['DELETE'])
    def delete_entrada_by_id(id_entrada):
        error_404 = False
        try:
            entrada = Entrada.query.filter(Entrada.id_entrada == id_entrada).one_or_none()
            if entrada is None:
                error_404 = True
                abort(404)
            eliminado = entrada.id_entrada
            entrada.delete()

            selection = Entrada.query.order_by('id_entrada').all()
            entradas = pagination_todos(request, selection, True)

            return jsonify({
                'success': True,
                'deleted': id_entrada,
                'entrada_eliminada': eliminado,
                'entradas': entradas,
                'total_entradas': len(entradas)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    






    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'internal server error'
        }), 500


    @app.errorhandler(405)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 405,
            'message': 'method not allowed'
        }), 405


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'code': 422,
            'message': 'unprocessable'
        }), 422

    return app

