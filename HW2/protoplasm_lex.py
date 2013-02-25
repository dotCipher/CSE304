# -------------------------------------------------------- #
# Protoplasm 1 - Lexer
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
# Global Imports
# -------------------------------------------------------- #
import sys
from ply import *
# -------------------------------------------------------- #
# Main Code Block
# -------------------------------------------------------- #

reserved = {
	'print' : 'PRINT',
	'input' : 'INPUT',
}

tokens = [
	'VAR',
	'INTCONST',
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'MOD',
	'LPAREN',
	'RPAREN',
	'EQUALS',
	'SEMICOLON'
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='
t_SEMICOLON = r';'
	
def t_VAR(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value, 'VAR')
	return t

def t_INTCONST(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
	print "Error: Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)

lex.lex()

