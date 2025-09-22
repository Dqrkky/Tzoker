import os
import pandas
import json
import random

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
    return max(
        [
            draw for file in results for draw in file['data']
        ],
        key=lambda x: [
            x['date']['year'],
            x['date']['month'],
            x['date']['day']
        ]
    )

# Example usage
files = [
    {
        "name": file,
        "data": xlsx_to_dict(file)
    }
    for file in os.listdir()
    if os.path.isfile(file) and
    file.endswith("xlsx")
]

commonnumbers = {
    "drawn_numbers": {},
    "joker": {}
}
for file in files:
    for result in file["data"]:
        for drawn_number in result["drawn_numbers"]:
            if str(drawn_number) in commonnumbers["drawn_numbers"]:
                commonnumbers["drawn_numbers"][str(drawn_number)] += 1
            else:
                commonnumbers["drawn_numbers"][str(drawn_number)] = 0
        if str(["joker"]) in commonnumbers["joker"]:
            commonnumbers["joker"][str(result["joker"])] += 1
        else:
            commonnumbers["joker"][str(result["joker"])] = 1

commonnumbers["drawn_numbers"] = sorted(commonnumbers["drawn_numbers"].items(), key=lambda x: x[1], reverse=True)
commonnumbers["joker"] = sorted(commonnumbers["joker"].items(), key=lambda x: x[1], reverse=True)

# Generate combinations
ranges = [(1,10), (11,20), (21,30), (31,40), (41,45)]
total_numbers = 5
import time
while True:
    combination = []

    numbers_per_range = [total_numbers // len(ranges)] * len(ranges)
    remainder = total_numbers % len(ranges)
    for i in range(remainder):
        numbers_per_range[i] += 1

    for r, n_count in zip(ranges, numbers_per_range):
        nums_in_range = [float(num) for num, count in commonnumbers["drawn_numbers"] if r[0] <= float(num) <= r[1]]

        selected = nums_in_range[:n_count]
        while len(selected) < n_count:
            candidate = random.randint(r[0], r[1])
            if candidate not in selected:
                selected.append(candidate)

        combination.extend(selected)

    combination.sort()

    # Weighted random joker
    joker_numbers = [int(num) for num, count in commonnumbers["joker"]]
    joker_weights = [count for num, count in commonnumbers["joker"]]
    if joker_numbers:
        selected_joker = random.choices(joker_numbers, weights=joker_weights, k=1)[0]
    else:
        selected_joker = random.randint(1, 20)

    print(f"{', '.join(map(str, combination))}    {selected_joker}")
    time.sleep(3)