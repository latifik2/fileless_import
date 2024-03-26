import sys

if len(sys.argv) < 3:
    print("Error! Not enough arguments")
    exit(1)

filename = sys.argv[1]
key = sys.argv[2]

with open(filename, mode='r') as file:
    text = file.read()
    key_len = len(key)

    for i in range(0, len(text), key_len):
        print(text[i:i+key_len])