import os
import re

from operator import attrgetter

class Word:
    word_name = ""
    word_length = 0
    word_weight = 0
    word_type = ""

    def __init__(self, name, length, weight, type):
        self.word_name = name
        self.word_length = length
        self.word_weight = weight
        self.word_type = type

class Logic:
    

def parserFile(filename, wordtype):
    words = []
    with open(filename, "r", encoding="UTF-8") as f:
        for line in f:
            line = line.strip()
            s = line.split("\t")
            word = Word(s[0], s[1], s[2], wordtype)
            words.append(word)
    return words


def parserAllFile(filepath):
    words_all = []
    pathDir = os.listdir(filepath)
    for s in pathDir:
        newDir = os.path.join(filepath, s)
        if os.path.isfile(newDir):
            words = parserFile(newDir, s)
            words_all += words
    return words_all

def charReplace(s):
    s = s.replace("，", ",")
    s = s.replace("（", "(")
    s = s.replace("）", ")")
    s = s.replace("｛", "{")
    s = s.replace("｝", "}")
    s = s.replace("“", "\"")
    s = s.replace("”", "\"")
    s = s.replace("？", "?")
    s = s.replace("：", ":")
    s = s.replace("；", ";")
    s = s.replace("！", "!")
    s = s.replace(" ", "")
    s = s.replace("$$", "$")
    s = s.replace("\n", "")
    s = s.replace("\t", "");
    s = s.replace("\r", "")
    return s

def delectGraph(sentence):
    se = ""
    p_pattern = r"<Picread.+?>.{0,1000}</Picread>"
    if re.search(p_pattern, sentence) is not None:
        s = re.split(p_pattern, sentence)
        for i in s:
            se+=i
    return se

def parser(sentence, words_all):
    sentenceElements = []
    flag = True
    while len(sentence) > 0:
        for i, word in enumerate(words_all):
            if re.match(word.word_name, sentence) is not None:
                elements = re.match(word.word_name, sentence).group()
                sentenceElements.append(elements)
                sentence = sentence[len(elements):len(sentence)]
                break
            elif i == len(words_all)-1:
                flag = False
        if not flag:
            flag = True
            if len(sentence) > 0:
                sentenceElements.append(sentence[0])
            if len(sentence) > 1:
                sentence = sentence[1:len(sentence) - 1]
            else:
                sentence = ""
     # 对填空题和选择题的填框变成？号
    result = []
    for elements in sentenceElements:
        pattern = "[\\(（]\\s{0,20}[\\)）]|_{1,20}"
        count = 1
        if re.match(pattern, elements) is not None:
            result.append("?" + str(count))
            count += 1
        else:
            result.append(elements)
    return result

def main():
    words_all = parserAllFile("F:\\work_p\\math-subject-analysis\\Demo\\external_file\\WordType")
    words_all = sorted(words_all, key=attrgetter("word_weight"), reverse=True)
    sentence = "设$F_1$,$F_2$分别为椭圆$C:\\frac{x^2}{a^2}+\\frac{y^2}{b^2}=1(a>b>0)$的左、右焦点，过$F_2$的直线l与椭圆C相交于A,B两点"
    sentence = charReplace(sentence)
    delectGraph(sentence)
    # if re.match("异面直线", sentence) is not None:
    #     print(re.match("异面直线", sentence).group())
    print(parser(sentence, words_all))

main()
# parser("证明：DE为异面直线$AB_1$与CD的公垂线")
# words_all = []
# words_all = parserAllFile("F:\\work_p\\math-subject-analysis\\Demo\\external_file\\WordType")
# words_all = sorted(words_all, key=attrgetter("word_weight"), reverse=True)
#
# for word in words_all:
#     print(word.word_name + " " + word.word_length + " " + word.word_weight + " " + word.word_type)