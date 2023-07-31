from ...libraries import transcenternal

code = {
	'decl': [ #name, 初期値
		('x',B0()),
		('cnt',B0()),
		('O',B0()), #出力
		('F0',N(N(B0(),B0()),N(B0(),B0()))), #フラッシュの初期化定数
		('F',B0()), #フラッシュ用の配列
	],
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


