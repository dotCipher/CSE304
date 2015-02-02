import sys
from protoplasm_parse import *

#Returns a boolean relating to whether the asTree
#is an AE with an ID or INTCONST only (without any Op's)
#Otherwise, it will also return a boolean indicating if
#the asTree is itself an ID or INTCONST already
def isIDorINTCONST(asTree):
    if isinstance(asTree,AE):
        return (isinstance(asTree.lchild,ID) or isinstance(asTree.lchild,INTCONST)) and asTree.mchild == None
    else:
        return isinstance(asTree.lchild,ID) or isinstance(asTree.lchild,INTCONST)

#Creates a list and and interprets intermediate code
#based on the AST starting with statement counter line
def gencode(asTree, line):
    
    triplesList = list()
    interp(asTree, triplesList, line)
    return triplesList

#Generates the actual intermediate code onto the triples
#list based on the AST starting with statement counter line
def interp(asTree, triples, line):

    #PGM -> STMTSEQ
    if isinstance(asTree,PGM):
        line = interp(asTree.child, triples, line)
        
    #STMTSEQ -> STMT STMTSEQ
    #       |   STMT
    if isinstance(asTree,STMTSEQ):
        line = interp(asTree.lchild, triples, line)
        line = interp(asTree.rchild, triples, line)
        
    #STMT -> ASSIGN
    #   |    PRINT
    #   |    BLOCK
    #   |    IF
    #   |    WHILE
    elif isinstance(asTree,STMT):
        line = interp(asTree.child, triples, line)
        
    #ASSIGN -> ID = RHS ;
    elif isinstance(asTree,ASSIGN):
        if isinstance(asTree.rchild.child, AE) and isIDorINTCONST(asTree.rchild.child):
            triples.append((line, '=', asTree.lchild.value, asTree.rchild.child.lchild.value))
        else:
            line = interp(asTree.rchild, triples, line)
            triples.append((line, '=', asTree.lchild.value, line - 1))
        line = line + 1
        
    #PRINT -> print( AE );
    elif isinstance(asTree,PRINT):
        if isIDorINTCONST(asTree.child):
            triples.append((line, 'print', None, asTree.child.lchild.value))
        else:
            line = interp(asTree.child, triples, line)
            triples.append((line, 'print', None, line - 1))
        line = line + 1

    #BLOCK -> { STMTSEQ }
    elif isinstance(asTree,BLOCK):
        line = interp(asTree.child, triples, line)

    #IF -> if AE then STMT else STMT
    #   |  if AE then STMT
    elif isinstance(asTree,IF):
        if isIDorINTCONST(asTree.lchild):
            statement = gencode(asTree.mchild, line + 1)
            lastElement = statement.pop(len(statement) - 1)
            lastLineNum = lastElement[0]
            if asTree.rchild == None:
                triples.append((line, 'if', asTree.lchild.lchild.value, lastLineNum + 1))
            else:
                triples.append((line, 'if', asTree.lchild.lchild.value, lastLineNum + 2))
            line = lastLineNum + 1
            statement.append(lastElement)
            for item in statement:
                triples.append(item)

        else:
            line1 = interp(asTree.lchild, triples, line)
            statement = gencode(asTree.mchild, line1 + 1)
            lastElement = statement.pop(len(statement) - 1)
            lastLineNum = lastElement[0]
            if asTree.rchild == None:
                triples.append((line1, 'if', line1 - 1, lastLineNum + 1))
            else:
                triples.append((line1, 'if', line1 - 1, lastLineNum + 2))
            line = lastLineNum + 1
            statement.append(lastElement)
            for item in statement:
                triples.append(item)

        if not asTree.rchild == None:
            statement = gencode(asTree.rchild, line + 1)
            lastElement = statement.pop(len(statement) - 1)
            lastLineNum = lastElement[0]
            triples.append((line, 'goto', None, lastLineNum + 1))
            line = lastLineNum + 1
            statement.append(lastElement)
            for item in statement:
                triples.append(item)

    #WHILE -> while AE do STMT
    elif isinstance(asTree,WHILE):
        if isIDorINTCONST(asTree.lchild):
            statement = gencode(asTree.rchild, line + 1)
            lastElement = statement.pop(len(statement) - 1)
            lastLineNum = lastElement[0] + 1
            triples.append((line, 'while', asTree.lchild.lchild.value, lastLineNum + 1))
            statement.append(lastElement)
            for item in statement:
                triples.append(item)
            triples.append((lastLineNum, 'goto', None, line))
            line = lastLineNum + 1

        else:
            line1 = interp(asTree.lchild, triples, line)
            statement = gencode(asTree.rchild, line1 + 1)
            lastElement = statement.pop(len(statement) - 1)
            lastLineNum = lastElement[0] + 1
            triples.append((line1, 'while', line1 - 1, lastLineNum + 1))
            statement.append(lastElement)
            for item in statement:
                triples.append(item)
            triples.append((lastLineNum, 'goto', None, line))
            line = lastLineNum + 1

    #RHS -> INPUT
    #   |   AE
    elif isinstance(asTree,RHS):
        line = interp(asTree.child, triples, line)
    
    #INPUT -> input ( )
    elif isinstance(asTree,INPUT):
        triples.append((line, 'input', None, None))
        line = line + 1
        
    #AE -> AE BINOP AE
    #   |  UNOP AE
    #   |  ( AE )
    #   |  INTCONST
    #   |  ID
    elif isinstance(asTree,AE):
        if isinstance(asTree.mchild, BINOP):
            if isIDorINTCONST(asTree.lchild):
                if isIDorINTCONST(asTree.rchild):
                    triples.append((line, asTree.mchild.value, asTree.lchild.lchild.value, asTree.rchild.lchild.value))
                else:
                    line = interp(asTree.rchild, triples, line)
                    triples.append((line, asTree.mchild.value, asTree.lchild.lchild.value, line - 1))
            else:
                line1 = interp(asTree.lchild, triples, line)
                if isIDorINTCONST(asTree.rchild):
                    line = line1
                    triples.append((line1, asTree.mchild.value, line1 - 1, asTree.rchild.lchild.value))
                else:
                    line = interp(asTree.rchild, triples, line1)
                    triples.append((line, asTree.mchild.value, line1 - 1, line - 1))

        elif isinstance(asTree.lchild, UNOP):
            if isIDorINTCONST(asTree.mchild):
                triples.append((line, asTree.lchild.value, None, asTree.mchild.lchild.value))
            else:
                line = interp(asTree.mchild, triples, line)
                triples.append((line, asTree.lchild.value, None, line - 1))
        elif isinstance(asTree.lchild, AE):
            line = interp(asTree.lchild, triples, line)
            line = line - 1

        line = line + 1

    elif isinstance(asTree,ID) or isinstance(asTree,INTCONST):
        triples.append((line, '=', None, asTree.value))
        line = line + 1

    return line

def optimize(triples):

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

