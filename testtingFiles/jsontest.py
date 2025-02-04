import json

path = "testing.json"
dataList = {}
data = {"clientHash": "nsad983hao290jal-12", "system": {"CPU": "Ryzen 7 4800H", "GPU": "Nvidia RTX 2060"}}
dataList.update({"systemData": data})


with open(path, "w") as write_file:
    json.dump(dataList, write_file, indent=3)

