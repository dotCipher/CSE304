# ---------------------------------------------------- #
# CSE 304/504
# HW 1
# Cody Moore
# Part B: Python Classes
# ---------------------------------------------------- #
# NNF Rules:
# ~(All x in G) -> Each x in ~G
# ~(Each x in G) -> All x in ~G
# ~~G -> G
# ~(G1 AND G2) -> ~G1 OR ~G2
# ~(G1 OR G2) -> ~G1 AND ~G2
# ---------------------------------------------------- #
# Imports and globals
import re
def insert_between(list, item, check):
	result = list
# ---------------------------------------------------- #
# 1- Read first operator (highest level)
# 2- Check all rules on operator
# 3- If more operators are underneath,
#    pop them off and check them too
# 4- Continue process until all operators
# 	 are checked
# ASSUMPTION: All variables declared are within alphabet:
# a-z
class PBF:
	def isNNF(PBF):
		i = 0
		pfa = str(PBF).split()
		while i < len(pfa):
			if pfa[i] == '!':
				nnf_var = bool(re.search('[a-z]', pfa[i-1], re.IGNORECASE))
				if nnf_var == False:
					return False
				elif i + 1 < len(pfa):
					if pfa[i+1] == '!':
						return False
			i += 1
		return True
	
	def toNNF(PBF):
		i = 0
		pfa = str(PBF).split()
		while i < len(pfa):
			if pfa[i] == '!':
				nnf_var = bool(re.search('[a-z]', pfa[i-1], re.IGNORECASE))
				if nnf_var == False:
					return False
				elif i + 1 < len(pfa):
					if pfa[i+1] == '!':
						return False
			i += 1
		return True
	
class OR(PBF):
    
    def __init__(self, f1, f2):
        self.lchild = f1
        self.rchild = f2

    def __str__(self):
        return str(self.lchild) + " " + str(self.rchild) + " |"


class AND(PBF):

    def __init__(self, f1, f2):
        self.lchild = f1
        self.rchild = f2

    def __str__(self):
        return str(self.lchild) + " " + str(self.rchild) + " &"


class NOT(PBF):

    def __init__(self, f):
        self.child = f

    def __str__(self):
        return str(self.child) + " !"


class PROP(PBF):

    def __init__(self, p):
        self.prop = p

    def __str__(self):
        return self.prop

# ---------------------------------------------------- #
# DEBUGGING CODE, REMOVE IF NEEDED
# ---------------------------------------------------- #
NNF_false_exp1 = AND(PROP("x"), NOT(OR(PROP("y"), PROP("z"))))
NNF_true_exp1 = AND(PROP("x"), AND(NOT(PROP("y")), NOT(PROP("z"))))
NNF_false_exp2 = NOT(AND(PROP("y"), PROP("z")))
NNF_true_exp2 = AND(NOT(PROP("y")), NOT(PROP("z")))
NNF_false_exp3 = NOT(NOT(PROP("y")))
NNF_true_exp3 = PROP("y")
print str(NNF_false_exp1)
print "NNF FALSE EXP 1 = " + str(PBF.isNNF(NNF_false_exp1))
print str(NNF_true_exp1)
print "NNF TRUE EXP 2 = " + str(PBF.isNNF(NNF_true_exp1))
print str(NNF_false_exp2)
print "NNF FALSE EXP 3 = " + str(PBF.isNNF(NNF_false_exp2))
print str(NNF_true_exp2)
print "NNF TRUE EXP 4 = " + str(PBF.isNNF(NNF_true_exp2))
print str(NNF_false_exp3)
print "NNF FALSE EXP 5 = " + str(PBF.isNNF(NNF_false_exp3))
print str(NNF_true_exp3)
print "NNF TRUE EXP 6 = " + str(PBF.isNNF(NNF_true_exp3))
print "CONVERT TO NNF EXP 1 = " + str(PBF.toNNF(NNF_false_exp1))
print "CONVERT TO NNF EXP 2 = " + str(PBF.toNNF(NNF_true_exp1))
print "CONVERT TO NNF EXP 3 = " + str(PBF.toNNF(NNF_false_exp2))
print "CONVERT TO NNF EXP 4 = " + str(PBF.toNNF(NNF_true_exp2))
print "CONVERT TO NNF EXP 5 = " + str(PBF.toNNF(NNF_false_exp3))
print "CONVERT TO NNF EXP 6 = " + str(PBF.toNNF(NNF_true_exp3))
# ---------------------------------------------------- #
