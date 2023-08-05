from ...libraries.transcenternal import *
from ...libraries.transcenternal_interpreter import *

X = ('v','X')
C = ('v','C')
O = ('v','O')
H = ('v','H')
F = ('v','F')

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
		('F',B0()), #フラッシュの文字
	],
	'output': 'O',
	'ops': [
		('set',O,H),
		('label','outer'),
		#フラッシュの定数初期化
		('new',F,(B0(),B0())),
		('new',F,(F,B0())),
		('new',rel(F,'1'),(B0(),B0())),
		
		('label','inner'),
		# 下2bitでABCDをとる
		('br',(char(6),B0()),
			[('br',(char(7),B0()),
				[('set',rel(F,'00'),B1())],
				[('set',rel(F,'01'),B1())],)],
			[('br',(char(7),B0()),
				[('set',rel(F,'10'),B1())],
				[('set',rel(F,'11'),B1())],)],
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
	'decl': [ #name, 初期値
		('X',B0()), #outer counter
		('C',B0()), #inner counter
		('O',B0()), #出力
		('H',('N',B0(),B0())), # outputの先端
		('F',B0()), #フラッシュの文字
	],
	'output': 'O',
	'ops': [
		('set',O,H),
		('label','outer'),
		#フラッシュの定数初期化
		('new',F,(B0(),B0())),
		('new',F,(F,B0())),
		('new',rel(F,'1'),(B0(),B0())),
		
		('label','inner'),
		# 下2bitでABCDをとる
		('br',(char(6),B0()),
			[('br',(char(7),B0()),
				[('set',rel(F,'00'),B1())],
				[('set',rel(F,'01'),B1())],)],
			[('br',(char(7),B0()),
				[('set',rel(F,'10'),B1())],
				[('set',rel(F,'11'),B1())],)],
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

_code = {
	'decl': [ # name, 初期値
		('O',('b','')), # 出力
	],
	'output': 'O',
	'ops': [
		('label','bar'),
		('label','foo'),
		('new',O,(B0(),O)),
		('gotoIfNe',(B1(),B1()),'foo'),
		('new',O,(B1(),O)),
		('gotoIfNe',(B1(),B1()),'bar'),
		('new',O,(B0(),O)),
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


