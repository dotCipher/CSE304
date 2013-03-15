
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\t\xe6\xa8\xf9\xeclhC\xb7\xa2\xa8:\xd6\xd6\x14f'
    
_lr_action_items = {'RPAREN':([10,11,12,14,15,27,29,31,32,33,34,],[-12,-13,-10,28,-14,34,-15,36,-11,-9,-16,]),'DIVIDE':([10,11,15,29,34,],[21,-13,-14,-15,-16,]),'SEMICOLON':([10,11,12,15,17,19,28,29,32,33,34,36,],[-12,-13,-10,-14,30,-8,35,-15,-11,-9,-16,-7,]),'EQUALS':([4,],[9,]),'TIMES':([10,11,15,29,34,],[22,-13,-14,-15,-16,]),'INTCONST':([7,9,13,16,20,21,22,23,24,25,26,],[11,11,11,11,11,-18,-17,-19,11,-21,-20,]),'PRINT':([0,3,5,6,30,35,],[1,1,-4,-3,-5,-6,]),'PLUS':([10,11,12,15,29,32,33,34,],[-12,-13,26,-14,-15,-11,-9,-16,]),'LPAREN':([1,7,9,13,16,18,20,21,22,23,24,25,26,],[7,13,13,13,13,31,13,-18,-17,-19,13,-21,-20,]),'VAR':([0,3,5,6,7,9,13,16,20,21,22,23,24,25,26,30,35,],[4,4,-4,-3,15,15,15,15,15,-18,-17,-19,15,-21,-20,-5,-6,]),'INPUT':([9,],[18,]),'MOD':([10,11,15,29,34,],[23,-13,-14,-15,-16,]),'MINUS':([7,9,10,11,12,13,15,16,20,21,22,23,24,25,26,29,32,33,34,],[16,16,-12,-13,25,16,-14,16,16,-18,-17,-19,16,-21,-20,-15,-11,-9,-16,]),'$end':([2,3,5,6,8,30,35,],[0,-2,-4,-3,-1,-5,-6,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'prodop':([10,],[20,]),'ae':([7,9,13,20,24,],[14,19,27,32,33,]),'f':([7,9,13,16,20,24,],[10,10,10,29,10,10,]),'sumop':([12,],[24,]),'rhs':([9,],[17,]),'pgm':([0,3,],[2,8,]),'stmt':([0,3,],[3,3,]),'t':([7,9,13,20,24,],[12,12,12,12,12,]),'print':([0,3,],[5,5,]),'assign':([0,3,],[6,6,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> pgm","S'",1,None,None,None),
  ('pgm -> stmt pgm','pgm',2,'p_pgm','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',151),
  ('pgm -> stmt','pgm',1,'p_pgm','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',152),
  ('stmt -> assign','stmt',1,'p_stmt','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',164),
  ('stmt -> print','stmt',1,'p_stmt','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',165),
  ('assign -> VAR EQUALS rhs SEMICOLON','assign',4,'p_assign','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',171),
  ('print -> PRINT LPAREN ae RPAREN SEMICOLON','print',5,'p_print','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',180),
  ('rhs -> INPUT LPAREN RPAREN','rhs',3,'p_rhs','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',186),
  ('rhs -> ae','rhs',1,'p_rhs','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',187),
  ('ae -> t sumop ae','ae',3,'p_ae','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',196),
  ('ae -> t','ae',1,'p_ae','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',197),
  ('t -> f prodop ae','t',3,'p_t','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',206),
  ('t -> f','t',1,'p_t','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',207),
  ('f -> INTCONST','f',1,'p_f','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',216),
  ('f -> VAR','f',1,'p_f','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',217),
  ('f -> MINUS f','f',2,'p_f','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',218),
  ('f -> LPAREN ae RPAREN','f',3,'p_f','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',219),
  ('prodop -> TIMES','prodop',1,'p_prodop','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',234),
  ('prodop -> DIVIDE','prodop',1,'p_prodop','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',235),
  ('prodop -> MOD','prodop',1,'p_prodop','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',236),
  ('sumop -> PLUS','sumop',1,'p_sumop','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',242),
  ('sumop -> MINUS','sumop',1,'p_sumop','G:\\- Work\\- School\\Super Senior Year\\Spring 2013\\CSE 304\\Homeworks\\HW2\\protoplasm_parse.py',243),
]