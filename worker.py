from flask import Flask
from flask import request
from google.cloud import secretmanager
import requests
import os
import json
app = Flask(__name__)

def get_api_key() -> str:
    client = secretmanager.SecretManagerServiceClient()
    secret_version_name = "projects/737526740663/secrets/compute-api-key/versions/3"
    try:
        # Access the secret version
        response = client.access_secret_version(request={"name":secret_version_name})

        # Extract the secret value
        secret_value = response.payload.data.decode("UTF-8")

        return secret_value
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None
      
@app.route("/")
def hello():
    return "Add workers to the Spark cluster with a POST request to add"

@app.route("/test")
def test():
    #return "Test" # testing 
    return(get_api_key())

@app.route("/add",methods=['GET','POST'])
def add():
  if request.method=='GET':
    return "Use post to add" # replace with form template
  else:
    token=get_api_key()
    ret = addWorker(token,request.form['num'])
    return ret


def addWorker(token, num):
    with open('payload.json') as p:
      tdata=json.load(p)
    tdata['name']='slave'+str(num)
    data=json.dumps(tdata)
    url='https://www.googleapis.com/compute/v1/projects/elaborate-scope-401116/zones/europe-west1-b/instances'
    headers={"Authorization": "Bearer "+token}
    resp=requests.post(url,headers=headers, data=data)
    if resp.status_code==200:     
      return "Done"
    else:
      print(resp.content)
      return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
