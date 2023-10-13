from flask import request,render_template,Flask
from flask_cors import cross_origin,CORS
import os,sys,json
from forest.loggers import logging
from forest.exception import ForestException


app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def homepage():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()