# -------------------------------------------------------- #
# Protoplasm 1 - Interpreter
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
class PROTO:
	pass
	
class PGM(PROTO):
    def __init__(self, f1, f2):
        self.lchild = f1
        self.rchild = f2
	
	@classmethod
	def endSTMT(self, f1):
		self.lchild = f1

    #def __str__(self):
    #    return 

class STMT(PROTO):
	def __init__(self, f1):
		self.child = f1

class 
