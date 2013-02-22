# -------------------------------------------------------- #
# Protoplasm 1 - Parser and Scanner
# -------------------------------------------------------- #
# The Grammer for protoplasm is as follows:
#
# Pgm = Program
# Stmt = Statement
# Asgn = Assignment
# Prnt = Print
# Rhs = Right hand side
# AE = Assignment expression
# T = Term
# F = Factor
# SumOp = Sum Operator
# PrdOp = Product Operator
#
# Pgm	-> Stmt Pgm
# Pgm	-> Stmt
# Stmt	-> Asgn
# Stmt	-> Prnt
# Asgn	-> var = Rhs ;
# Prnt	-> print ( AE );
# Rhs	-> input ( )
# Rhs	-> AE
# AE	-> T SumOp AE
# AE	-> T
# T	-> F PrdOp T
# T	-> F
# F	-> intconst
# F	-> var
# F	-> - F
# F	-> ( AE )
# SumOp	-> +
# SumOp	-> -
# PrdOp	-> *
# PrdOp	-> /
# PrdOp	-> %
# -------------------------------------------------------- #
# Imports and globals
# -------------------------------------------------------- #
import sys
import ply.lex as lex
import ply.yacc as yacc
import protoplasm_interp
import protoplasm_lex
# -------------------------------------------------------- #
# Functions
# -------------------------------------------------------- #

def tokenz(l, i):
    if len(l) == i:
        return
    if len(l[i]) == 0:
        l.pop(i)
    elif len(l[i]) > 1:
        if ';' in l[i]:
            ituple = l[i].partition(';')
            l.pop(i)
            for j in range(3):
                l.insert(i+j,ituple[j])
        elif '=' in l[i]:
            ituple = l[i].partition('=')
            l.pop(i)
            for j in range(3):
                l.insert(i+j,ituple[j])
        elif '(' in l[i]:
            ituple = l[i].partition('(')
            l.pop(i)
            for j in range(3):
                l.insert(i+j,ituple[j])
        elif ')' in l[i]:
            ituple = l[i].partition(')')
            l.pop(i)
            for j in range(3):
                l.insert(i+j,ituple[j])
        elif '-' in l[i]:
            ituple = l[i].partition('-')
            l.pop(i)
            for j in range(3):
                l.insert(i+j,ituple[j])
        elif '*' in l[i]:
            ituple = l[i].partition('*')
            l.pop(i)
            for j in range(3):
                l.insert(i+j,ituple[j])
        elif '/' in l[i]:
            ituple = l[i].partition('/')
            l.pop(i)
            for j in range(3):
                l.insert(i+j,ituple[j])
        elif '%' in l[i]:
            ituple = l[i].partition('%')
            l.pop(i)
            for j in range(3):
                l.insert(i+j,ituple[j])
        else:
            i += 1
    else:
        i += 1
    tokenz(l, i)

def convertToStmts(parsedList):
    newList = list()
    listToAdd = list()
    while len(parsedList) > 0:
        if parsedList[0] == ';':
            newList.append(listToAdd)
            listToAdd = list()
        else:
            listToAdd.append(parsedList[0])
        parsedList.pop(0)
    return newList

# -------------------------------------------------------- #
# Main Code Block
# -------------------------------------------------------- #
def main():
	s = ''
	if len(sys.argv) > 1:
		f = open(sys.argv[1],'r')
		for line in f:
			s += line
	else:
		print 'Please run protoplasm with this format: protoplasm1.py arg1'
		print 'arg1 being a .proto file'
	if len(sys.argv) > 1:
		for line in f:
			s += line + ' '
		#l = s.split()
		#tokenz(l, 0)
		#print l
		#newList = convertToStmts(l)
		#print newList
		# Setup lexer
		lexer = lex.lex(module=protoplasm_lex)
		lexer.input(s)
		token_list = list()
		while True:
			token = lexer.token()
			if not token: 
				break
			else:
				token_list.append(token)
		print token_list
		
if __name__ == "__main__":
	main()
