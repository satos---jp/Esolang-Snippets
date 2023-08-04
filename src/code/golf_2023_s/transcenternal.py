from ...libraries.transcenternal import *
from ...libraries.transcenternal_interpreter import *

X = ('v','X')
C = ('v','C')
O = ('v','O')
H = ('v','H')

def print_char_op(c):
	return sum([
		[
		('new',('ra',H,'1'),(B0() if c == '0' else B1(),B0())),
		('set',H,('ra',H,'1')),
		] for c in format(ord(c),'08b')[::-1]],[]
	)

def nextchar():
	return [('set',('b','1'),('b','1'*9))] #改行飛ばす

code = {
	'decl': [ #name, 初期値
		('X',B0()), #outer counter
		('C',B0()), #inner counter
		('O',B0()), #出力
		('H',('N',B0(),B0())), # outputの先端
		('F0',N(N(B0(),B0()),N(B0(),B0()))), #フラッシュの初期化定数
		('F',B0()), #フラッシュの文字
	],
	'output': 'O',
	'ops': [
		('set',O,H),
		('label','outer'),
		('set','F','F0'),
		('label','inner'),
		# 下2bitでABCDをとる
		('br',char(6),B0(),
			[('br',char(7),B0(),
				[('set',rel('F','00'),B1())],
				[('set',rel('F','01'),B1())],)],
			[('branch',char(7),B0(),
				[('set',rel('F','10'),B1())],
				[('set',rel('F','11'),B1())],)],
		),
		*nextchar(), #数字へ
		*nextchar(), #次の文字へ
		('gotoIf',(C,B0()),'inner'),
		*nextchar(), #改行飛ばす
		
		#判定
		#とりあえず文字出す
		*print_char_op('\n'),
		
		('set',X,char(0)),
		('gotoIf',(X,B0()),'outer'),
		('set',O,('ra',O,'1')),
	]
}

code = {
	'decl': [ # name, 初期値
		('O',('b','')), # 出力
		('H',('N',B0(),B0())), # outputの先端
	],
	'output': 'O',
	'ops': [
		('set',('v','O'),('v','H')),
		('br',(char(0),B0()),
			[*print_char_op('N')],
			[*print_char_op('Y')],
		),
		*print_char_op('X'),
		('set',('v','O'),('ra',('v','O'),'1')),
	]
}

_code = {
	'decl': [ # name, 初期値
		('O',('b','')), # 出力
		('H',('N',B0(),B0())), # outputの先端
	],
	'output': 'O',
	'ops': [
		('set',('v','O'),('v','H')),
		*print_char_op('Y'),
		*print_char_op('e'),
		('set',('v','O'),('ra',('v','O'),'1')),
	]
}

"""
		('br',(char(0),B0()),
			[*print_char_op('N')],
			[*print_char_op('Y')],
		),
"""
G = ('v','G')
_code = {
	'decl': [
		('O',('b','')), # 出力
		('G',('b','10011010')),
		('X',('b','01110010')),
	],
	'output': 'O',
	'ops': [
		('br',(char(0),B1()),[('set',O,G)],[('set',O,X)])
	]
}

_code = {
	'decl': [
		('O',('b','')), # 出力
	],
	'output': 'O',
	'ops': [
		('br',(B0(),B1()),[],[])
	]
}

_code = {
	'decl': [ # name, 初期値
		('O',('b','')), # 出力
		('H',('N',B0(),B0())), # outputの先端
	],
	'output': 'O',
	'ops': [
		('set',('v','O'),('v','H')),
		*print_char_op('X'),
		('set',('v','O'),('ra',('v','O'),'1')),
	]
}


_code = {
	'decl': [ # name, 初期値
		('O',('b','')), # 出力
		('H',('b','01100010' + '01100010')), # outputの先端
	],
	'output': 'O',
	'ops': [
		('set',('v','O'),('v','H')),
		('set',('v','H'),('ra',('v','H'),'11111111')),
		('set',('ra',('v','H'),'0'),B1()),
	]
}

# print(code)
# code = printFD()
# code = branchTestGraph()
g = code_to_graph(code)
# g = echoGraph()
s = graph_to_output(g)
interpreter(g,b"c2")
compile(code,'o')


