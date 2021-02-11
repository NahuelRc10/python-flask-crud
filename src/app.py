from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/adminproyectos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    genero = db.Column(db.String(1))
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(255))
    telefono = db.Column(db.String(25))
    id_rol = db.Column(db.Integer)

    def __init__(self, id, nombre, apellido, genero, email, password, telefono, id_rol):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.genero = genero
        self.email = email
        self.password = password
        self.telefono = telefono
        self.id_rol = id_rol

db.create_all()
class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'apellido', 'genero', 'email', 'password', 'telefono', 'id_rol')

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many = True)

@app.route('/usuarios', methods = ['POST'])
def create_usuario():
    print(request.json)
    nombre = request.json['nombre']
    apellido = request.json['apellido']
    genero = request.json['genero']
    email = request.json['email']
    password = request.json['password']
    telefono = request.json['telefono']
    id_rol = request.json['id_rol']
    new_usuario = Usuario(None, nombre, apellido, genero, email, password, telefono, id_rol)
    db.session.add(new_usuario)
    db.session.commit()
    return usuario_schema.jsonify(new_usuario), 201

@app.route('/usuarios', methods = ['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    result = usuarios_schema.dump(usuarios)
    return jsonify(result), 200

@app.route('/usuarios/<id>', methods = ['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    return usuario_schema.jsonify(usuario), 200

@app.route('/usuarios/<id>', methods = ['PUT'])
def update_usuario(id):
    usuario_db = Usuario.query.get(id)
    telefono = request.json['telefono']

    usuario_db.telefono = telefono

    db.session.commit()
    return usuario_schema.jsonify(usuario_db), 201

@app.route('/usuarios/<id>', methods = ['DELETE'])
def delete_usuario(id):
    usuario_db = Usuario.query.get(id)
    db.session.delete(usuario_db)
    db.session.commit()
    return usuario_schema.jsonify(usuario_db), 200

@app.route('/', methods = ['GET'])
def index():
    return jsonify(({'message': 'API PYTHON - FLASK / CRUD'}))

if __name__ == "__main__":
    app.run(debug = True)