from transcenternal import *
from transcenternal_interpreter import interpreter

def var(x):
	return ('v',x)

def echoGraph():
	res = {
		0: {
			0: {}, #B0
			1: {}, #B1
		}
	}
	B0 = res[0][0]
	B1 = res[0][1]
	B0[0] = B0[1] = B0
	B1[0] = B1[1] = B1
	res[1] = B0
	return res

def printFJ():
	sample = {
		'decl': [ # name, 初期値
#			('O',('b','01001110'[::-1])), #出力
			('O',('b','01000110'[::-1] + '01001010'[::-1])), #出力
#			('P',('b','01000101')),
		],
		'output': 'O',
		'ops': [
		]
	}
	return sample

def printG():
	code = {
		'decl': [ # name, 初期値
			('O',('b','')), # 出力
		],
		'output': 'O',
		'ops': [
			('new',('v','O'),(B0(),('v','O'))),
			('new',('v','O'),(B1(),('v','O'))),
			('new',('v','O'),(B0(),('v','O'))),
			('new',('v','O'),(B0(),('v','O'))),
			('new',('v','O'),(B0(),('v','O'))),
			('new',('v','O'),(B1(),('v','O'))),
			('new',('v','O'),(B1(),('v','O'))),
			('new',('v','O'),(B1(),('v','O'))),
		]
	}
	return code

def printFD():
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
	return code

def Check_LSB_1():
	code = {
		'decl': [
			('O',('b','')), # 出力
			('G',('b','10011010')),
			('X',('b','01110010')),
		],
		'output': 'O',
		'ops': [
			('br',(char(0),B1()),[('set',('v','O'),('v','G'))],[('set',('v','O'),('v','X'))])
		]
	}
	return code

def test_br():
	G = var('G')
	O = var('O')
	X = var('X')
	code = {
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
	return code

def GotoIf():
	O = var('O')
	C = var('C')
	T = var('T')
	Y = var('Y')
	code = {
		'decl': [
			('O',B0()), # 出力
			('Y',('b','10011010')),
			('T',B0()),
			('C',('b','00000')),
		],
		'output': 'O',
		'ops': [
			('label','loop'),
				('set',T,Y),
				('label','copyS'),
					('new',O,(rel(T,'0'),O)),
					('set',T,rel(T,'1')),
					('gotoIfNe',(T,B0()),'copyS'),
				('set',C,rel(C,'1')),
				('gotoIfNe',(C,B0()),'loop'),
		]
	}
	return code

def main():
	tests = [
#		(('c',test_br()),b'',b''),
		(('c',GotoIf()),b'',b''),
	]
	
	for (ty,d),i,o in tests:
		if ty == 'c':
			g = code_to_graph(d)
		else:
			g = d
		
		_ = graph_to_output(g)
		o = interpreter(g,i)
	

if __name__ == '__main__':
	main()
