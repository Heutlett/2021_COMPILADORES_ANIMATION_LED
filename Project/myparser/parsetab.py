
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftSUMARESTAleftMULTIPLICACIONDIVISIONDIVISIONENTERArightUMENOSrightMODULOrightEXPONENTEBEGIN BLINK BOOLEAN CALL COMA CORCHETEDER CORCHETEIZQ DEL DELAY DIVISION DIVISIONENTERA DOSPUNTOS END EXPONENTE F FOR ID IF IGUAL IGUALES IN INSERT INT LEN LIST LLAVEDER LLAVEIZQ MAIN MAYORIGUAL MAYORQUE MENORIGUAL MENORQUE MIL MIN MODULO MULTIPLICACION NEG PARENTESISDER PARENTESISIZQ PRINTLED PRINTLEDX PROCEDURE PUNTO PYC RANGE RESTA SEG SHAPEC SHAPEF STEP STRING SUMA T TYPE\n    statements : empty\n               | primitive\n               | statement\n               | statements statement\n    \n    statement : expression PYC\n              | callable PYC\n              | var_assign\n              | funcionreservada\n              | procedure\n    \n    primitive : BOOLEAN\n              | INT\n              | list\n              | STRING\n    \n    ids : ID\n        | ids COMA ids\n    \n    params  : input\n    \n    input  : empty\n            | expression\n            | primitive\n            | sublist\n            | input COMA input\n    \n    var_assign : ID IGUAL expression PYC\n               | ID IGUAL primitive PYC\n               | ids IGUAL params PYC\n               | sublist IGUAL params PYC\n    \n        statement : TYPE PARENTESISIZQ ID PARENTESISDER PYC\n    \n    list  : CORCHETEIZQ params CORCHETEDER\n    \n    callable  : sublist\n    \n    index  : CORCHETEIZQ expression CORCHETEDER\n    \n    index  : CORCHETEIZQ expression COMA expression CORCHETEDER\n           | CORCHETEIZQ expression CORCHETEDER CORCHETEIZQ expression CORCHETEDER\n    \n    sublist  : ID index\n             | ID CORCHETEIZQ expression COMA expression CORCHETEDER\n    \n    expression : expression EXPONENTE expression\n               | expression MODULO expression\n               | expression MULTIPLICACION expression\n               | expression DIVISIONENTERA expression\n               | expression DIVISION expression\n               | expression SUMA expression\n               | expression RESTA expression\n    expression : PARENTESISIZQ expression PARENTESISDER\n    expression : ID\n               | INT\n    expression : RESTA expression %prec UMENOS\n    empty :\n     condicion : expression IGUALES valorIf\n                             | expression  MAYORQUE valorIf\n                             | expression  MENORQUE valorIf\n                             | expression  MENORIGUAL valorIf\n                             | expression  MAYORIGUAL valorIf\n     valorIf : BOOLEAN\n              | INT\n     funcionreservada : IF PARENTESISIZQ condicion PARENTESISDER LLAVEIZQ ordenes LLAVEDER\n   \n    procedure : PROCEDURE ID PARENTESISIZQ params PARENTESISDER LLAVEIZQ ordenes LLAVEDER PYC\n                | PROCEDURE MAIN PARENTESISIZQ params PARENTESISDER LLAVEIZQ ordenes LLAVEDER PYC\n    \n    funcionreservada : CALL ID PARENTESISIZQ params PARENTESISDER PYC\n    \n    funcionreservada : FOR expression IN INT LLAVEIZQ ordenes LLAVEDER\n                        | FOR expression IN expression LLAVEIZQ ordenes LLAVEDER\n    \n    ordenes : statement\n                       | ordenes statement\n                       | ordenes funcionreservada\n                       | funcionreservada\n\n   \n    funcionreservada : BLINK PARENTESISIZQ params PARENTESISDER PYC\n    \n    funcionreservada : DELAY PARENTESISIZQ params PARENTESISDER PYC\n    \n    funcionreservada : PRINTLED PARENTESISIZQ params PARENTESISDER PYC\n    \n    funcionreservada : PRINTLEDX PARENTESISIZQ params PARENTESISDER PYC\n    '
    
_lr_action_items = {'TYPE':([0,1,2,3,4,5,6,7,8,11,12,13,29,31,39,79,96,97,101,102,118,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[14,14,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,-4,-5,-6,-27,-22,-23,-25,-24,-26,14,14,14,-63,-64,-65,-66,14,-59,-8,-56,14,14,14,14,-53,-60,-8,-58,-57,14,14,-54,-55,]),'PARENTESISIZQ':([0,1,2,3,4,5,6,7,8,11,12,13,14,15,17,18,21,23,24,25,26,27,29,31,32,33,34,35,36,37,38,39,43,45,55,56,58,59,61,62,63,64,65,66,79,80,87,88,93,94,96,97,98,101,102,118,120,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[15,15,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,40,15,15,15,58,15,61,62,63,64,-4,-5,15,15,15,15,15,15,15,-6,15,15,15,15,15,87,15,15,15,15,93,94,-27,15,15,15,15,15,-22,-23,15,-25,-24,-26,15,15,15,15,-63,-64,-65,-66,15,-59,-8,-56,15,15,15,15,-53,-60,-8,-58,-57,15,15,-54,-55,]),'ID':([0,1,2,3,4,5,6,7,8,11,12,13,15,17,18,22,23,28,29,31,32,33,34,35,36,37,38,39,40,43,45,55,56,57,58,61,62,63,64,79,80,87,88,93,94,96,97,98,101,102,118,120,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[16,16,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,42,52,42,59,42,65,-4,-5,42,42,42,42,42,42,42,-6,74,42,42,52,52,84,42,52,52,52,52,-27,52,52,42,52,52,-22,-23,42,-25,-24,-26,42,16,16,16,-63,-64,-65,-66,16,-59,-8,-56,16,16,16,16,-53,-60,-8,-58,-57,16,16,-54,-55,]),'INT':([0,1,2,3,4,5,6,7,8,11,12,13,15,17,18,23,29,31,32,33,34,35,36,37,38,39,43,45,55,56,58,61,62,63,64,79,80,87,88,93,94,96,97,98,101,102,104,105,106,107,108,118,120,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[6,30,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,30,53,30,30,-4,-5,30,30,30,30,30,30,30,-6,53,30,53,53,30,53,53,53,53,-27,53,53,111,53,53,-22,-23,30,-25,-24,124,124,124,124,124,-26,30,30,30,30,-63,-64,-65,-66,30,-59,-8,-56,30,30,30,30,-53,-60,-8,-58,-57,30,30,-54,-55,]),'RESTA':([0,1,2,3,4,5,6,7,8,9,11,12,13,15,16,17,18,23,29,30,31,32,33,34,35,36,37,38,39,41,42,43,45,49,52,53,54,55,56,58,60,61,62,63,64,67,68,69,70,71,72,73,75,76,78,79,80,86,87,88,93,94,96,97,98,101,102,110,111,118,119,120,121,130,131,132,133,134,135,139,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[18,18,-1,-2,-3,-10,-11,-12,-13,38,-7,-8,-9,18,-42,18,18,18,-4,-43,-5,18,18,18,18,18,18,18,-6,38,-42,18,18,38,-42,-43,-44,18,18,18,38,18,18,18,18,-34,-35,-36,-37,-38,-39,-40,-41,38,38,-27,18,38,18,18,18,18,-22,-23,18,-25,-24,38,-43,-26,38,18,18,18,18,-63,-64,-65,-66,38,18,-59,-8,-56,18,18,18,18,-53,-60,-8,-58,-57,18,18,-54,-55,]),'IF':([0,1,2,3,4,5,6,7,8,11,12,13,29,31,39,79,96,97,101,102,118,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[21,21,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,-4,-5,-6,-27,-22,-23,-25,-24,-26,21,21,21,-63,-64,-65,-66,21,-59,-8,-56,21,21,21,21,-53,-60,-8,-58,-57,21,21,-54,-55,]),'CALL':([0,1,2,3,4,5,6,7,8,11,12,13,29,31,39,79,96,97,101,102,118,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[22,22,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,-4,-5,-6,-27,-22,-23,-25,-24,-26,22,22,22,-63,-64,-65,-66,22,-59,-8,-56,22,22,22,22,-53,-60,-8,-58,-57,22,22,-54,-55,]),'FOR':([0,1,2,3,4,5,6,7,8,11,12,13,29,31,39,79,96,97,101,102,118,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[23,23,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,-4,-5,-6,-27,-22,-23,-25,-24,-26,23,23,23,-63,-64,-65,-66,23,-59,-8,-56,23,23,23,23,-53,-60,-8,-58,-57,23,23,-54,-55,]),'BLINK':([0,1,2,3,4,5,6,7,8,11,12,13,29,31,39,79,96,97,101,102,118,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[24,24,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,-4,-5,-6,-27,-22,-23,-25,-24,-26,24,24,24,-63,-64,-65,-66,24,-59,-8,-56,24,24,24,24,-53,-60,-8,-58,-57,24,24,-54,-55,]),'DELAY':([0,1,2,3,4,5,6,7,8,11,12,13,29,31,39,79,96,97,101,102,118,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[25,25,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,-4,-5,-6,-27,-22,-23,-25,-24,-26,25,25,25,-63,-64,-65,-66,25,-59,-8,-56,25,25,25,25,-53,-60,-8,-58,-57,25,25,-54,-55,]),'PRINTLED':([0,1,2,3,4,5,6,7,8,11,12,13,29,31,39,79,96,97,101,102,118,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[26,26,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,-4,-5,-6,-27,-22,-23,-25,-24,-26,26,26,26,-63,-64,-65,-66,26,-59,-8,-56,26,26,26,26,-53,-60,-8,-58,-57,26,26,-54,-55,]),'PRINTLEDX':([0,1,2,3,4,5,6,7,8,11,12,13,29,31,39,79,96,97,101,102,118,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[27,27,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,-4,-5,-6,-27,-22,-23,-25,-24,-26,27,27,27,-63,-64,-65,-66,27,-59,-8,-56,27,27,27,27,-53,-60,-8,-58,-57,27,27,-54,-55,]),'PROCEDURE':([0,1,2,3,4,5,6,7,8,11,12,13,29,31,39,79,96,97,101,102,118,121,130,131,132,133,134,135,140,141,142,143,144,145,146,147,149,150,151,152,153,154,155,158,159,],[28,28,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,-4,-5,-6,-27,-22,-23,-25,-24,-26,28,28,28,-63,-64,-65,-66,28,-59,-8,-56,28,28,28,28,-53,-60,-8,-58,-57,28,28,-54,-55,]),'$end':([0,1,2,3,4,5,6,7,8,11,12,13,29,31,39,79,96,97,101,102,118,132,133,134,135,143,149,152,153,158,159,],[-45,0,-1,-2,-3,-10,-11,-12,-13,-7,-8,-9,-4,-5,-6,-27,-22,-23,-25,-24,-26,-63,-64,-65,-66,-56,-53,-58,-57,-54,-55,]),'BOOLEAN':([0,17,43,55,56,61,62,63,64,80,87,93,94,104,105,106,107,108,],[5,5,5,5,5,5,5,5,5,5,5,5,5,123,123,123,123,123,]),'STRING':([0,17,43,55,56,61,62,63,64,80,87,93,94,],[8,8,8,8,8,8,8,8,8,8,8,8,8,]),'CORCHETEIZQ':([0,16,17,43,52,55,56,61,62,63,64,80,87,93,94,99,],[17,45,17,17,45,17,17,17,17,17,17,17,17,17,17,120,]),'COMA':([5,7,8,16,17,20,30,42,44,47,48,49,50,51,52,53,54,55,56,61,62,63,64,67,68,69,70,71,72,73,75,78,79,80,83,84,87,93,94,99,100,138,148,],[-10,-12,-13,-14,-45,57,-43,-42,-32,80,-17,-18,-19,-20,-42,-11,-44,-45,-45,-45,-45,-45,-45,-34,-35,-36,-37,-38,-39,-40,-41,98,-27,-45,57,-14,-45,-45,-45,-29,80,-30,-31,]),'CORCHETEDER':([5,7,8,17,30,42,44,46,47,48,49,50,51,52,53,54,67,68,69,70,71,72,73,75,78,79,80,99,100,119,138,139,148,],[-10,-12,-13,-45,-43,-42,-32,79,-16,-17,-18,-19,-20,-42,-11,-44,-34,-35,-36,-37,-38,-39,-40,-41,99,-27,-45,-29,-21,138,-30,148,-31,]),'PYC':([5,6,7,8,9,10,16,19,30,42,44,47,48,49,50,51,52,53,54,55,56,67,68,69,70,71,72,73,75,76,77,79,80,81,82,95,99,100,112,113,114,115,129,138,148,156,157,],[-10,-43,-12,-13,31,39,-42,-28,-43,-42,-32,-16,-17,-18,-19,-20,-42,-11,-44,-45,-45,-34,-35,-36,-37,-38,-39,-40,-41,96,97,-27,-45,101,102,118,-29,-21,132,133,134,135,143,-30,-31,158,159,]),'PARENTESISDER':([5,7,8,30,41,42,44,47,48,49,50,51,52,53,54,61,62,63,64,67,68,69,70,71,72,73,74,75,79,80,85,87,89,90,91,92,93,94,99,100,109,116,117,122,123,124,125,126,127,128,138,148,],[-10,-12,-13,-43,75,-42,-32,-16,-17,-18,-19,-20,-42,-11,-44,-45,-45,-45,-45,-34,-35,-36,-37,-38,-39,-40,95,-41,-27,-45,103,-45,112,113,114,115,-45,-45,-29,-21,129,136,137,-46,-51,-52,-47,-48,-49,-50,-30,-31,]),'EXPONENTE':([6,9,16,30,41,42,49,52,53,54,60,67,68,69,70,71,72,73,75,76,78,86,110,111,119,139,],[-43,32,-42,-43,32,-42,32,-42,-43,32,32,32,32,32,32,32,32,32,-41,32,32,32,32,-43,32,32,]),'MODULO':([6,9,16,30,41,42,49,52,53,54,60,67,68,69,70,71,72,73,75,76,78,86,110,111,119,139,],[-43,33,-42,-43,33,-42,33,-42,-43,33,33,-34,33,33,33,33,33,33,-41,33,33,33,33,-43,33,33,]),'MULTIPLICACION':([6,9,16,30,41,42,49,52,53,54,60,67,68,69,70,71,72,73,75,76,78,86,110,111,119,139,],[-43,34,-42,-43,34,-42,34,-42,-43,-44,34,-34,-35,-36,-37,-38,34,34,-41,34,34,34,34,-43,34,34,]),'DIVISIONENTERA':([6,9,16,30,41,42,49,52,53,54,60,67,68,69,70,71,72,73,75,76,78,86,110,111,119,139,],[-43,35,-42,-43,35,-42,35,-42,-43,-44,35,-34,-35,-36,-37,-38,35,35,-41,35,35,35,35,-43,35,35,]),'DIVISION':([6,9,16,30,41,42,49,52,53,54,60,67,68,69,70,71,72,73,75,76,78,86,110,111,119,139,],[-43,36,-42,-43,36,-42,36,-42,-43,-44,36,-34,-35,-36,-37,-38,36,36,-41,36,36,36,36,-43,36,36,]),'SUMA':([6,9,16,30,41,42,49,52,53,54,60,67,68,69,70,71,72,73,75,76,78,86,110,111,119,139,],[-43,37,-42,-43,37,-42,37,-42,-43,-44,37,-34,-35,-36,-37,-38,-39,-40,-41,37,37,37,37,-43,37,37,]),'LLAVEDER':([11,13,31,39,96,97,101,102,118,132,133,134,135,140,141,142,143,144,145,149,150,151,152,153,154,155,158,159,],[-7,-9,-5,-6,-22,-23,-25,-24,-26,-63,-64,-65,-66,149,-59,-8,-56,152,153,-53,-60,-8,-58,-57,156,157,-54,-55,]),'IGUAL':([16,19,20,44,83,84,99,138,148,],[43,55,56,-32,-15,-14,-29,-30,-31,]),'MAIN':([28,],[66,]),'IN':([30,42,54,60,67,68,69,70,71,72,73,75,],[-43,-42,-44,88,-34,-35,-36,-37,-38,-39,-40,-41,]),'IGUALES':([30,42,54,67,68,69,70,71,72,73,75,86,],[-43,-42,-44,-34,-35,-36,-37,-38,-39,-40,-41,104,]),'MAYORQUE':([30,42,54,67,68,69,70,71,72,73,75,86,],[-43,-42,-44,-34,-35,-36,-37,-38,-39,-40,-41,105,]),'MENORQUE':([30,42,54,67,68,69,70,71,72,73,75,86,],[-43,-42,-44,-34,-35,-36,-37,-38,-39,-40,-41,106,]),'MENORIGUAL':([30,42,54,67,68,69,70,71,72,73,75,86,],[-43,-42,-44,-34,-35,-36,-37,-38,-39,-40,-41,107,]),'MAYORIGUAL':([30,42,54,67,68,69,70,71,72,73,75,86,],[-43,-42,-44,-34,-35,-36,-37,-38,-39,-40,-41,108,]),'LLAVEIZQ':([30,42,54,67,68,69,70,71,72,73,75,103,110,111,136,137,],[-43,-42,-44,-34,-35,-36,-37,-38,-39,-40,-41,121,130,131,146,147,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statements':([0,],[1,]),'empty':([0,17,55,56,61,62,63,64,80,87,93,94,],[2,48,48,48,48,48,48,48,48,48,48,48,]),'primitive':([0,17,43,55,56,61,62,63,64,80,87,93,94,],[3,50,77,50,50,50,50,50,50,50,50,50,50,]),'statement':([0,1,121,130,131,140,144,145,146,147,154,155,],[4,29,141,141,141,150,150,150,141,141,150,150,]),'list':([0,17,43,55,56,61,62,63,64,80,87,93,94,],[7,7,7,7,7,7,7,7,7,7,7,7,7,]),'expression':([0,1,15,17,18,23,32,33,34,35,36,37,38,43,45,55,56,58,61,62,63,64,80,87,88,93,94,98,120,121,130,131,140,144,145,146,147,154,155,],[9,9,41,49,54,60,67,68,69,70,71,72,73,76,78,49,49,86,49,49,49,49,49,49,110,49,49,119,139,9,9,9,9,9,9,9,9,9,9,]),'callable':([0,1,121,130,131,140,144,145,146,147,154,155,],[10,10,10,10,10,10,10,10,10,10,10,10,]),'var_assign':([0,1,121,130,131,140,144,145,146,147,154,155,],[11,11,11,11,11,11,11,11,11,11,11,11,]),'funcionreservada':([0,1,121,130,131,140,144,145,146,147,154,155,],[12,12,142,142,142,151,151,151,142,142,151,151,]),'procedure':([0,1,121,130,131,140,144,145,146,147,154,155,],[13,13,13,13,13,13,13,13,13,13,13,13,]),'sublist':([0,1,17,55,56,61,62,63,64,80,87,93,94,121,130,131,140,144,145,146,147,154,155,],[19,19,51,51,51,51,51,51,51,51,51,51,51,19,19,19,19,19,19,19,19,19,19,]),'ids':([0,1,57,121,130,131,140,144,145,146,147,154,155,],[20,20,83,20,20,20,20,20,20,20,20,20,20,]),'index':([16,52,],[44,44,]),'params':([17,55,56,61,62,63,64,87,93,94,],[46,81,82,89,90,91,92,109,116,117,]),'input':([17,55,56,61,62,63,64,80,87,93,94,],[47,47,47,47,47,47,47,100,47,47,47,]),'condicion':([58,],[85,]),'valorIf':([104,105,106,107,108,],[122,125,126,127,128,]),'ordenes':([121,130,131,146,147,],[140,144,145,154,155,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statements","S'",1,None,None,None),
  ('statements -> empty','statements',1,'p_statements','parser.py',41),
  ('statements -> primitive','statements',1,'p_statements','parser.py',42),
  ('statements -> statement','statements',1,'p_statements','parser.py',43),
  ('statements -> statements statement','statements',2,'p_statements','parser.py',44),
  ('statement -> expression PYC','statement',2,'p_operation','parser.py',60),
  ('statement -> callable PYC','statement',2,'p_operation','parser.py',61),
  ('statement -> var_assign','statement',1,'p_operation','parser.py',62),
  ('statement -> funcionreservada','statement',1,'p_operation','parser.py',63),
  ('statement -> procedure','statement',1,'p_operation','parser.py',64),
  ('primitive -> BOOLEAN','primitive',1,'p_primitive_var','parser.py',72),
  ('primitive -> INT','primitive',1,'p_primitive_var','parser.py',73),
  ('primitive -> list','primitive',1,'p_primitive_var','parser.py',74),
  ('primitive -> STRING','primitive',1,'p_primitive_var','parser.py',75),
  ('ids -> ID','ids',1,'p_ids','parser.py',84),
  ('ids -> ids COMA ids','ids',3,'p_ids','parser.py',85),
  ('params -> input','params',1,'p_params','parser.py',96),
  ('input -> empty','input',1,'p_input','parser.py',109),
  ('input -> expression','input',1,'p_input','parser.py',110),
  ('input -> primitive','input',1,'p_input','parser.py',111),
  ('input -> sublist','input',1,'p_input','parser.py',112),
  ('input -> input COMA input','input',3,'p_input','parser.py',113),
  ('var_assign -> ID IGUAL expression PYC','var_assign',4,'p_var_assign','parser.py',128),
  ('var_assign -> ID IGUAL primitive PYC','var_assign',4,'p_var_assign','parser.py',129),
  ('var_assign -> ids IGUAL params PYC','var_assign',4,'p_var_assign','parser.py',130),
  ('var_assign -> sublist IGUAL params PYC','var_assign',4,'p_var_assign','parser.py',131),
  ('statement -> TYPE PARENTESISIZQ ID PARENTESISDER PYC','statement',5,'p_var_type','parser.py',149),
  ('list -> CORCHETEIZQ params CORCHETEDER','list',3,'p_list_assign','parser.py',162),
  ('callable -> sublist','callable',1,'p_callable','parser.py',174),
  ('index -> CORCHETEIZQ expression CORCHETEDER','index',3,'p_index_1','parser.py',183),
  ('index -> CORCHETEIZQ expression COMA expression CORCHETEDER','index',5,'p_index_2','parser.py',191),
  ('index -> CORCHETEIZQ expression CORCHETEDER CORCHETEIZQ expression CORCHETEDER','index',6,'p_index_2','parser.py',192),
  ('sublist -> ID index','sublist',2,'p_sublist','parser.py',205),
  ('sublist -> ID CORCHETEIZQ expression COMA expression CORCHETEDER','sublist',6,'p_sublist','parser.py',206),
  ('expression -> expression EXPONENTE expression','expression',3,'p_expression','parser.py',280),
  ('expression -> expression MODULO expression','expression',3,'p_expression','parser.py',281),
  ('expression -> expression MULTIPLICACION expression','expression',3,'p_expression','parser.py',282),
  ('expression -> expression DIVISIONENTERA expression','expression',3,'p_expression','parser.py',283),
  ('expression -> expression DIVISION expression','expression',3,'p_expression','parser.py',284),
  ('expression -> expression SUMA expression','expression',3,'p_expression','parser.py',285),
  ('expression -> expression RESTA expression','expression',3,'p_expression','parser.py',286),
  ('expression -> PARENTESISIZQ expression PARENTESISDER','expression',3,'p_expression_parentesis','parser.py',296),
  ('expression -> ID','expression',1,'p_expression_var','parser.py',303),
  ('expression -> INT','expression',1,'p_expression_var','parser.py',304),
  ('expression -> RESTA expression','expression',2,'p_expression_uminus','parser.py',311),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',318),
  ('condicion -> expression IGUALES valorIf','condicion',3,'p_condicion','parser.py',325),
  ('condicion -> expression MAYORQUE valorIf','condicion',3,'p_condicion','parser.py',326),
  ('condicion -> expression MENORQUE valorIf','condicion',3,'p_condicion','parser.py',327),
  ('condicion -> expression MENORIGUAL valorIf','condicion',3,'p_condicion','parser.py',328),
  ('condicion -> expression MAYORIGUAL valorIf','condicion',3,'p_condicion','parser.py',329),
  ('valorIf -> BOOLEAN','valorIf',1,'p_valorIf','parser.py',335),
  ('valorIf -> INT','valorIf',1,'p_valorIf','parser.py',336),
  ('funcionreservada -> IF PARENTESISIZQ condicion PARENTESISDER LLAVEIZQ ordenes LLAVEDER','funcionreservada',7,'p_if','parser.py',343),
  ('procedure -> PROCEDURE ID PARENTESISIZQ params PARENTESISDER LLAVEIZQ ordenes LLAVEDER PYC','procedure',9,'p_procedure','parser.py',351),
  ('procedure -> PROCEDURE MAIN PARENTESISIZQ params PARENTESISDER LLAVEIZQ ordenes LLAVEDER PYC','procedure',9,'p_procedure','parser.py',352),
  ('funcionreservada -> CALL ID PARENTESISIZQ params PARENTESISDER PYC','funcionreservada',6,'p_call','parser.py',360),
  ('funcionreservada -> FOR expression IN INT LLAVEIZQ ordenes LLAVEDER','funcionreservada',7,'p_for','parser.py',368),
  ('funcionreservada -> FOR expression IN expression LLAVEIZQ ordenes LLAVEDER','funcionreservada',7,'p_for','parser.py',369),
  ('ordenes -> statement','ordenes',1,'p_ordenes','parser.py',378),
  ('ordenes -> ordenes statement','ordenes',2,'p_ordenes','parser.py',379),
  ('ordenes -> ordenes funcionreservada','ordenes',2,'p_ordenes','parser.py',380),
  ('ordenes -> funcionreservada','ordenes',1,'p_ordenes','parser.py',381),
  ('funcionreservada -> BLINK PARENTESISIZQ params PARENTESISDER PYC','funcionreservada',5,'p_blink','parser.py',405),
  ('funcionreservada -> DELAY PARENTESISIZQ params PARENTESISDER PYC','funcionreservada',5,'p_delay','parser.py',456),
  ('funcionreservada -> PRINTLED PARENTESISIZQ params PARENTESISDER PYC','funcionreservada',5,'p_PrintLed','parser.py',488),
  ('funcionreservada -> PRINTLEDX PARENTESISIZQ params PARENTESISDER PYC','funcionreservada',5,'p_PrintLedX','parser.py',520),
]
