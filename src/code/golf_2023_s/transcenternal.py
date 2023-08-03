from ...libraries.transcenternal import *

code = {
	'decl': [ #name, 初期値
		('x',B0()),
		('cnt',B0()),
		('O',B0()), #出力
		('F0',N(N(B0(),B0()),N(B0(),B0()))), #フラッシュの初期化定数
		('F',B0()), #フラッシュの文字
	],
	'output': 'O',
	'ops': [
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
		('set',char(0),char(8)), #数字へ
		('set',char(0),char(8)), #次の文字へ
		('gotoIf',('cnt',B0()),'inner'),
		('set',char(0),char(8)), #改行飛ばす
		
		#判定
		#とりあえず文字出す
		
		
		
		
		('load','x',char(0)),
		('gotoIf',('x',B0()),'outer'),
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
		*sum([
			[
			('new',('ra',('v','H'),'1'),(B0() if c == '0' else B1(),B0())),
			('set',('v','H'),('ra',('v','H'),'1')),
			] for c in ('01000110'[::-1] + '01000100'[::-1])],[]
		),
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
# code = printFJ()

compile(code,'o')


