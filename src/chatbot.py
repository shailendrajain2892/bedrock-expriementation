import sys
import boto3
from pprint import pprint
import json

history=[]

brclient = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def get_foundation_models():
    brclient = boto3.client('bedrock')
    models  = brclient.list_foundation_models()
    return [model.get('modelId') for model in models.get('modelSummaries')]
    # pprint(models)

def get_foundation_model_by_id(id):
    return brclient.get_foundation_model(modelIdentifier=id)

def select_model():
    models = get_foundation_models()

    print("Choose one of the following options:")
    for index, option in enumerate(models, start=1):
        print(f"{index}. {option}")
    while True:
        choice = input("Enter your choice from these list: ")
        if choice.isdigit():  # Check if input is a digit
            choice = int(choice)
            if 1 <= choice <= len(models):  # Check if input is within the range of options
                selected_option = models[choice - 1]
                print(f"You have selected: {selected_option}")
                break    
        print("enter valid choice")
    return selected_option

def get_history():
    return "\n".join(history)


def predict_response(modelid, brclient):
    print(f"prediction for model : {modelid}")
    while True:
        prompt = input("User:")
        history.append(prompt)
        if prompt == "exit":
            break
        titan_config = json.dumps({
                "inputText": get_history(),
                "textGenerationConfig": {
                    "maxTokenCount": 4096,
                    "stopSequences": [],
                    "temperature": 0,
                    "topP": 1
                }
            })
        response = brclient.invoke_model(body=titan_config, 
                            modelId=modelid,
                            accept='application/json',
                            contentType='application/json')
        response_body = json.loads(response.get('body').read()).get("results")[0].get('outputText').strip()
        print(f"A: {response_body}")
        history.append(response_body)

modelid = select_model()
predict_response(modelid, brclient)