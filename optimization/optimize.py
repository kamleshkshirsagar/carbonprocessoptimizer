import json
import requests
import opti_model
from azureml.contrib.services.aml_request import rawhttp
from azureml.contrib.services.aml_response import AMLResponse

def init():
    print('Inside init')
 
@rawhttp
def run(request):
    """
    This function is called for every invocation of the endpoint to perform the actual scoring/prediction.
    In the example we extract the data from the json input and call the scikit-learn model's predict()
    method and return the result back
    """
    print(request)
    print("Request received")
    respHeaders = {}
    return opti_model.opti_model()
    #text = json.loads(request)
    # Test setup for responding to CORS preflight.
    # if request.method == 'OPTIONS':
    #     respHeaders['Access-Control-Allow-Origin'] = "*"
    #     respHeaders["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    #     respHeaders['Access-Control-Allow-Headers'] = "*"
    #     respHeaders['Access-Control-Max-Age'] = "86400"
    #     return AMLResponse("Success", 200, respHeaders)
    # elif request.method == 'GET':
    #     respHeaders['Access-Control-Allow-Origin'] = "*"
    #     respHeaders["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    #     respHeaders['Access-Control-Allow-Headers'] = "*"
    #     respHeaders['Access-Control-Max-Age'] = "86400"
    #     # Run inference
    #     print('inside_get_request')
    #     url = 'https://carbon-aware-api.azurewebsites.net/emissions/forecasts/current?location=eastus'
    #     result = webservice(url)
    #     return AMLResponse(result, 200, respHeaders)    
    # elif request.method == 'POST':
    #     respHeaders['Access-Control-Allow-Origin'] = "*"
    #     respHeaders["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    #     respHeaders['Access-Control-Allow-Headers'] = "*"
    #     respHeaders['Access-Control-Max-Age'] = "86400"
    #     # Run inference
    #     print('inside_post_request')
    #     url = 'https://carbon-aware-api.azurewebsites.net/emissions/forecasts/current?location=eastus'
    #     result = webservice(url)
    #     return AMLResponse(result, 200, respHeaders)

def webservice(url):
    response =requests.get(url)
    fjson=json.loads(response.text)
    data_file = json.dumps(fjson[0])
    result=json.loads(data_file)['forecastData']
    return str.encode(json.dumps(result))

if __name__ == "__main__":
    init()
    response_api = run('url')
    #response_api[0]
    print(response_api[0])
    	

