import sys
from protoplasm_parse import *

triples = list()

#generates and returns intermediate code from AST
def gencode(asTree, line):

    #PGM -> STMT PGM | STMT
    if isinstance(asTree,PGM):
        line = gencode(asTree.rchild, gencode(asTree.lchild, line) + 1)
    #STMT -> ASSIGN | PRINT
    elif isinstance(asTree,STMT):
        line = gencode(asTree.child, line)
    #ASSIGN -> VAR = RHS ;
    elif isinstance(asTree,ASSIGN):
        line = gencode(asTree.rchild, line)
        triples.append((line + 1, '=', asTree.lchild.value, line))
        line = line + 1
    #PRINT -> print( AE );
    elif isinstance(asTree,PRINT):
        line = gencode(asTree.child, line)
        triples.append((line + 1, 'print', None, line))
        line = line + 1
    #INPUT -> input()
    elif isinstance(asTree,INPUT):
        triples.append(line, 'input', None, None)
    #RHS -> INPUT | AE
    elif isinstance(asTree,RHS):
        line = gencode(asTree.child, line)
    #AE -> T SUMOP AE | T
    elif isinstance(asTree,AE):
        if isinstance(asTree.mchild, SUMOP):
            line = gencode(asTree.rchild, line)
            triples.append((line + 1, asTree.mchild.value, asTree.lchild.value, line))
            line = line + 1
        else:
            line = gencode(asTree.lchild, line)
    #T -> F PRODOP T | F
    elif isinstance(asTree,T):
        if isinstance(asTree.mchild, PRODOP):
            line = gencode(asTree.rchild, line)
            if isinstance(asTree.lchild.child, VAR) or isinstance(asTree.lchild.child, INTCONST):
                triples.append((line + 1, asTree.mchild.value, asTree.lchild.child.value, line))
            else:
                line1 = gencode(asTree.lchild, line + 1)
                triples.append((line1 + 1, asTree.mchild.value, line1, line))
                line = line1
            line = line + 1
        else:
            line = gencode(asTree.lchild, line)
    #F -> - F | ( AE ) | INTCONST | VAR
    elif isinstance(asTree,F):
        if isinstance(asTree.child,F):
            line = gencode(asTree.child, line)
            triples.append((line + 1, 'minus', None, line))
            line = line + 1
        else:
            line = gencode(asTree.child, line)
    #INTCONST | VAR
    elif isinstance(asTree,VAR) or isinstance(asTree,INTCONST):
        triples.append((line, '=', asTree.value, None))

    return line

##def optimize():
##
##    changed = True
##
##    while changed:
##        changed = False


#program = PGM(STMT(ASSIGN(VAR('x'),
#                          RHS(AE(T(F(INTCONST('4')),
#                                   PRODOP('*'),
#                                   T(F(VAR('y')),
#                                     None,
#                                     None)),
#                                 None,
#                                 None)))), PGM(STMT(ASSIGN(VAR('x'),
#                          RHS(AE(T(F(F(INTCONST('4'))),
#                                   PRODOP('*'),
#                                   T(F(VAR('y')),
#                                     None,
#                                     None)),
#                                 None,
#                                None)))), None))
#gencode(program, 0)

#print triples

