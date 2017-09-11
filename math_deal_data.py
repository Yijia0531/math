#-*-coding: utf-8-*-
import re

def read_file(filename, qfile, afile):
    qs_pattern = r"<questions>"
    qs_pattern2 = r"<questions id=\"(.+?)\""
    q_pattern = r"<question id=\"(.+?)\""
    ty_pattern = r"type=\"(.+?)\">"

    id_count = 0
    questions_text = []
    answers_text = []
    question_text = []
    question = ""
    answer = ""

    question_file = open(qfile, "w", encoding="UTF-8")
    answer_file = open(afile, "w", encoding="UTF-8")

    with open(filename, "r", encoding="UTF-8") as f:
        q_start = False
        a_start = False
        q_type = ""
        line_count = 0
        for line in f:

            line_count += 1
            if line_count % 100 ==0:
                print("data deal "+ str(line_count))

            line = line.strip()
            if len(re.findall(qs_pattern, line)) != 0 or len(re.findall(qs_pattern2, line)) != 0:
                if not q_start and not a_start:
                    q_type = "questions"
                    if id_count % 2 == 0:
                        q_start = True
                        id_count += 1
                    else:
                        id_count += 1
                        a_start = True

            if len(re.findall(q_pattern, line)) != 0:
                if not q_start and not a_start:
                    q_type = re.findall(ty_pattern, line)
                    if id_count % 2 == 0:
                        q_start = True
                        id_count += 1
                    else:
                        a_start = True
                        id_count += 1

            if q_start and not a_start:
                question = question + line.strip()
                question_text.extend(xml_parser(line.strip(), "question"))
                if len(re.findall("</question>", line)) != 0 and q_type is not "questions" or len(re.findall("</questions>", line)) != 0:
                    question_file.write(question + "\n")
                    questions_text.append(question_text)
                    question = ""
                    question_text = []
                    q_start = False
            elif a_start and not q_start:
                answer = answer + line.strip()
                if len(re.findall("</question>", line)) != 0 and q_type is not "questions" or len(re.findall("</questions>", line)) != 0:
                    answer_file.write(answer + "\n")
                    answers_text.append(xml_parser(answer, "answer"))
                    answer = ""
                    a_start = False
    question_file.close()
    answer_file.close()
    return questions_text,answers_text

def xml_parser(sentence, flag):

    qa_pattern = r"<text format=\"latex\">(.+?)</text>"
    qa_pattern2 = r"<text format=\"latex,html\">(.+?)</text>"
    qa_pattern1 = r"<text>(.+?)</text>"
    bl_pattern = r"<blank num=\"[0-9]\" format=\"latex\">(.+?)</blank>"
    bl_pattern1 = r"<blank format=\"latex\" num=\"[0-9]\">(.+?)</blank>"
    bl_pattern2 = r"<blank format=\"latex,html\" num=\"[0-9]\">(.+?)</blank>"
    st_pattern = r"<stem>(.+?)</stem>"
    ch_pattern = r"<choice id=\"[0-9]\">(.+?)</choice>"
    se_pattern = r"<option value=\"[A|B|C|D]\">(.+?)</option>"
    an_pattern = r"<logic>(.+?)</logic>"
    an_se_pattern = r"<Sentence>(.+?)</Sentence>"
    an_sel_pattern = r"<select format=\"latex\" multiple=\"false\">(.+?)</select>"

    question = []
    answer = []
    if flag == "question":
        if len(re.findall(qa_pattern, sentence)) != 0:
            question.extend(re.findall(qa_pattern, sentence))
        elif len(re.findall(qa_pattern1, sentence)) != 0:
            question.extend(re.findall(qa_pattern1, sentence))
        elif len(re.findall(qa_pattern2, sentence)) != 0:
            question.extend(re.findall(qa_pattern2, sentence))
        elif len(re.findall(bl_pattern, sentence)) != 0:
            question.extend(re.findall(bl_pattern, sentence))
        elif len(re.findall(bl_pattern1, sentence)) != 0:
            question.extend(re.findall(bl_pattern1, sentence))
        elif len(re.findall(bl_pattern2, sentence)) != 0:
            question.extend(re.findall(bl_pattern2, sentence))
        elif len(re.findall(st_pattern, sentence)) != 0:
            question.extend(re.findall(st_pattern, sentence))
        elif len(re.findall(se_pattern, sentence)) != 0:
            question.extend(re.findall(se_pattern, sentence))
        elif len(re.findall(ch_pattern, sentence)) != 0:
            question.extend(re.findall(ch_pattern, sentence))
        re_question = []
        for que in question:
            re_question.extend(split_question(que))
        return re_question
    else:
        option = ""
        if len(re.findall(an_sel_pattern, sentence)) != 0:
            option = re.findall(an_sel_pattern, sentence)[0]
            index = sentence.find(option)
            sentence = sentence[0:index] + sentence[index+len(option):len(sentence)]
        an_se = re.findall(an_se_pattern, sentence)
        for an in an_se:
            answer.append(re.findall(an_pattern, an))
        if len(re.findall(se_pattern, option)) != 0:
            op_str = re.findall(se_pattern, option)
            for op in op_str:
                if len(re.findall(an_pattern, op)) != 0:
                    answer.append(re.findall(an_pattern, op))
                else:
                    an = []
                    an.append(op)
                    answer.append(an)
        return answer

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
    p_pattern = "<Picread.+?>.{0,1000}</Picread>"
    if re.search(p_pattern, sentence) is not None:
        s = re.split(p_pattern, sentence)
        for i in s:
            se+=i
    else:
        se = sentence
    return se

def split_question(sentence):
    '''split question sentence

    args: ex 已知函数$f(x)=log_a{\frac{1-mx}{x-1}}(a\textgreater 1)$是奇函数
    return: ["已知函数$f(x)=log_a{\frac{1-mx}{x-1}}$是奇函数",["a\textgreater 1"]]
    # '''
    
    sentence = delectGraph(sentence)
    sentence = charReplace(sentence)

    split_results = []
    common_pattern = "\\$(.+)\\$"
    pattern = "\\$[^\\$]+(\\([^\\$]+\\))\\$"
    # point_pattern = "[A-Z]\\(.+,.+\\)"
    # judge_pattern = "[a-zA-Z0-9+-]+$"
    # judge_pattern1 = "[a-zA-Z0-9+-]+,+[a-zA-Z0-9+-]+$"

    judge_pattern = ".+(textgreater|in|forall|textless|neq|leq|le|geq|ge).+"

    first_strs = []
    last_strs = []
    temp_sentence = sentence
    dic = {}
    while re.search(pattern, temp_sentence) is not None:
        all_str = re.findall(common_pattern, temp_sentence)[0]
        last_str = re.findall(pattern,temp_sentence)[0]
        if last_str not in dic:
            dic[last_str] = 1
        else:
            dic[last_str] += 1
        index = sentence.find(last_str, dic[last_str])
        # if re.match(point_pattern, all_str) is None and re.match(judge_pattern, last_str[1:len(last_str)-1]) is None and re.match(judge_pattern1, last_str[1:len(last_str)-1]) is None:
        #     s1 = sentence[0:index]
        #     s1 = s1 + sentence[index+len(last_str):len(sentence)]
        #     sentence = s1
        #     last_strs.append("$" + last_str[1:len(last_str)-1] + "$")
        if re.match(judge_pattern, last_str[1:len(last_str)-1]) is not None:
            s1 = sentence[0:index]
            s1 = s1 + sentence[index+len(last_str):len(sentence)]
            sentence = s1
            last_strs.append("$" + last_str[1:len(last_str)-1] + "$")
        temp_sentence = sentence[index+len(last_str):len(sentence)]

    bracket_count = 0
    _count = 0
    index = 0
    for i in range(len(sentence)):
        if sentence[i] == "$":
            _count += 1
        elif sentence[i] == "(" or sentence[i] == "[":
            bracket_count += 1
        elif sentence[i] == ")" or sentence[i] == "]":
            bracket_count -= 1
        elif sentence[i] == "," and bracket_count <=0:
            if _count%2 == 0:
                s = sentence[index:i]
                first_strs.append(s)
                index = i+1
            else:
                s = sentence[index:i] + "$"
                first_strs.append(s)
                temp_str = sentence[0:i+1]
                temp_str += "$" + sentence[i+1:len(sentence)]
                sentence = temp_str
                _count -= 1
                index = i+1
    first_strs.append(sentence[index:len(sentence)])

    split_results.extend(first_strs)
    split_results.extend(last_strs)
    return(split_results)


# print(split_question("在平面直角坐标系$xOy$中,点$A(\cos\\theta,sqrt{2}\sin\\theta),B(\sin\\theta,0)$,其中he$\\tta\in R$."))
# questions_text,answers_text = read_file("correct.txt", "question", "answer")
# print(questions_text)
# print(answers_text)
# for question in questions_text:
#     print(question)
# count = 1
# for answer in answers_text:
#      print(count)
#      print(answer)
#      count +=1
# print(questions_text)a
# print(split_question("已知函数$f(x)=log_a{\\frac{1-mx}{x-1}}(\\tta\in R)$是奇函数"))