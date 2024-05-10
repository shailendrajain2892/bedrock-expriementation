import sys
import boto3
from pprint import pprint

brclient = boto3.client('bedrock')

def get_foundation_models():
    models  = brclient.list_foundation_models()
    pprint(models)

def get_foundation_model_by_id(id):
    return brclient.get_foundation_model(modelIdentifier=id)

pprint(get_foundation_model_by_id(sys.argv[1]))