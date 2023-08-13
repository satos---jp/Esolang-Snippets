from ...libraries.transcenternal import *
from ...libraries.transcenternal_interpreter import *

X = ('v','X')
C = ('v','C')
C0 = var('C0')
O = ('v','O')
H = ('v','H')
F = ('v','F')
T = var('T')
S = var('S')

DEBUG=False

def print_char_op(c):
	return sum([
		[
		('new',('ra',H,'1'),(B0() if c == '0' else B1(),B0())),
		('set',H,('ra',H,'1')),
		] for c in format(ord(c),'08b')[::-1]],[]
	)

def print_char_debug_op(c):
	if DEBUG:
		return print_char_op(c)
	else:
		return []

def nextchar():
	return [('set',('b','1'),('b','1'*9))] #改行飛ばす

code = {
	'decl': [ #name, 初期値
		('X',B0()), #outer counter
		('C',B0()), #inner counter
		('C0',('b','00000')), # counter for C
		('O',B0()), #出力
		('H',New(B0(),B0())), # outputの先端
		('F',B0()), #フラッシュ判定用
		('T',B0()), #outer counter
		('S',B0()), #ストレート判定用
	],
	'output': 'O',
	'ops': [
		('set',O,H),
		('label','outer'),
		#カウンタリセット
		('set',C,C0),
		
		#フラッシュの定数初期化
		('new',F,(B0(),B0())),
		('new',F,(B0(),F)),
		('new',F,(B0(),F)),
		('new',F,(B0(),F)),
		#ストレートの定数初期化
		('new',S,(B0(),B0())),
		('new',S,(B0(),S)),
		('new',S,(B0(),S)),
		('new',S,(B0(),S)),
		('new',S,(B0(),S)),

		('label','inner'),
		# 下2bitでABCDをとる
		('br',(char(0),B0()),
			[('br',(char(1),B0()),
				[('set',rel(F,'0'),B1())],
				[('set',rel(F,'10'),B1())],)],
			[('br',(char(1),B0()),
				[('set',rel(F,'110'),B1())],
				[('set',rel(F,'1110'),B1())],)],
		),

		*nextchar(), #数字へ
		# 1,10,11,100,101
		('br',(char(2),B0()),
			[('br',(char(1),B0()),
				[('set',rel(S,'0'),B1())],
				[('br',(char(0),B0()),
					[('set',rel(S,'10'),B1())],
					[('set',rel(S,'110'),B1())],)],)],
			[('br',(char(0),B0()),
				[('set',rel(S,'1110'),B1())],
				[('set',rel(S,'11110'),B1())],)],
		),

		*print_char_debug_op('R'),
		*nextchar(), #次の文字へ
		('set',C,rel(C,'1')),
		('gotoIfNe',(C,B0()),'inner'),
		*nextchar(), #改行飛ばす
		
		# F判定
		('set',T,B0()),
		('label','checkF'),
		('br',(rel(F,'0'),B0()),[*print_char_debug_op('D'),],[
			*print_char_debug_op('X'),
			('br',(T,B0()),[
				('set',T,B1()),
			],[
				('set',T,('b','00')),
			]),]),
		('set',F,rel(F,'1')),
		('gotoIfNe',(F,B0()),'checkF'),
	
		('br',(T,B1()),[
			*print_char_op('F'),
		],[]),
		# S判定
		('set',T,B0()),
		('label','checkS'),
		('br',(rel(S,'0'),B1()),[
			*print_char_debug_op('Y'),
		],[
			*print_char_debug_op('N'),
			('set',T,B1()),
		]),
		('set',S,rel(S,'1')),
		('gotoIfNe',(S,B0()),'checkS'),
	
		('br',(T,B0()),[
			*print_char_op('S'),
		],[]),
		# 改行
		*print_char_op('\n'),

#		('set',X,char(1)),
		('gotoIfNe',(('b','1'),B0()),'outer'),
		('set',O,('ra',O,'1')),
	]
}

# print(code)
# code = printFD()
# code = branchTestGraph()
g = code_to_graph(code)
# g = echoGraph()
s = graph_to_output(g)
#interpreter(g,b"A1A2A3A4A4\n")
interpreter(g,b"A1A2A3A4A4\nB5B3B4B2B1\n")
compile(code,'o')


