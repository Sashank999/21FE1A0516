import requests

REGISTER_URL = "http://20.244.56.144/test/register"

COMPANY_INFO = {
    "companyName": "Abc, Inc.",
    "ownerName": "Any Name",
    "rollNo": "21FE1A0516",
    "ownerEmail": "bandi.rao999@gmail.com",
    "accessCode": "nbYNBp"
}

r = requests.post(REGISTER_URL, json=COMPANY_INFO)
print(r.text)
print(r.json())

with open("res.txt", "a") as f:
    f.write(r.text)
