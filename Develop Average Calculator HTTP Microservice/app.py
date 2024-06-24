from flask import Flask
import requests
from datetime import datetime

AUTH_URL = "http://20.244.56.144/test/auth"

CLIENT_ID = "07231c06-43ac-43f3-8db2-e5a38a7f1d1b"
CLIENT_SECRET = "OvmEyOJjpsrBNzCo"
COMPANY_DATA = {
    "companyName": "Abc, Inc.",
    "clientID": "07231c06-43ac-43f3-8db2-e5a38a7f1d1b",
    "clientSecret": "OvmEyOJjpsrBNzCo",
    "ownerName": "Any Name",
    "ownerEmail": "bandi.rao999@gmail.com",
    "rollNo": "21FE1A0516"
}

TEST_SERVER_URL = "http://20.244.56.144/test/"

ACCESS_TOKEN = None
EXPIRES_IN = 0

WINDOW_SIZE = 10

app = Flask(__name__)


def generate_auth_token():
    global ACCESS_TOKEN
    global EXPIRES_IN

    present = datetime.now()

    if ACCESS_TOKEN != None or (datetime.fromtimestamp(EXPIRES_IN / 1000.0) > present):
        return

    r = requests.post(AUTH_URL, json=COMPANY_DATA)
    json = r.json()
    ACCESS_TOKEN = json["access_token"]
    EXPIRES_IN = int(json["expires_in"]) * 1000

    with open("auth.txt", "a") as f:
        f.write(ACCESS_TOKEN + "\n")
        f.write(str(EXPIRES_IN) + "\n")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


prevState = None
currentState = []

@app.route("/numbers/<number_type>")
def numbers(number_type):
    global prevState
    global currentState

    if number_type not in "pfer":
        return { "error": "error" }
    
    numbers = fetch_from_test_api(number_type)
    if numbers == None:
        return { "error": "error" }

    if prevState == None:
        prevState = []
        currentState = numbers[-1 * WINDOW_SIZE:]
        return { "numbers": numbers, "avg": round(sum(currentState) / len(currentState), 2), "windowPrevState": [], "windowCurrState": numbers }
    else:
        temp = prevState + numbers
        temp = temp[-1 * WINDOW_SIZE:]

        prevState = currentState
        currentState = temp
        return { "numbers": numbers, "avg": round(sum(currentState) / len(currentState), 2), "windowPrevState": prevState, "windowCurrState": currentState }



def fetch_from_test_api(number_type):
    actual_types = {
        "p": "primes",
        "f": "fibo",
        "e": "even",
        "r": "random"
    }
    type_url = TEST_SERVER_URL + "/" + actual_types[number_type]

    generate_auth_token()

    r = requests.get(type_url, headers={ 'Authorization': 'Bearer ' + ACCESS_TOKEN })

    print(r.json())

    if type(r.json()) != dict:
        return None

    return list(set(r.json()["numbers"]))
