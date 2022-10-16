import json
import numpy as np
import requests

def init():
    print('Inside init')
 

def run(request):
    print(request)
    #text = json.loads(request)
    
    # Run inference
    print('inside_request')
    url = 'https://carbon-aware-api.azurewebsites.net/emissions/forecasts/current?location=eastus'
    result = webservice(url)
    return result


def webservice(url):
    response =requests.get(url)
    fjson=json.loads(response.text)
    data_file = json.dumps(fjson[0])
    result=json.loads(data_file)['forecastData']
    return str.encode(json.dumps(result))

if __name__ == "__main__":
    init()
    response_api = run('url')
    response_api[0]
    print(response_api[0])
    	

