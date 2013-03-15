# -------------------------------------------------------- #
# Protoplasm 2 - Parser
# -------------------------------------------------------- #
# The Grammer for protoplasm2 is as follows:
#
# Pgm = Program
# Stmt = Statement
# StmtSeq = Statement Sequence
# Asgn = Assignment
# Prnt = Print
# Block = Block
# If = If
# While = While
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
	('right', 'UMINUS'),
	('right', 'NOT'),
    ('right', 'EQUALS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('left', 'PLUS', 'MINUS'),
    ('nonassoc', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'LAND'),
    ('left', 'LOR'),
)
# -------------------------------------------------------- #
# Grammar Type Definitions
# -------------------------------------------------------- #
class PROTO:
	pass

# Pgm	-> StmtSeq
class PGM(PROTO):
	def __init__(self, stmtseq):
		self.child = stmtseq
	def __repr__(self):
		return "PGM(%r)" % (self.child)

# StmtSeq  -> Stmt StmtSeq
# StmtSeq  -> Stmt None
class STMTSEQ(PROTO):
	def __init__(self, stmt, stmtseq):
		self.lchild = stmt
		self.rchild = stmtseq
	def __repr__(self):
		return "STMTSEQ(%r, %r)" % (self.lchild, self.rchild)

# Stmt	-> Asgn
# Stmt	-> Prnt
# Stmt  -> Block
# Stmt  -> If
# Stmt  -> While
class STMT(PROTO):
	def __init__(self, stype):
		self.child = stype
	def __repr__(self):
		return "STMT(%r)" % (self.child)
		
# Asgn	-> id = Rhs ;
class ASSIGN(PROTO):
	def __init__(self, idstr, rhs):
		self.lchild = idstr
		self.rchild = rhs
	def __repr__(self):
		return "ASSIGN(%r, %r)" % (self.lchild, self.rchild)

# Prnt	-> print ( AE );
class PRINT(PROTO):
	def __init__(self, ae):
		self.child = ae
	def __repr__(self):
		return "PRINT(%r)" % (self.child)

# Block  -> { StmtSeq }
class BLOCK(PROTO):
	def __init__(self, stmtseq):
		self.child = stmtseq
	def __repr__(self):
		return "BLOCK(%r)" % (self.child)

# If  -> if AE then STMT else STMT
# If  -> if AE then STMT      None
class IF(PROTO):
	def __init__(self, ae, stmt1, stmt2):
		self.lchild = ae
		self.mchild = stmt1
		self.rchild = stmt2
	def __repr__(self):
		return "IF(%r, %r, %r)" % (self.lchild, self.mchild, self.rchild)

# While  -> while AE do STMT
class WHILE(PROTO):
	def __init__(self, ae, stmt):
		self.lchild = ae
		self.rchild = stmt
	def __repr__(self):
		return "WHILE(%r, %r)" % (self.lchild, self.rchild)

# Rhs	-> input ( )
# Rhs	-> AE
class RHS(PROTO):
	def __init__(self, ae):
			self.child = ae
	def __repr__(self):
		return "RHS(%r)" % (self.child)

# AE	-> T BinOp AE
# AE    -> UnOp AE
# AE    -> ( AE )
# AE    -> intconst
# AE    -> id
class AE(PROTO):
	def __init__(self, f1, f2, f3):
		self.lchild = f1
		self.mchild = f2
		self.rchild = f3
	def __repr__(self):
		return "AE(%r, %r, %r)" % (self.lchild, self.mchild, self.rchild)

# BinOp	-> +
# BinOp	-> -
# BinOp	-> *
# BinOp	-> /
# BinOp	-> %
# BinOp	-> &&
# BinOp	-> ||
# BinOp	-> ==
# BinOp	-> !=
# BinOp	-> <
# BinOp	-> <=
# BinOp	-> >
# BinOp	-> >=
class BINOP(PROTO):
	def __init__(self, op):
		self.value = op
	def __repr__(self):
		return "BINOP(%r)" % (self.value)

# UnOp	-> -
# UnOp	-> !
class UNOP(PROTO):
	def __init__(self, op):
		self.value = op
	def __repr__(self):
		return "UNOP(%r)" % (self.value)

# Intconst -> int
class INTCONST(PROTO):
	def __init__(self, intconst):
		self.value = intconst
	def __repr__(self):
		return "INTCONST(%r)" % (self.value)

# Id -> String
class ID(PROTO):
	def __init__(self, string):
		self.value = string
	def __repr__(self):
		return "ID(%r)" % (self.value)

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
	pgm : stmtseq
	"""
	# Check if empty
	if len(p) == 1:
		raise TypeError("Error: No program to compile")
	else:
		p[0] = PGM(p[1])

def p_stmtseq(p):
	"""
	stmtseq : stmt stmtseq
	stmtseq : stmt
	"""
	if len(p) == 2:
		p[0] = STMTSEQ(p[1], None)
	else:
		p[0] = STMTSEQ(p[1], p[2])

def p_stmt(p):
	""" 
	stmt : assign
	stmt : print
	stmt : block
	stmt : if
	stmt : while
	"""
	p[0] = STMT(p[1])

def p_assign(p):
	"""
	assign : ID EQUALS rhs SEMICOLON
	"""
	if len(p) < 3:
		raise TypeError("Error: Invalid Syntax")
	else:
		p[0] = ASSIGN(ID(p[1]), p[3])

def p_print(p):
	"""
	print : PRINT LPAREN ae RPAREN SEMICOLON
	"""
	p[0] = PRINT(p[3])

def p_block(p):
	"""
	block : LBRACE stmtseq RBRACE
	"""
	p[0] = BLOCK(p[2])
	
def p_if(p):
	"""
	if : IF ae THEN stmt ELSE stmt
	if : IF ae THEN stmt
	"""
	if len(p) == 5:
		p[0] = IF(p[2], p[4], None)
	elif len(p) == 7:
		p[0] = IF(p[2], p[4], p[6])
	else:
		raise TypeError("Error: Invalid Syntax")

def p_while(p):
	"""
	while : WHILE ae DO stmt
	"""
	if len(p) != 5:
		raise TypeError("Error: Invalid Syntax")
	else:
		p[0] = WHILE(p[2], p[4])

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
	ae : ae binop ae
	ae : unop ae
	ae : LPAREN ae RPAREN
	ae : INTCONST
	ae : ID
	"""
	if len(p) == 4:
		if (p[1] == "(") and (p[3] == ")"):
			p[0] = AE(p[2], None, None)
		else:
			p[0] = AE(p[1], p[2], p[3])
	elif len(p) == 3:
		p[0] = AE(p[1], p[2], None)
	elif len(p) == 2:
		isInt = isinstance(p[1], int)
		if isInt:
			p[0] = AE(INTCONST(str(p[1])), None, None)
		else:
			p[0] = AE(ID(p[1]), None, None)

def p_binop(p):
	"""
	binop : PLUS
	binop : MINUS
	binop : TIMES
	binop : DIVIDE
	binop : MOD
	binop : LAND
	binop : LOR
	binop : EQ
	binop : NE
	binop : LT
	binop : LE
	binop : GT
	binop : GE
	"""
	p[0] = BINOP(p[1])
	
def p_unop(p):
	"""
	unop : NOT
	unop : MINUS %prec UMINUS
	"""
	p[0] = UNOP(p[1])

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


