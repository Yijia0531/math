import math_deal_data
import math_sentence_parser
import math_logic_parser
import re
import string
import json
import os
from operator import attrgetter

class QA:
	question = ""
	answer = ""
	def __init__(self, question, answer):
		self.question = question
		self.answer = answer

words_all = math_sentence_parser.parserAllFile("C:\\Users\\zhaoyijia\\Desktop\\codding\\WordType")
words_all = sorted(words_all, key=attrgetter("word_weight"), reverse=True)
latex_words = math_sentence_parser.read_latex_parser_file("C:\\Users\\zhaoyijia\\Desktop\\codding\\LatexWord\\LatexParser.txt")
C_E_Dict = math_sentence_parser.read_language_translate("C:\\Users\\zhaoyijia\\Desktop\\codding\\LatexWord\\LanguageTranslator.txt")

def deal_original_file(filename,qfile,afile):
	question_texts,answer_texts = math_deal_data.read_file(filename,qfile,afile)

	questions = []
	answers = []

	if len(question_texts) == len(answer_texts):
		for i in range(len(question_texts)):
			if i%10 ==0:
				print("data parser " + str(i))

			question = question_texts[i]
			answer = answer_texts[i]

			question_sentence_text = []
			for qus in question:
				question_sentence_text.append(math_sentence_parser.parser(qus, words_all, latex_words))

			answer_logic = []
			for logic in answer:
				parser_logic = []
				for l in logic:
					parser_logic.extend(math_logic_parser.parser(l))
					parser_logic.append(";")
				answer_logic.append(parser_logic)
			answers.append(answer_logic)
			questions.append(question_sentence_text)
	return questions,answers

def C_E(question_sentence, C_E_Dict):
	question_to = []
	for word in question_sentence:
		if word in C_E_Dict:
			question_to.append(C_E_Dict[word])
		else:
			question_to.append(word)
	return question_to

def write_data(filename, question, question_to, answer):

	question_sentence_texts = []
	answer_logics = []
	if os.path.exists("question.json") and os.path.exists("answer.json"):
		fp = open("question.json", "r", encoding = "UTF-8")
		question_sentence_texts = json.load(fp)

		fp1 = open("answer.json", "r", encoding = "UTF-8")
		answer_logics = json.load(fp1)
	else:
		question_sentence_texts,answer_logics = deal_original_file(filename,"question_text","answer_text")
		with open("question.json", "w", encoding="UTF-8") as json_file:
			json.dump(question_sentence_texts, json_file, indent=2, ensure_ascii=False)
		with open("answer.json", "w", encoding="UTF-8") as json_file:
			json.dump(answer_logics, json_file, indent=2, ensure_ascii=False)
	
	question_file = open(question, "w", encoding = "UTF-8")
	question_to_file = open(question_to, "w", encoding = "UTF-8")
	answer_file = open(answer, "w", encoding = "UTF-8")

	wrong_question = open("w_question", "w", encoding="UTF-8")
	wrong_answer = open("w_answer", "w", encoding="UTF-8")

	un_count = 0
	sc_count = 0

	if len(question_sentence_texts) == len(answer_logics):
		for i in range(len(answer_logics)):
			
			question_sentence_text = question_sentence_texts[i]
			answer_logic = answer_logics[i]

			q_lines = len(question_sentence_text)
			a_lines = len(answer_logic)
			if q_lines == a_lines:
				for j in range(q_lines):
					question_file.write(" ".join(question_sentence_text[j])+"\n")
					answer_file.write(" ".join(answer_logic[j])+"\n")
					c_e_str = C_E(question_sentence_text[j], C_E_Dict)
					question_to_file.write(" ".join(c_e_str) + "\n")
			elif q_lines > a_lines:

				q_a_dict = {}
				q_a_i = 0
				
				for q_i in range(q_lines):
					c_e_str = C_E(question_sentence_text[q_i], C_E_Dict)
					q_set = set(c_e_str)
					common_count = 0
					# if q_a_i+2 >= len(answer_logic):
					# 	end_i = len(answer_logic)
					# else:
					# 	end_i = q_a_i+2
					for a_i in range(q_a_i,len(answer_logic)):

						a_logic = []

						for logic in answer_logic[a_i]:
							if re.match("\\$.+\\$", logic) is not None:
								a_logic.extend(math_sentence_parser.parser_latex(logic,latex_words))
							else:
								a_logic.append(logic)

						a_set = set(a_logic)
						if len(a_set & q_set) > common_count:
							q_a_i = a_i
							common_count = len(a_set & q_set)


					if q_a_i in q_a_dict:
						l = q_a_dict[q_a_i]
						l.append(q_i)
						q_a_dict[q_a_i] = l
					else:
						l = []
						l.append(q_i)
						q_a_dict[q_a_i] = l
				wrong_answer.write("##################################" + str(i) + "\n")
				wrong_question.write("##################################" + str(i) + "\n")
				for a_i in range(len(answer_logic)):
					wrong_answer.write(" ".join(answer_logic[a_i])+"\n")
					q_is = []
					if a_i in q_a_dict:
						q_is = q_a_dict[a_i]
					for q_i in q_is:
						wrong_question.write(" ".join(question_sentence_text[q_i]) + " ")
					wrong_question.write("\n")

			else:
				un_count += 1
				wrong_answer.write("*********************************" + str(i) + "\n")
				wrong_question.write("*********************************" + str(i) + "\n")
				for a_i in range(len(answer_logic)):
					wrong_answer.write(" ".join(answer_logic[a_i])+"\n")
					if a_i < q_lines:
						wrong_question.write(" ".join(question_sentence_text[a_i]) + "\n")
					else:
						wrong_question.write("\n")

	question_to_file.close()
	question_file.close()
	answer_file.close()
	print(un_count)


write_data("correct", "question", "question_to", "answer")
# print(math_sentence_parser.parser_latex("$-\\frac{1}{2}$", latex_words))

