import json

data = {"message": "hello"}

with open("test.json", "w") as json_file:
    json.dump(data, json_file)

print("JSON file 'test.json' created successfully.")
