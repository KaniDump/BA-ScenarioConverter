import json

def read_excelt_json(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as infile:
        return json.load(infile)

def write_excelt_json(file_path: str, data: dict):
    with open(file_path, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)

def read_exceltable_json(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)
        return data.get("DataList", [])

def write_exceltable_json(file_path: str, data: list):
    datalist = {"DataList": data}
    with open(file_path, "w", encoding="utf-8") as outfile:
        json.dump(datalist, outfile, ensure_ascii=False, indent=2)