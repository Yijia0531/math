import json
import importlib
import sys
import os
importlib.reload(sys)

def get_data(data_file, sorce_file, target_file):
    fp = open(data_file, "r", encoding="UTF-8")
    datas = json.load(fp)

    for data in datas:
        if data["correct"] != "Error":
            if len(data["mapping_text"]) == len(data["mapping_equations"]):
                for i in data["mapping_text"]:
                    si = i.replace("\n", "")
                    si = si.replace("\r", "")
                    sorce_file.write(si+"\n")
                for j in data["mapping_equations"]:
                    sj = j.replace("\n", "")
                    sj = sj.replace("\r", "")
                    sj = sj.replace(" ", "")
                    target_file.write(sj+"\n")

def eachFile(filepath, sorce_file, target_file):
    pathDir = os.listdir(filepath)
    for s in pathDir:
        newDir = os.path.join(filepath, s)
        if os.path.isfile(newDir):
            print(newDir)
            get_data(newDir, sorce_file, target_file)
        else:
            eachFile(newDir, sorce_file, target_file)

def main():
    sf = open("train.source", "w", encoding="UTF-8")
    tf = open("train.target", "w", encoding="UTF-8")
    eachFile("G:\\math\\codding\\data\\train", sf, tf)
    sf1 = open("dev.source", "w", encoding="UTF-8")
    tf1 = open("dev.target", "w", encoding="UTF-8")
    eachFile("G:\\math\\codding\\data\\test", sf1, tf1)

def text():
    texts = []
    with open("train_templates.target", "r", encoding="UTF-8") as f:
        for line in f:
            line = line.strip()
            line = line.replace(",", " , ")
            texts.append(line)
    with open("train_templates1.target", "w", encoding="UTF-8") as f:
        for line in texts:
            f.write(line+"\n")

text()
# main()





