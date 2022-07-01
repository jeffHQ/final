from flask_sqlalchemy import SQLAlchemy

database_name = 'peliculasdb'
database_path = 'postgresql://{}:{}@localhost:{}/{}'.format('postgres', 'Magdalena150', 5432,database_name)
#'postgresql+psycopg2://postgres@localhost:5432/todoapp20db'
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()





class Pelicula(db.Model):
    __tablename__ = 'peliculas'
    id_pelicula = db.Column(db.Integer, primary_key=True)
    #id = db.Column(db.Integer, primary_key=True)
    nombre_pelicula = db.Column(db.String, nullable=False)
    duracion_pelicula = db.Column(db.Integer, nullable=False)
    calificacion_pelicula = db.Column(db.Integer, nullable=False)
    idioma_pelicula = db.Column(db.String, nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id_pelicula
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def format(self):
        return {
            'id_pelicula': self.id_pelicula,'nombre_pelicula': self.nombre_pelicula,'duracion_pelicula': self.duracion_pelicula,'calificacion_pelicula': self.calificacion_pelicula,'idioma_pelicula': self.idioma_pelicula
        }

    def __repr__(self):
        return f'Pelicula: id_pelicula={self.id_pelicula}, nombre_pelicula={self.nombre_pelicula}, duracion_pelicula={self.duracion_pelicula},calificacion_pelicula={self.calificacion_pelicula},idioma_pelicula={self.idioma_pelicula}'

class Sala(db.Model):
    __tablename__ = 'salas'
    id_sala = db.Column(db.Integer, primary_key=True)
    capacidad_sala = db.Column(db.Integer, nullable=False)
    numero_sala = db.Column(db.Integer, nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id_sala
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def format(self):
        return {
            'id_sala': self.id_sala,'capacidad_sala': self.capacidad_sala,'numero_sala': self.numero_sala
        }


    def __repr__(self):
        return f'Sala: id_sala={self.id_sala}, capacidad_sala={self.capacidad_sala}, numero_sala={self.numero_sala}'

class Funcion(db.Model):
    __tablename__ = 'funciones'
    id_funcion = db.Column(db.Integer, primary_key=True)

    id_funcion_sala = db.Column(db.Integer, db.ForeignKey('salas.id_sala'))
    salas = db.relationship("Sala")

    id_funcion_pelicula = db.Column(db.Integer, db.ForeignKey('peliculas.id_pelicula'))
    peliculas = db.relationship("Pelicula")

    dia = db.Column(db.Integer, nullable=False)
    hora = db.Column(db.Integer, nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id_funcion
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def format(self):
        return {
            'id_funcion': self.id_funcion,'id_funcion_sala': self.id_funcion_sala,'id_funcion_pelicula': self.id_funcion_pelicula,'dia': self.dia,'hora': self.hora
        }

    def __repr__(self):
        return f'Funcion: id_funcion={self.id_funcion}, id_funcion_sala={self.id_funcion_sala}, id_funcion_pelicula={self.id_funcion_pelicula},dia={self.dia},hora={self.hora}'

    


class Entrada(db.Model):
    __tablename__ = 'entradas'
    id_entrada = db.Column(db.Integer, primary_key=True)

    id_entrada_funcion = db.Column(db.Integer, db.ForeignKey('funciones.id_funcion'))
    funciones = db.relationship("Funcion")

    precio = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.String, nullable=False)
    hora = db.Column(db.Integer, nullable=False)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id_entrada
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()


    def format(self):
        return {
            'id_entrada': self.id_entrada,'id_entrada_funcion': self.id_entrada_funcion,'precio': self.precio,'fecha': self.fecha,'hora': self.hora
        }

    def __repr__(self):
        return f'Funcion: id_entrada={self.id_entrada}, id_entrada_funcion={self.id_entrada_funcion}, precio={self.precio},fecha={self.fecha},hora={self.hora}'



