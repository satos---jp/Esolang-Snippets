
"""

 root -1-> input/output
  \
   \--0->+-0->+-0-> B0
         |     \-1-> B1
         1
         |
         v
         +--0-->+--0--> current op
         |      |
         1      \--1--> data
         |
         v
       next op

input :: c1 -1-> c2 ... cn -1-> B0
         0|      0| 
          v       v
        B0/B1   B0/B1
 
 000 :: B0
 001 :: B1
 01  :: 
   if === B0 then halt
 0100 ::
 	 if ==== B0  then [01010] <- [01011]
 	 elif === B1 then [01010] <- new([010110],[010111])
 	             else if [010100] == [010101] then [01] <- [01011]; continue
 	 [01] <- [011]
 
 1 :: input/output
"""


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

def code_to_graph(code):
	def gengenVar():
		vn = 0
		def genVar():
			nonlocal vn
			vn += 1
			return "V%d" % vn
		return genVar
	
	genVar = gengenVar()

	decl = code['decl']
	ops = code['ops']
	def _get_branches(ops):
		res = []
		for op in ops:
			ty = op[0]
			if ty == 'br':
				v = genVar()
				res.append((v,None))
				op.append(v)
				res += get_branches[op[1]]
				res += get_branches[op[2]]
		return res

	finalCode = {
		0: {
			0: {}, #B0
			1: {}, #B1
		}
	}
	B0 = finalCode[0][0]
	B1 = finalCode[0][1]
	# とりあえずB1は自己ループ
	B1[0] = B1[1] = B1
	
	def bin2g(s):
		assert(all(map(lambda c: c in '01',s)))
		res = B0
		for c in s[::-1]:
			c = B0 if c == '0' else B1
			res = { 0: c, 1: res }
		return res
	
	def data_to_graph(data):
		ty = data[0]
		if ty == 'b': # raw binary
			return  bin2g(data[1])
		elif ty == 'c': # constant
			c = data[1]
			if c == 'B0':
				return bin2g('000')
			elif c == 'B1':
				return bin2g('001')
		elif ty == 'N': # new 
			return {
				0: data_to_graph(data[1]),
				1: data_to_graph(data[2])
			}
		elif ty == 'v': # address of variable
			return bin2g(decl_gs[data[1]])

		print('Unknown data',data)
		assert False
	
	# B0,B1に適当なデータを載せておくことができる。
	# とりあえずB0にデータを乗せておくことにする。
	# TODO: ちょっと先端が損。
	h = {}
	B0[0] = B0[1] = h
	decl_gs = {} # 変数名 -> アドレス のdict
	addr = '0000'
	for var,data in decl:
		g = data_to_graph(data)
		decl_gs[var] = addr + '0'
		addr += '1'
		th = {}
		h[0] = g
		h[1] = th
		h = th
	h[0] = h[1] = h
	
	def setOp(to,fr,cont):
		return {
			0: {
				0: B0,
				1: {
					0: data_to_graph(to),
					1: data_to_graph(fr),
				}
			},
			1: cont
		}

	def newOp(to,v0v1,cont):
		v0,v1 = v0v1
		return {
			0: {
				0: B1,
				1: {
					0: bin2g(to),
					1: {0: bin2g(v0), 1: bin2g(v1)},
				}
			},
			1: cont
		}
	
	def branchOp(v0v1,to,cont):
		v0,v1 = v0v1
		return {
			0: {
				0: bin2g('00'),
				1: {
					0: {0: bin2g(v0), 1: bin2g(v1)},
					1: bin2g(to),
				}
			},
			1: cont
		}

	def ops_to_graph(ops,cont):
		res = cont
		for op in ops[::-1]:
			ty = op[0]
			if ty == 'set':
				(_,to,fr) = op
				res = setOp(to,fr,res)
				continue
			print('Unknown op',op)
			assert False
		return res
	
	cont = B0
	# cont = setOp('1' + '11111111', decl_gs[code['output']], cont)
	cont = setOp(('b','1'), ('b',decl_gs[code['output']]), cont)
	
	finalCode[1] = ops_to_graph(ops,cont)
	return finalCode

def B0():
	return ('c','B0')

def B1():
	return ('c','B1')

def N(v0,v1):
	return ('N',v0,v1)

def char(n):
	return ('b','1' + '1'*n + '0')

def rel(v,rel):
	return ('rel',v,rel)


############## Graph related codes ####################################

def print_graph(g):
	gone = set()
	def dfs(g):
		nonlocal gone
		n = g['n']
		if n in gone:
			return
		gone.add(n)
		print('%s -> (%s ,%s)' % (n,g[0]['n'],g[1]['n'])) 
		
		for nxt in [0,1]:
			dfs(g[nxt])
	dfs(g)


def graph_to_output(g):
	n = 0
	def genVar():
		nonlocal n
		n += 1
		return b"%d" % n
	
	v = genVar()
	res = [v]
	g['n'] = v
	def dfs(g):
		for nxt in [0,1]:
			t0 = g[nxt]
			if not 'n' in t0:
				v0 = genVar()
				t0['n'] = v0
				res.append(v0)
				dfs(t0)
			else:
				res.append(t0['n'])
	
	dfs(g)
	print_graph(g)
	
	return b' '.join(res)
	

def compile(code,save=None):
	g = code_to_graph(code)
	s = graph_to_output(g)
	if save is not None:
		with open(save,'wb') as fp:
			fp.write(s)
	return s

if __name__ == '__main__':
	sample = {
		'decl': [ # name, 初期値
#			('O',('b','01001110'[::-1])), #出力
			('O',('b','')), #出力
#			('P',('b','01000101')),
		],
		'output': 'O',
		'ops': [
		]
	}
	
	compile(sample,'o')
