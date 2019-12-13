import json

data = {
    "access_token": "fd5f80e811feca5e357a2c9d7a42f1ca80c8295abed6d095885277550225a79a5111532334488b19268a4"
}
with open("config.json", "w") as write_file:
    json.dump(data, write_file)