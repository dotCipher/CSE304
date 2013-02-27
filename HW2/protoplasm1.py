# -------------------------------------------------------- #
# Protoplasm 1 - Main Caller
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
import protoplasm_parse
import protoplasm_lex
import protoplasm_interp
import protoplasm_mips
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
		
		program = protoplasm_parse.parse(s)
		# Global of triples set up in protoplasm_interp
		protoplasm_interp.gencode(program, 0)
		protoplasm_interp.optimize()
		#print ""
		#print ""
		#print program
		#print ""
		#print ""
		#print ""
		#print ""
		#print protoplasm_interp.triples
		#print ""
		#print ""
		# Get file name to write too
		i = sys.argv[1].rindex('.')
		substr = sys.argv[1][:i]
		filename = substr + ".asm"
		# Generate MIPS from intermediate code
		protoplasm_mips.make_asm_exec(filename, protoplasm_interp.triples)
		print "Written out to file: %s" % filename

if __name__ == "__main__":
	main()
