import os
import pandas
import json

def xlsx_to_dict(file_path):
    df = pandas.read_excel(file_path)
    results = []
    for line in df.to_csv().strip().split("\n")[3:]:
        parts = line.split(",")
        date = parts[2].split('/')
        results.append({
            "url": f'https://api.opap.gr/draws/v3.0/5104/{parts[1]}',
            "draw": int(parts[1]),
            "date": {
                "day": int(date[0]),
                "month": int(date[1]),
                "year": int(date[2])
            },
            "drawn_numbers": sorted(list(map(float, parts[3:8]))),
            "joker": int(parts[8])
        })
    return results

def get_last_result(results):
    return max([draw for file in results for draw in file['data']], key=lambda x: [x['date']['year'], x['date']['month'], x['date']['day']])

# Example usage
results = [{"name": file, "data": xlsx_to_dict(file)} for file in os.listdir() if os.path.isfile(file) and file.endswith("xlsx")]
os.system("cls")
print(json.dumps(obj=get_last_result(results), indent=4))