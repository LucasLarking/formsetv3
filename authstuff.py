import request
from getpass import getpass
username = input('username')
password = getpass()
auth_endpoint = "http://localhost:8000/auth/"
auth_response = request.post(auth_endpoint, json={'username' : username, 'password' : password})
print(auth_response.json())

if auth_response.status_code == 200:
    token = auth_response.jeson['token']
    headers = {
        'Authorization':f"Token {token}"
    }
    endpoint = "http://localhost:8000/surveys/"
    get_response = request.get(endpoint, headers=headers)
    print(get_response.json())