# -*- coding: UTF-8 -*-
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

class LatexWord:
    word_name = ""
    logic_name = ""
    def __init__(self, word_name, logic_name):
        self.word_name = word_name
        self.logic_name = logic_name

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

def read_latex_parser_file(filename):
    latex_word = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            s = line.split("\t")
            latex_word.append(LatexWord(s[0], s[1]))
    return latex_word

def parser_latex(sentence, latex_word):
    pattern = "\\$.+\\$"
    parser_result = []
    if re.match(pattern, sentence) is not None:
        sentence = sentence[1:len(sentence)-1]
        for word in latex_word:
            index1 = 0
            str_temp = sentence
            s1 = ""
            while str_temp.find(word.word_name) != -1:
                index2 = index1 + str_temp.find(word.word_name)
                s1 += sentence[index1:index2]
                s1 += " " + word.logic_name + " "
                index1 = index2+len(word.word_name)
                str_temp = str_temp[index1:len(str_temp)]
            sentence = s1 + sentence[index1:len(sentence)]
    sentence = sentence.strip()
    parser_result = sentence.split(" ")
    return parser_result


def parser(sentence, words_all, latex_words):
    sentenceElements = []
    flag = True
    while len(sentence) > 0:
        for i, word in enumerate(words_all):
            if re.match(word.word_name, sentence) is not None:
                elements = re.match(word.word_name, sentence).group()
                if re.match("\\$.+\\$", elements) is not None:
                    sentenceElements.extend(parser_latex(elements, latex_words))
                else:
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

def read_language_translate(filename):
    C_E_dic = {}
    pattern = "#.*#"
    with open(filename, "r", encoding="UTF-8") as f:
        for line in f:
            line = line.strip()
            if re.match(pattern, line) is None:
                s = line.split("\t")
                C_E_dic[s[0]] = s[1]
    return C_E_dic

# C_E_dic = read_language_translate("C:\\Users\\zhaoyijia\\Desktop\\codding\\LatexWord\\LanguageTranslator.txt")
# def main():
#     words_all = parserAllFile("C:\\Users\\zhaoyijia\\Desktop\\codding\\WordType")
#     # print(len(words_all))
#     words_all = sorted(words_all, key=attrgetter("word_weight"), reverse=True)
#     latex_words = read_latex_parser_file("C:\\Users\\zhaoyijia\\Desktop\\codding\\LatexWord\\LatexParser.txt")
#     sentence = "在等差数列$\\{a_{n}\\}$中,$a_{1}+a_{9}=10$,则$a_{5}$的值为______"
#     print(parser(sentence, words_all, latex_words))

# main()

