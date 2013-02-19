# -------------------------------------------------------- #
# Protoplasm 1 - Parser and Scanner
# -------------------------------------------------------- #
# The Grammer for protoplasm is as follows:

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
# T		-> F PrdOp T
# T		-> F
# F		-> intconst
# F		-> var
# F		-> - F
# F		-> ( AE )
# SumOp	-> +
# SumOp	-> -
# PrdOp	-> *
# PrdOp	-> /
# PrdOp	-> %
# -------------------------------------------------------- #
# Imports and globals
# -------------------------------------------------------- #
import sys
# -------------------------------------------------------- #
# Main Code Block
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

def seperateLines(strList):
	

def main():
	s = ''
	if len(sys.argv) > 1:
		f = open(sys.argv[1],'r')
		for line in f:
			s += line
	else:
		print 'Please run protoplasm with this format: protoplasm1.py arg1'
		print 'arg1 being a .proto file'
	
	for line in f:
		s += line + ' '
	l = s.split()
	print l
	tokenz(l, 0)
	print l
	
main()
