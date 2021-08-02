import os
from flask import (
    Flask,
    request,
    jsonify)
import pickle
from flask_basicauth import BasicAuth
from flask.wrappers import Request
from textblob import TextBlob
from dotenv import (
    load_dotenv, find_dotenv)


columns = ['tamanho', 'ano', 'garagem']

model = pickle.load(open('../../models/model.sav', 'rb'))

app = Flask(__name__)


app.config['BASIC_AUTH_USERNAME'] = os.environ.get("BASIC_AUTH_USERNAME")
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get("BASIC_AUTH_PASSWORD")
app.config['BASIC_AUTH_FORCE'] = True
auth = BasicAuth(app)

@app.route('/')
@auth.required
def home():
    """Rota de home"""
    return "hello word"


@app.route('/sentimento/<frase>/')
def sentiment(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')
    polaridade = tb_en.sentiment.polarity
    return f'Polaridade: {polaridade}'


@app.route('/cotacao/', methods=['POST'])
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in columns]
    preco = model.predict([dados_input])
    return jsonify(preco=preco[0])


if __name__ == '__main__':

    app.run(
        debug=True, 
        port=5000,
        host='0.0.0.0'
    )
