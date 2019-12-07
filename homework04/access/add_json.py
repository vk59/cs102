import json

data = {
    "access_token": "35efe5dd8034ab224caa885275d5449f56827204357046b062c242616d5ac1779f2da8147882977bb1d6f"
}
with open("config.json", "w") as write_file:
    json.dump(data, write_file)