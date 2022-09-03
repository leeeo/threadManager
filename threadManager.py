import requests
import json


if __name__ == '__main__':
    URL = "https://eai.mrcamel.co.kr/devops"

    response = requests.post(URL)
    params = json.loads(response.text)
    print(params['body']['value'])
    
