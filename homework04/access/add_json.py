import json

data = {
    "access_token": "08b500321f5559ba9d05b8ba796695021c36d4c07288c7526312dbe4a8e3e57dd6da5def2e1221d37ba80"
}
with open("config.json", "w") as write_file:
    json.dump(data, write_file)