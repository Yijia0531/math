import json
import importlib
import sys
importlib.reload(sys)

def select_data(data_file, right_file, wrong_file):
    fp = open(data_file, 'r', encoding='UTF-8')
    datas = json.load(fp)
    right_subset = []
    wrong_subset = []

    for data in datas:
        print(data["id"])
        if data["correct"] != "Error" and data["correct"] != "error":
            if len(data["mapping_text"]) == len(data["mapping_equations"]):
                right_subset.append(data)
            else:
                wrong_subset.append(data)
    with open(right_file, 'w', encoding='UTF-8') as json_file:
        json.dump(right_subset, json_file, indent=2, ensure_ascii=False)
        print(len(right_subset))
    with open(wrong_file, 'w', encoding='UTF-8') as json_file:
        json.dump(wrong_subset, json_file, indent=2, ensure_ascii=False)
        print(len(wrong_subset))

select_data("marked_data.json", "right(marked_data).json", "wrong(marked_data).json")
