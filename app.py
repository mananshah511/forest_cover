from flask import request,render_template,Flask
from flask_cors import cross_origin,CORS
import os,sys,json
from forest.loggers import logging
from forest.exception import ForestException
from forest.pipeline.pipeline import Pipeline

app = Flask(__name__)

@app.route('/',methods=['GET'])
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route('/train',methods=['POST'])
@cross_origin()
def train():
    pipeline = Pipeline()
    pipeline.run_pipeline()
    return render_template('index.html',prediction_text = "Model training completed")

if __name__ == "__main__":
    app.run()