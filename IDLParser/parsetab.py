
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xbb1\xf9\x879\x04\x8d;g\xbcr\xa4^\xc1\x9dh'
    
_lr_action_items = {'Map':([4,15,16,17,22,],[6,6,6,6,6,]),'GT':([8,9,10,12,20,21,23,24,25,26,],[-7,-6,-8,-5,23,24,-9,-10,26,-11,]),'Set':([4,15,16,17,22,],[7,7,7,7,7,]),'String':([4,15,16,17,22,],[8,8,8,8,8,]),'SEMICOLON':([1,],[4,]),'intconstant':([0,5,],[1,1,]),'Double':([4,15,16,17,22,],[9,9,9,9,9,]),'Object':([4,15,16,17,22,],[10,10,10,10,10,]),'List':([4,15,16,17,22,],[11,11,11,11,11,]),'LT':([6,7,11,],[15,16,17,]),'Boolean':([4,15,16,17,22,],[12,12,12,12,12,]),'COMMA':([2,3,8,9,10,12,14,18,19,23,24,26,],[5,-3,-7,-6,-8,-5,-4,-2,22,-9,-10,-11,]),'identifier':([8,9,10,12,13,23,24,26,],[-7,-6,-8,-5,18,-9,-10,-11,]),'$end':([2,3,14,18,],[0,-3,-4,-2,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'declaration':([0,5,],[3,14,]),'type':([4,15,16,17,22,],[13,19,20,21,25,]),'declaration_list':([0,],[2,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> declaration_list","S'",1,None,None,None),
  ('assignment -> identifier ASSIGN intconstant','assignment',3,'p_assignment','<stdin>',2),
  ('declaration -> intconstant SEMICOLON type identifier','declaration',4,'p_declaration','<stdin>',2),
  ('declaration_list -> declaration','declaration_list',1,'p_declaration_list','<stdin>',2),
  ('declaration_list -> declaration_list COMMA declaration','declaration_list',3,'p_declaration_list','<stdin>',3),
  ('type -> Boolean','type',1,'p_type','<stdin>',2),
  ('type -> Double','type',1,'p_type','<stdin>',3),
  ('type -> String','type',1,'p_type','<stdin>',4),
  ('type -> Object','type',1,'p_type','<stdin>',5),
  ('type -> Set LT type GT','type',4,'p_type','<stdin>',6),
  ('type -> List LT type GT','type',4,'p_type','<stdin>',7),
  ('type -> Map LT type COMMA type GT','type',6,'p_type','<stdin>',8),
]
