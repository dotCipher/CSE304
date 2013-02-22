# -------------------------------------------------------- #
# Protoplasm 1 - Interpreter
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
import ply.yacc as yacc
# -------------------------------------------------------- #
# Main Code Block
# -------------------------------------------------------- #
class PROTO:
	pass

# Pgm	-> Stmt Pgm
# Pgm	-> Stmt
class PGM(PROTO):
    def __init__(self, stmt, pgm):
        self.lchild = stmt
        self.rchild = pgm
	
	@classmethod
	def endSTMT(self, stmt):
		self.child = stmt
		
# Stmt	-> Asgn
# Stmt	-> Prnt
class STMT(PROTO):
	def __init__(self, asgn_or_prnt):
		self.child = asgn_or_prnt
		
# Asgn	-> var = Rhs ;
class ASSIGN(PROTO):
	def __init__(self, var, rhs):
		self.lchild = var
		self.rchild = rhs

# Prnt	-> print ( AE );
class PRINT(PROTO):
	def __init__(self, ae):
		self.child = ae

# Rhs	-> input ( )
# Rhs	-> AE
class RHS(PROTO):
	def __init__(self, f):
			self.lchild = f

class AE(PROTO):
	def __init__(self, f):
		self.lchild = f
	
	@classmethod
	def setSumOp(self, f1, f2, f3):
		self.lchild = f1
		self.mchild = f2
		self.rchild = f3

class T(PROTO):
	def __init__(self, f):
		self.lchild = f
	
	@classmethod
	def setProdOp(self, f1, f2, f3):
		self.lchild = f1
		self.mchild = f2
		self.rchild = f3

class F(PROTO):
	def __init__(self, f):
		self.lchild = f
	
	@classmethod
	def setProdOp(self, f1, f2, f3):
		self.lchild = f1
		self.mchild = f2
		self.rchild = f3

class SUMOP():
	def __init__(self, type):
		self.value = type
