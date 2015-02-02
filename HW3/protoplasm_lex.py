# -------------------------------------------------------- #
# Protoplasm 2 - Lexer
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
# Pgm	-> StmtSeq
# StmtSeq  -> Stmt StmtSeq
# StmtSeq  -> Stmt None
# Stmt	-> Asgn
# Stmt	-> Prnt
# Stmt  -> Block
# Stmt  -> If
# Stmt  -> While
# Asgn	-> id = Rhs ;
# Prnt	-> print ( AE );
# Block  -> { StmtSeq }
# If  -> if AE then STMT else STMT
# If  -> if AE then STMT      None
# While  -> while AE do STMT
# Rhs	-> input ( )
# Rhs	-> AE
# AE	-> T SumOp AE
# AE	-> T
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
# UnOp	-> -
# UnOp	-> !
# Intconst -> int
# Id -> String
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
	'if' : 'IF',
	'then' : 'THEN',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'do' : 'DO',
}

tokens = [
	'ID',
	'INTCONST',
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'MOD',
	'LAND', 'LOR', 
	'NOT',
	'EQ', 'NE',
	'LT', 'GT',
	'LE', 'GE',
	'LPAREN', 'RPAREN',
	'LBRACE', 'RBRACE',
	'EQUALS',
	'SEMICOLON',
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_LAND = r'&&'
t_LOR = r'\|\|'
t_NOT = r'!'
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_EQUALS = r'='
t_SEMICOLON = r';'

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value, 'ID')
	return t

def t_INTCONST(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_COMMENT(t):
	r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
	pass

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
	print "Error: Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)

lex.lex()

