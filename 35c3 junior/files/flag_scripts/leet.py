import requests

host = "http://35.207.132.47/wee/run"
leet = str(int("0x1337", 16))

check = {"code": "alert(assert_leet("+leet+"))"}
flag_request = requests.post(host, json=check)
flag = flag_request.json()["result"].strip()
print(flag)
