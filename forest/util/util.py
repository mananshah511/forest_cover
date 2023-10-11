import os,sys,dill,yaml
from forest.exception import ForestException


def read_yaml(file_path:str):
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise ForestException(sys,e) from e
    