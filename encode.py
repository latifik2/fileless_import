import sys
import base64

if len(sys.argv) < 2:
    print("Error! Not enough arguments")
    exit(1)

filename = sys.argv[1]
encoded_data = None

with open(filename, mode='r') as file:
    text = file.read()
    encoded_data = base64.b64encode(text.encode())

print(encoded_data.decode())
