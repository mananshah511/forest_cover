from flask import request,render_template,Flask
from flask_cors import cross_origin,CORS
import os,sys,json
from forest.loggers import logging
from forest.exception import ForestException
from forest.pipeline.pipeline import Pipeline
from forest.entity.artifact_entity import FinalArtifact
from forest.constant import COLUMN,DROP_COLUMN_LIST,TARGET_CLASS_LIST
import pandas as pd
import numpy as np
from forest.util.util import load_object

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

@app.route('/predict',methods=['POST'])
@cross_origin()
def predict():
    
    data = [int(x) for x in request.form.values()]
    if not os.path.exists('data.json'):
        return render_template('index.html',output_text = "No model is trained, please start training")
    
    with open('data.json', 'r') as json_file:
        dict_data = json.loads(json_file.read())

    final_artifact = FinalArtifact(**dict_data)

    wilderness_index = data[7]
    soil_index = data[8]
    data.pop(-1)
    data.pop(-1)

    for i in range(4):
        if i == (wilderness_index-1):
            data.append(1)
        else:
            data.append(0)

    for i in range(40):
        if i == (soil_index-1):
            data.append(1)
        else:
            data.append(0) 
    logging.info(f"final artifact : {final_artifact}")

    df = pd.DataFrame(data).T
    df.columns = COLUMN[:-1]
    df = df.drop(DROP_COLUMN_LIST,axis=1)



    preproceesed_object = load_object(file_path=final_artifact.preprocessed_model_path)
    df = preproceesed_object.transform(np.array(df).reshape(1,-1))
    

    cluster_object = load_object(file_path=final_artifact.cluster_model_path)
    cluster_number = int(cluster_object.predict(df))

    model_object = load_object(file_path=final_artifact.export_dir_path[cluster_number])
    output = int(model_object.predict(df))
    
    return render_template('index.html',output_text = "Forest covertype of given data is "+TARGET_CLASS_LIST[output-1])
if __name__ == "__main__":
    app.run()