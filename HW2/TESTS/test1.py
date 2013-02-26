import tokrules1
import ply.lex as lex
lexer = lex.lex(module=tokrules1)
lexer.input("3 + 4")
print lexer.token()
print lexer.token()
print lexer.token()
