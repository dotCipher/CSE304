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
        triples.append((line, 'input', None, None))
    #RHS -> INPUT | AE
    elif isinstance(asTree,RHS):
        line = gencode(asTree.child, line)
    #AE -> T SUMOP AE | T
    elif isinstance(asTree,AE):
        if isinstance(asTree.mchild, SUMOP):
            line1 = gencode(asTree.lchild, line)
            line = gencode(asTree.rchild, line1 + 1)
            triples.append((line + 1, asTree.mchild.value, line1, line))
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

def optimize():

    i = 0
    length = len(triples)

    while i < length:

        #print triples
        if triples[i][3] == None and not triples[i][1] == 'input':
            j = i + 1
            while not (triples[j][2] == triples[i][0] or
                       triples[j][3] == triples[i][0]):
                j = j + 1
            if triples[j][2] == triples[i][0]:
                triples.insert(j, (triples[j][0],
                                   triples[j][1],
                                   triples[i][2],
                                   triples[j][3]))
            elif triples[j][3] == triples[i][0]:
                triples.insert(j, (triples[j][0],
                                   triples[j][1],
                                   triples[j][2],
                                   triples[i][2]))
            triples.pop(i)
            triples.pop(j)
            length = length - 1
        elif not triples[i][2] == None and isinstance(triples[i][2], str) and isinstance(triples[i][3], str) and triples[i][2].isdigit() and triples[i][3].isdigit():
                if triples[i][1] == '+':
                    triples.insert(i, (triples[i][0],
                                        '=',
                                        str(int(float(triples[i][2])) +
                                            int(float(triples[i][3]))),
                                        None))
                elif triples[i][1] == '-':
                    triples.insert(i, (triples[i][0],
                                        '=',
                                        str(int(float(triples[i][2])) -
                                            int(float(triples[i][3]))),
                                        None))
                elif triples[i][1] == '*':
                    triples.insert(i, (triples[i][0],
                                       '=',
                                       str(int(float(triples[i][2])) *
                                           int(float(triples[i][3]))),
                                       None))
                elif triples[i][1] == '/':
                    triples.insert(i, (triples[i][0],
                                       '=',
                                       str(int(float(triples[i][2])) /
                                           int(float(triples[i][3]))),
                                       None))
                elif triples[i][1] == '%':
                    triples.insert(i, (triples[i][0],
                                       '=',
                                       str(int(float(triples[i][2])) %
                                           int(float(triples[i][3]))),
                                       None))
                triples.pop(i + 1)
        elif triples[i][1] == '=':
            j = i + 1
            while not (triples[j][2] == triples[i][2] or
                       triples[j][3] == triples[i][2]):
                j = j + 1
            if triples[j][2] == triples[i][2]:
                triples.insert(j, (triples[j][0],
                                   triples[j][1],
                                   triples[i][3],
                                   triples[j][3]))
            elif triples[j][3] == triples[i][2]:
                triples.insert(j, (triples[j][0],
                                   triples[j][1],
                                   triples[j][2],
                                   triples[i][3]))
            triples.pop(i)
            triples.pop(j)
            length = length - 1
        else:
            i = i + 1

    
