# -------------------------------------------------------- #
# Protoplasm 1 - Parser
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
# -------------------------------------------------------- #
# Imports and globals
# -------------------------------------------------------- #
import re
import protoplasm_lex
from ply import *
# -------------------------------------------------------- #
# Precedence of Grammar
# -------------------------------------------------------- #
tokens = protoplasm_lex.tokens

precedence = (
    ('right', 'EQUALS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)
# -------------------------------------------------------- #
# Grammar Type Definitions
# -------------------------------------------------------- #
class PROTO:
	pass

# Pgm	-> Stmt Pgm
# Pgm	-> Stmt
class PGM(PROTO):
	def __init__(self, stmt, pgm):
		self.lchild = stmt
		self.rchild = pgm
	def __repr__(self):
		return "PGM(%r, %r)" % (self.lchild, self.rchild)

# Stmt	-> Asgn
# Stmt	-> Prnt
class STMT(PROTO):
	def __init__(self, asgn_or_prnt):
		self.child = asgn_or_prnt
	def __repr__(self):
		return "STMT(%r)" % (self.child)
		
# Asgn	-> var = Rhs ;
class ASSIGN(PROTO):
	def __init__(self, var, rhs):
		self.lchild = var
		self.rchild = rhs
	def __repr__(self):
		return "ASSIGN(%r, %r)" % (self.lchild, self.rchild)

# Prnt	-> print ( AE );
class PRINT(PROTO):
	def __init__(self, ae):
		self.child = ae
	def __repr__(self):
		return "PRINT(%r)" % (self.child)

# Rhs	-> input ( )
# Rhs	-> AE
class RHS(PROTO):
	def __init__(self, f):
			self.child = f
	def __repr__(self):
		return "RHS(%r)" % (self.child)

# AE	-> T SumOp AE
# AE	-> T
class AE(PROTO):
	def __init__(self, f1, f2, f3):
		self.lchild = f1
		self.mchild = f2
		self.rchild = f3
	def __repr__(self):
		return "AE(%r, %r, %r)" % (self.lchild, self.mchild, self.rchild)

# T	-> F PrdOp T
# T	-> F
class T(PROTO):
	def __init__(self, f1, f2, f3):
		self.lchild = f1
		self.mchild = f2
		self.rchild = f3
	def __repr__(self):
		return "T(%r, %r, %r)" % (self.lchild, self.mchild, self.rchild)

# F	-> intconst
# F	-> var
# F	-> - F
# F	-> ( AE )
class F(PROTO):
	def __init__(self, f):
		self.child = f
	def __repr__(self):
		return "F(%r)" % (self.child)

# SumOp	-> +
# SumOp	-> -
class SUMOP(PROTO):
	def __init__(self, f):
		self.value = f
	def __repr__(self):
		return "SUMOP(%r)" % (self.value)

# PrdOp	-> *
# PrdOp	-> /
# PrdOp	-> %
class PRODOP(PROTO):
	def __init__(self, f):
		self.value = f
	def __repr__(self):
		return "PRODOP(%r)" % (self.value)

# Intconst -> int
class INTCONST(PROTO):
	def __init__(self, f):
		self.value = f
	def __repr__(self):
		return "INTCONST(%r)" % (self.value)

# Var -> String
class VAR(PROTO):
	def __init__(self, f):
		self.value = f
	def __repr__(self):
		return "VAR(%r)" % (self.value)

class INPUT():
	def __init__(self):
		pass
	def __repr__(self):
		return "INPUT()"

# -------------------------------------------------------- #
# Grammar Rule Functions
# -------------------------------------------------------- #
def p_pgm(p):
	""" 
	pgm : stmt pgm
	pgm : stmt
	"""
	# Check if empty
	if len(p) == 1:
		raise TypeError("Error: No program to compile")
	elif len(p) == 2:
		p[0] = PGM(p[1], None)
	else:
		p[0] = PGM(p[1], p[2])

def p_stmt(p):
	""" 
	stmt : assign
	stmt : print
	"""
	p[0] = STMT(p[1])

def p_assign(p):
	"""
	assign : VAR EQUALS rhs SEMICOLON
	"""
	if len(p) < 3:
		raise TypeError("Error: Invalid Syntax")
	else:
		p[0] = ASSIGN(VAR(p[1]), p[3])

def p_print(p):
	"""
	print : PRINT LPAREN ae RPAREN SEMICOLON
	"""
	p[0] = PRINT(p[3])

def p_rhs(p):
	"""
	rhs : INPUT LPAREN RPAREN
	rhs : ae
	"""
	if p[1] == "input":
		p[0] = RHS(INPUT())
	else:
		p[0] = RHS(p[1])

def p_ae(p):
	"""
	ae : t sumop ae
	ae : t
	"""
	if len(p) == 2:
		p[0] = AE(p[1], None, None)
	else:
		p[0] = AE(p[1], p[2], p[3])

def p_t(p):
	"""
	t : f prodop ae
	t : f
	"""
	if len(p) == 2:
		p[0] = T(p[1], None, None)
	else:
		p[0] = T(p[1], p[2], p[3])

def p_f(p):
	"""
	f : INTCONST
	f : VAR
	f : MINUS f
	f : LPAREN ae RPAREN
	"""
	if p[1] == '-':
		p[0] = F(p[2])
	elif (p[1] == '(') and (p[3] == ')'):
		p[0] = F(p[2])
	else:
		isInt = isinstance(p[1], int)
		if isInt:
			p[0] = F(INTCONST(str(p[1])))
		else:
			p[0] = F(VAR(p[1]))

def p_prodop(p):
	"""
	prodop : TIMES
	prodop : DIVIDE
	prodop : MOD
	"""
	p[0] = PRODOP(p[1])
	
def p_sumop(p):
	"""
	sumop : PLUS
	sumop : MINUS
	"""
	p[0] = SUMOP(p[1])

# Error rule for syntax errors
def p_error(p):
	print "Syntax Error at %r on line %r" % (p.value, p.lineno)

# Build parser to make AST
proto_parser = yacc.yacc()

def parse(data):
	proto_parser.error = 0
	parse = proto_parser.parse(data)
	if proto_parser.error: return None
	return parse


