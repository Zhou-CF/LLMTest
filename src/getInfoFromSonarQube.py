import requests
from requests.auth import HTTPBasicAuth
import json

# 目标URL
url = 'http://192.168.6.128:9000/'
auth = HTTPBasicAuth("squ_a53c076582b68036437787d98f8fc85c6f5955e3", '')

def search(project, p=1):
    response = requests.get(url+f'api/hotspots/search?project={project}&p={p}', auth=auth)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print('请求失败，状态码：', response.status_code)
        return {'hotspots':[]}
    

def show(key):
    response = requests.get(url+f'api/hotspots/show?hotspot={key}', auth=auth)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        print('请求失败，状态码：', response.status_code)
        return 

