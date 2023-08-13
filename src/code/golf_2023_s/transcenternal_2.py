from ...libraries.transcenternal import *
from ...libraries.transcenternal_interpreter import *

C = ('v','C')
C0 = var('C0')
H = ('v','H')
F = ('v','F')
T = var('T')
S = var('S')
M = var('M')

DEBUG=False

def print_char_debug_op(c):
	if DEBUG:
		return []
	else:
		return []

code = {
	'decl': [ #name, 初期値
		('C',B0()), #inner counter
		('C0',('b','00010')), # counter for C
		('M',B0()), # 現在の2byteの先頭を覚えておく
		('F',B0()), #フラッシュ判定用
		('T',B0()), #outer counter
		('S',B0()), #ストレート判定用
		('H',B0()), #Output保存
	],
	'output': None,
	'ops': [
		('set',H,('b','1')),
		('label','outer'),
		#カウンタリセット
		('set',C,C0),
		
		#フラッシュの定数初期化
		('set',F,B1()),
		#ストレートの定数初期化
		('new',S,(B0(),B0())),
		('new',S,(B0(),S)),
		('new',S,(B0(),S)),
		('new',S,(B0(),S)),
		('new',S,(B0(),S)),

		('label','inner'),
		('set',M,('b','1')),
		# フラッシュ計算
		# 下2bitでABCDをとる
		('br',(char(0),char(16)),[],[
			('set',F,B0()),
		]),
		('br',(char(1),char(17)),[],[
			('set',F,B0()),
		]),
		# Cが1ならフラッシュ判定までする
		('br',(rel(C,'0'),B1()),[
			('set',rel(M,'110'),F), #Fなら1になってるbit目
			('set',rel(M,'10'),B1()),
			('set',rel(M,'0'),B0()),
		],[]),

		('set',('b','1'),('b','1'*9)), #数字へ
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
		('set',('b','1'),('b','1'*9)), #次の文字へ
		('set',C,rel(C,'1')),
		('gotoIfNe',(C,B0()),'inner'),
		('set',('b','1'),('b','1'*9)), #改行飛ばす

		# S判定
		('set',T,B1()),
		('label','checkS'),
		('br',(rel(S,'0'),B1()),[
			*print_char_debug_op('Y'),
		],[
			*print_char_debug_op('N'),
			('set',T,B0()),
		]),
		('set',S,rel(S,'1')),
		('gotoIfNe',(S,B0()),'checkS'),

		('set',rel(M,'11110'),T), #Sなら1になってるbit目
		('set',rel(M,'10'),B1()),
		('set',rel(M,'0'),B1()),

#		('set',X,char(1)),
		('gotoIfNe',(('b','1'),B0()),'outer'),
		('set',('b','1'),H),
	]
}

# print(code)
# code = printFD()
# code = branchTestGraph()
g = code_to_graph(code)
# g = echoGraph()
s = graph_to_output(g)
#interpreter(g,b"A1A2A3A4A4\n")
interpreter(g,b"A1A2A3A4A4\nB5B3B4B2B1\nA1A2D3A5A4\n")
compile(code,'o')


