import urllib.request
import json
from requests.auth import HTTPBasicAuth

url='https://optimize-service.eastus.inference.ml.azure.com/score'
data = {'location':'eastus'}
body = str.encode(json.dumps(data))
headers = {'Accept': 'application/json'}
api_key = 'AuMWcf1s2D2pYfmjCdC92OdyRdfQIxDR'
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'default' }
req = urllib.request.Request(url, body, headers)
response = urllib.request.urlopen(req)
print(response.read())

