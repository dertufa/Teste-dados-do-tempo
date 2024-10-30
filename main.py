from flask import Flask
  # Importa as rotas definidas em views.py

app = Flask(__name__)
from views import *
if __name__ == "__main__":
    app.run(debug=True)  # Ativa o modo debug para ajudar a identificar erros
