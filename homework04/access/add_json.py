import json

data = {
    "access_token": "067adb7c9b89873d90b98134d75bebf359b256e64771d62eb31dfdb6187d97c60834b47a3d9b5ab678ea9"
}
with open("config.json", "w") as write_file:
    json.dump(data, write_file)