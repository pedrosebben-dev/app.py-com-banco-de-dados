from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin # type: ignore
from database import db
from flask_login import LoginManager, login_user, current_user
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
db = SQLAlchemy()
#view login
login_manager.login_view = 'login'
#Session <- conexão ativa


class User(db.Model, UserMixin):
    # id (inteiro), username (texto) , senha (texto)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
   # Login
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
      login_user(user)
      print(current_user.is_authenticated)
      return jsonify({"message": "Autenticação realizada com sucesso!"})

  return jsonify({"message": "Credenciais inválidas"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logout realizado com sucesso!"})


@app.route('/user', methods=["POST"])
def create_user():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuario cadastrado com sucesso"})
  return jsonify({"message": "Dados invalidos"}), 400

@app.route('/user/<int:id_user>', methods=['GET'])
def read_user(id_user):
  data = request.json
  user= User.query.get(id_user)

  if user and data.get("password"):
    user.username = data.get("password")
    
    return jsonify({"Message": f"Usuario {id_user} atualizado com sucesso!"})
  
  return jsonify({"Message": "Usuario não encontrado"})

@app.route("/hello-world", methods=["GET"])
def hello_world():
  return "Hello world"

if __name__ == "__main__":
  app.run(debug=True)