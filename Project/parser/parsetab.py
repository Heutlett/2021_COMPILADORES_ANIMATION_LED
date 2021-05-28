
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftSUMARESTAleftMULTIPLICACIONDIVISIONDIVISIONENTERArightUMENOSrightMODULOrightEXPONENTEBEGIN BLINK BOOLEAN CALL COMA CORCHETEDER CORCHETEIZQ DEL DELAY DIVISION DIVISIONENTERA DOSPUNTOS END EXPONENTE F FOR ID IF IGUAL IGUALES IN INSERT INT LEN LIST MAIN MAYORIGUAL MAYORQUE MENORIGUAL MENORQUE MIL MIN MODULO MULTIPLICACION NEG PARENTESISDER PARENTESISIZQ PRINTLED PRINTLEDX PROCEDURE PUNTO PYC RANGE RESTA SEG SHAPEC SHAPEF STEP STRING SUMA T TYPE statements : statements statement\n                   | statement\n     statement : expression\n                    | print\n    \n    print : PUNTO\n    \n        statement : ids IGUAL values\n     ids : ID COMA ids\n            | ID\n    \n    values : value COMA values\n           | value\n     value : INT\n              | BOOLEAN\n              | ID\n   \n        statement : TYPE PARENTESISIZQ ID PARENTESISDER\n    \n    expression   : expression RESTA expression\n                 | expression SUMA expression\n                 | expression DIVISIONENTERA expression\n                 | expression DIVISION expression\n                 | expression MULTIPLICACION expression\n                 | expression MODULO expression\n                 | expression EXPONENTE expression\n    expression : RESTA expression %prec UMENOSexpression : PARENTESISIZQ expression PARENTESISDERexpression : INT'
    
_lr_action_items = {'TYPE':([0,1,2,3,4,10,11,12,24,25,26,27,28,29,30,31,32,33,34,35,36,38,41,42,],[6,6,-2,-3,-4,-24,-5,-1,-22,-15,-16,-17,-18,-19,-20,-21,-6,-10,-11,-12,-13,-23,-14,-9,]),'RESTA':([0,1,2,3,4,7,9,10,11,12,13,14,15,16,17,18,19,22,24,25,26,27,28,29,30,31,32,33,34,35,36,38,41,42,],[9,9,-2,13,-4,9,9,-24,-5,-1,9,9,9,9,9,9,9,13,-22,-15,-16,-17,-18,-19,-20,-21,-6,-10,-11,-12,-13,-23,-14,-9,]),'PARENTESISIZQ':([0,1,2,3,4,6,7,9,10,11,12,13,14,15,16,17,18,19,24,25,26,27,28,29,30,31,32,33,34,35,36,38,41,42,],[7,7,-2,-3,-4,21,7,7,-24,-5,-1,7,7,7,7,7,7,7,-22,-15,-16,-17,-18,-19,-20,-21,-6,-10,-11,-12,-13,-23,-14,-9,]),'INT':([0,1,2,3,4,7,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,30,31,32,33,34,35,36,38,40,41,42,],[10,10,-2,-3,-4,10,10,-24,-5,-1,10,10,10,10,10,10,10,34,-22,-15,-16,-17,-18,-19,-20,-21,-6,-10,-11,-12,-13,-23,34,-14,-9,]),'PUNTO':([0,1,2,3,4,10,11,12,24,25,26,27,28,29,30,31,32,33,34,35,36,38,41,42,],[11,11,-2,-3,-4,-24,-5,-1,-22,-15,-16,-17,-18,-19,-20,-21,-6,-10,-11,-12,-13,-23,-14,-9,]),'ID':([0,1,2,3,4,10,11,12,20,21,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,40,41,42,],[8,8,-2,-3,-4,-24,-5,-1,36,37,8,-22,-15,-16,-17,-18,-19,-20,-21,-6,-10,-11,-12,-13,-23,36,-14,-9,]),'$end':([1,2,3,4,10,11,12,24,25,26,27,28,29,30,31,32,33,34,35,36,38,41,42,],[0,-2,-3,-4,-24,-5,-1,-22,-15,-16,-17,-18,-19,-20,-21,-6,-10,-11,-12,-13,-23,-14,-9,]),'SUMA':([3,10,22,24,25,26,27,28,29,30,31,38,],[14,-24,14,-22,-15,-16,-17,-18,-19,-20,-21,-23,]),'DIVISIONENTERA':([3,10,22,24,25,26,27,28,29,30,31,38,],[15,-24,15,-22,15,15,-17,-18,-19,-20,-21,-23,]),'DIVISION':([3,10,22,24,25,26,27,28,29,30,31,38,],[16,-24,16,-22,16,16,-17,-18,-19,-20,-21,-23,]),'MULTIPLICACION':([3,10,22,24,25,26,27,28,29,30,31,38,],[17,-24,17,-22,17,17,-17,-18,-19,-20,-21,-23,]),'MODULO':([3,10,22,24,25,26,27,28,29,30,31,38,],[18,-24,18,18,18,18,18,18,18,18,-21,-23,]),'EXPONENTE':([3,10,22,24,25,26,27,28,29,30,31,38,],[19,-24,19,19,19,19,19,19,19,19,19,-23,]),'IGUAL':([5,8,39,],[20,-8,-7,]),'COMA':([8,33,34,35,36,],[23,40,-11,-12,-13,]),'PARENTESISDER':([10,22,24,25,26,27,28,29,30,31,37,38,],[-24,38,-22,-15,-16,-17,-18,-19,-20,-21,41,-23,]),'BOOLEAN':([20,40,],[35,35,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statements':([0,],[1,]),'statement':([0,1,],[2,12,]),'expression':([0,1,7,9,13,14,15,16,17,18,19,],[3,3,22,24,25,26,27,28,29,30,31,]),'print':([0,1,],[4,4,]),'ids':([0,1,23,],[5,5,39,]),'values':([20,40,],[32,42,]),'value':([20,40,],[33,33,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statements","S'",1,None,None,None),
  ('statements -> statements statement','statements',2,'p_statments','parser.py',62),
  ('statements -> statement','statements',1,'p_statments','parser.py',63),
  ('statement -> expression','statement',1,'p_sentencia_expr','parser.py',75),
  ('statement -> print','statement',1,'p_sentencia_expr','parser.py',76),
  ('print -> PUNTO','print',1,'p_printVariables','parser.py',83),
  ('statement -> ids IGUAL values','statement',3,'p_statement_assign','parser.py',91),
  ('ids -> ID COMA ids','ids',3,'p_ids','parser.py',100),
  ('ids -> ID','ids',1,'p_ids','parser.py',101),
  ('values -> value COMA values','values',3,'p_values','parser.py',108),
  ('values -> value','values',1,'p_values','parser.py',109),
  ('value -> INT','value',1,'p_value','parser.py',156),
  ('value -> BOOLEAN','value',1,'p_value','parser.py',157),
  ('value -> ID','value',1,'p_value','parser.py',158),
  ('statement -> TYPE PARENTESISIZQ ID PARENTESISDER','statement',4,'p_type','parser.py',169),
  ('expression -> expression RESTA expression','expression',3,'p_expression_op','parser.py',203),
  ('expression -> expression SUMA expression','expression',3,'p_expression_op','parser.py',204),
  ('expression -> expression DIVISIONENTERA expression','expression',3,'p_expression_op','parser.py',205),
  ('expression -> expression DIVISION expression','expression',3,'p_expression_op','parser.py',206),
  ('expression -> expression MULTIPLICACION expression','expression',3,'p_expression_op','parser.py',207),
  ('expression -> expression MODULO expression','expression',3,'p_expression_op','parser.py',208),
  ('expression -> expression EXPONENTE expression','expression',3,'p_expression_op','parser.py',209),
  ('expression -> RESTA expression','expression',2,'p_expression_uminus','parser.py',242),
  ('expression -> PARENTESISIZQ expression PARENTESISDER','expression',3,'p_factor_expr','parser.py',248),
  ('expression -> INT','expression',1,'p_expression_num','parser.py',253),
]
