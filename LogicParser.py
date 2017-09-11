# -*- coding: UTF-8 -*-
import os
import re

class Logic:
    logic_name = ""
    logic_elements = ""

    def __init__(self, name, elements):
        self.logic_name = name
        self.logic_elements = elements

Normal_lp = "[a-zA-Z0-9]+\\(.+\\)"
Inference_lp = ".+:-.+"
Demonstrate_lp = "(AlwaysRight|Demonstrate)\\((.+)\\)"
LogicRS_lp = "LogicalRelationship\\((.+)\\)"
Condition_lp = "(UnnecessaryAndSufficientCondition|NecessaryNotSufficientCondition|NecessaryAndSufficientCondition|NeitherSufficientNorNecessaryConditions)\\((.+)\\)"
Proposition_lp = "(OriginalProposition|Proposition|NegativeProposition|TrueProposition|FalseProposition|ConverseNegativeProposition|SimpleProposition)\\((.+)\\)"

def parser_basic_logic(logic_sentence):
    '''parser logic sentence

    args
       logic_sentence:logic sentence need to parser ex:ValueOfParameter(m,rs_a)

    returns
        logic ex:Class Logic(logic_name, logic_elements)
        parser_result ex :["ValueOfParameter","(","m",",","rs_a",")"]

    '''
    bracket_counts = 0
    logic_name = ""
    logic_elements = []
    parser_result = []

    if re.match(Normal_lp, logic_sentence) is not None:
        index1 = logic_sentence.find("(")
        logic_name = logic_sentence[0:index1]
        
        parser_result.append(logic_name)
        parser_result.append("(")

        for i in range(len(logic_sentence)):
            if logic_sentence[i] == "(":
                bracket_counts += 1
            if logic_sentence[i] == ")":
                bracket_counts -= 1
            if logic_sentence[i] == "," and bracket_counts <=1:
                ele = logic_sentence[index1+1:i]

                parser_result.append(ele)
                parser_result.append(",")

                index1 = i

        ele = logic_sentence[index1+1:len(logic_sentence)-1]
        parser_result.append(ele)
        parser_result.append(")")
        
    else:
        logic_name = logic_sentence
        parser_result.append(logic_name)

    return parser_result

def split_logic(logic_sentence):
    '''split logic sentence

    args
       logic_sentence:logic sentence need to split
       ex :Trapezoid(ABCD),AreaOfTrapezoid(ABCD,$12\\sqrt{2}$)

    returns
        logic list
        ex:["Trapezoid","(","ABCD",")",",","AreaOfTrapezoid","(","ABCD",",","$12\\sqrt{2}$",")"]

    '''
    bracket_counts = 0
    logics = []
    parser_result = []

    index = 0

    for i in range(len(logic_sentence)):
        if logic_sentence[i] == "(":
            bracket_counts += 1
        if logic_sentence[i] == ")":
            bracket_counts -= 1
        if logic_sentence[i] == "," and bracket_counts <=0:
            logics.append(logic_sentence[index:i])
            index = i+1
    logics.append(logic_sentence[index:len(logic_sentence)])

    length = len(logics)
    count = 0

    for logic in logics:
    	count+=1
    	if re.match(Inference_lp, logic) is not None:
    		parser_result.extend(parser_inference_logic(logic))
    	elif re.match(Demonstrate_lp, logic) is not None:
    		parser_result.extend(parser_demonstrate_logic(logic))
    	elif re.match(Condition_lp, logic) is not None:
    		parser_result.extend(parser_condition_logic(logic))
    	elif re.match(Proposition_lp, logic) is not None:
    		parser_result.extend(parser_proposition_logic(logic))
    	else:
    		parser_result.extend(parser_basic_logic(logic))
    		if count<length:
    			parser_result.append(",")

    return parser_result


def parser_inference_logic(logic_sentence):
	''' parser inference logic
	args:
		logic sentence
			ex:(SlopeOfLine(l,rs_a),Asking1(rs_a)):-(Equal($\cos\theta$,$\frac{4}{5}$))
	returns
		logic list
			ex:["(","SlopeOfLine","(","l",",","rs_a",")",",","Asking1","(","rs_a",")",")",":-","(","Equal","(","$\cos\theta$",",","$\frac{4}{5}$",")",")"]
	'''
	parser_result = []
	bracket_counts = 0
	pattern = "\\(.+\\)"

	if re.match(Inference_lp, logic_sentence) is not None:
		parser_result.append("(")

		for i in range(len(logic_sentence)-1):
			if logic_sentence[i] == "(":
				bracket_counts += 1
			elif logic_sentence[i] == ")":
				bracket_counts -= 1
			elif logic_sentence[i] == ":" and logic_sentence[i+1] == "-" and bracket_counts<=0:
				s1 = logic_sentence[0:i]
				s2 = logic_sentence[i+2:len(logic_sentence)]

		if re.match(pattern, s1) is not None:
			parser_result.extend(split_logic(s1[1:len(s1)-1]))
			parser_result.append(")")
		else:
			parser_result.extend(parser_basic_logic(s1))
		parser_result.append(":-")

		if re.match(pattern, s2) is not None:
			parser_result.append("(")
			parser_result.extend(split_logic(s2[1:len(s2)-1]))
			parser_result.append(")")
		else:
			parser_result.extend(parser_basic_logic(s2))
	else:
		p_logic = parser_basic_logic(logic_sentence)
		parser_result.extend(p_logic)

	return parser_result

def parser_demonstrate_logic(logic_sentence):
	''' parser Demonstrate logic
	args:
		logic sentence
			ex:(SlopeOfLine(l,rs_a),Asking1(rs_a)):-(Equal($\cos\theta$,$\frac{4}{5}$))
	returns
		logic list
			ex:["(","SlopeOfLine","(","l",",","rs_a",")",",","Asking1","(","rs_a",")",")",":-","(","Equal","(","$\cos\theta$",",","$\frac{4}{5}$",")",")"]
	'''
	parser_result = []
	if re.match(Demonstrate_lp, logic_sentence) is not None:
		index = logic_sentence.find("(")
		logic_name = logic_sentence[0:index]

		parser_result.append(logic_name)
		ele = logic_sentence[index+1:len(logic_sentence)-1]

		if re.match(Inference_lp, ele) is not None:
			parser_result.append("(")
			parser_result.extend(parser_inference_logic(ele))
			parser_result.append(")")
		else:
			parser_result.append("(")
			parser_result.extend(split_logic(ele))
			parser_result.append(")")

	return parser_result

def parser_logicRS_logic(logic_sentence):
	'''parser LogicalRelationship logic

	ex:LogicalRelationship((GreaterThan(A,$30^{\circ}$)),(GreaterThan($\sinA$,$\\frac{1}{2}$)),rs_a)
	'''
	parser_result = []
	bracket_counts = 0
	logic_eles = []
	
	if re.match(LogicRS_lp, logic_sentence) is not None:
		index = logic_sentence.find("(")
		logic_name = logic_sentence[0:index]

		for i in range(len(logic_sentence)):
			if logic_sentence[i] == "(":
				bracket_counts += 1
			elif logic_sentence[i] == ")":
				bracket_counts -= 1
			elif logic_sentence[i] == "," and bracket_counts <=1:
				logic_eles.append(logic_sentence[index+2:i-1])
				index = i
		logic_eles.append(logic_sentence[index+1:len(logic_sentence)-1])

		parser_result.append(logic_name)
		parser_result.append("(")
		parser_result.append("(")
		count = 0
		for ele in logic_eles:
			count += 1 
			parser_result.extend(split_logic(ele))
			parser_result.append(")")
			if count<3:
				parser_result.append(",")

	return parser_result

def parser_proposition_logic(logic_sentence):
	''' parser proposition logic

	args:
		ex:Proposition(rs_a,(Exist($x_{0}C_{R}Q$),BelongTo($x_{0}^3$,Q)))
	'''
	parser_result = []
	bracket_counts = 0

	if re.match(Proposition_lp, logic_sentence) is not None:
		index = logic_sentence.find("(")
		logic_name = logic_sentence[0:index]

		for i in range(len(logic_sentence)):
			if logic_sentence[i] == "(":
				bracket_counts += 1
			elif logic_sentence[i] == ")":
				bracket_counts -= 1
			elif logic_sentence[i] == "," and bracket_counts <=1:
				'''
				s1 = "rs_a" s2 = "Exist($x_{0}C_{R}Q$),BelongTo($x_{0}^3$,Q)"
				'''
				s1 = logic_sentence[index+1:i] 
				s2 = logic_sentence[i+2:len(logic_sentence)-2]
		
		parser_result.append(logic_name)
		parser_result.append("(")
		parser_result.extend(parser_basic_logic(s1))
		parser_result.append(",")
		parser_result.append("(")
		parser_result.extend(split_logic(s2))
		parser_result.append(")")
		parser_result.append(")")
	return parser_result

def parser_condition_logic(logic_sentence):
	'''parser condition logic

	args ex:NecessaryNotSufficientCondition((GreaterThan($a^2-3b$,0)),(HaveNumberDifferentZeroPoint(f(x),3)))
	'''
	pattern = "\\(.+\\)"
	parser_result = []
	bracket_counts = 0
	if re.match(Condition_lp, logic_sentence) is not None:
		index = logic_sentence.find("(")
		logic_name = logic_sentence[0:index]

		for i in range(len(logic_sentence)):
			if logic_sentence[i] == "(":
				bracket_counts += 1
			elif logic_sentence[i] == ")":
				bracket_counts -= 1
			elif logic_sentence[i] == "," and bracket_counts <=1:
				'''
				s1 = "(GreaterThan($a^2-3b$,0))"
				s2 = "(HaveNumberDifferentZeroPoint(f(x),3))"
				'''
				s1 = logic_sentence[index+1:i]
				s2 = logic_sentence[i+1:len(logic_sentence)-1]

		parser_result.append(logic_name)
		parser_result.append("(")
		if re.match(pattern,s1) is not None:
			parser_result.append("(")
			parser_result.extend(split_logic(s1[1:len(s1)-1]))
			parser_result.append(")")
			parser_result.append(",")
		else:
			parser_result.extend(parser_basic_logic(s1))
			parser_result.append(",")

		if re.match(pattern,s2) is not None:
			parser_result.append("(")
			parser_result.extend(split_logic(s2[1:len(s2)-1]))
			parser_result.append(")")
			parser_result.append(")")
		else:
			parser_result.extend(parser_basic_logic(s2))
			parser_result.append(")")
	return parser_result



def parser(logic_sentence):
	parser_result = []
	if re.match(Demonstrate_lp, logic_sentence) is not None:
		parser_result = parser_demonstrate_logic(logic_sentence)
	elif re.match(LogicRS_lp, logic_sentence) is not None:
		parser_result = parser_logicRS_logic(logic_sentence)
	elif re.match(Inference_lp, logic_sentence) is not None:
		parser_result = parser_inference_logic(logic_sentence)
	elif re.match(Condition_lp, logic_sentence) is not None:
		parser_result = parser_condition_logic(logic_sentence)
	elif re.match(Proposition_lp, logic_sentence) is not None:
		parser_result = parser_proposition_logic(logic_sentence)
	else:
		parser_result = parser_basic_logic(logic_sentence)
	return parser_result