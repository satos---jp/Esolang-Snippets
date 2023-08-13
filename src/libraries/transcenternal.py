
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

def gengenVar(prefix):
	vn = 0
	def genVar():
		nonlocal vn
		vn += 1
		return "%s%d" % (prefix,vn)
	return genVar

def code_to_graph(code):
	genVar = gengenVar('V')
	genLabel = gengenVar('L')
	
	# Make a graph with hashing
	def makeN():
		genHash = gengenVar('H')
		table = {}
		def N(g):
			if set(g.keys()) != set([0,1]):
				print('Unexpected argument: ',g.keys())
				assert(False)
			g0, g1 = g[0], g[1]
			if g0 is None or g1 is None:
				h = genHash()
				res = {
					0: g0, 1: g1,
					'h': h
				}
				return res
			k = "%s#%s" % (g0['h'],g1['h'])
			if k in table:
				return table[k]
			h = genHash()
			res = {
				0: g0, 1: g1,
				'h': h
			}
			table[k] = res
			return res
		return N
	N = makeN()

	decl = code['decl']

	finalCode = {
		'h': 'HRoot',
		0: {
			'h': 'HR00',
			0: {'h': 'HB0'}, #B0
			1: {'h': 'HB1'}, #B1
		}
	}
	JumpDummy = finalCode[0]
	B0 = finalCode[0][0]
	B1 = finalCode[0][1]
	# とりあえずB1は自己ループ
	B1[0] = B1[1] = B1
	
	def bin2g_cont(s,cont):
		assert(all(map(lambda c: c in '01',s)))
		res = cont
		for c in s[::-1]:
			c = B0 if c == '0' else B1
			res = N({ 0: c, 1: res })
		return res
	
	def bin2g(s):	
		return bin2g_cont(s,B0)
	
	def data_to_graph_cont(data,cont):
		ty = data[0]
		if ty == 'b': # raw binary
			return  bin2g_cont(data[1],cont)
		elif ty == 'c': # constant
			c = data[1]
			if c == 'B0':
				return bin2g_cont('000',cont)
			elif c == 'B1':
				return bin2g_cont('001',cont)
		elif ty == 'N': # new 
			return N({
				0: data_to_graph_cont(data[1],cont),
				1: data_to_graph_cont(data[2],cont)
			})
		elif ty == 'v': # address of variable
			return bin2g_cont(decl_gs[data[1]],cont)
		elif ty == 'ra': # relative address after variable
			(_,d,rel) = data
			return data_to_graph_cont(d,bin2g_cont(rel,cont))

		print('Unknown data',data)
		assert False
	
	def data_to_graph(data):
		return data_to_graph_cont(data,B0)

	operations = code['ops']

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
	
	print(decl_gs)
	
	############# Operation Compilation #################
	
	N2 = lambda v: v
	def setOp(to,fr,cont):
		return N2({
			0: N2({
				0: B0,
				1: N2({
					0: data_to_graph(to),
					1: data_to_graph(fr),
				})
			}),
			1: cont
		})

	def newOp(to,v0v1,cont):
		v0,v1 = v0v1
		return N2({
			0: N2({
				0: B1,
				1: N2({
					0: data_to_graph(to),
					1: N2({0: data_to_graph(v0), 1: data_to_graph(v1)}),
				})
			}),
			1: cont
		})
	
	def branchOp(v0v1,to,cont):
		v0,v1 = v0v1
		return N2({
			0: N2({
				0: JumpDummy, #B0,B1以外ならなんでも
				1: N2({
					0: N2({0: data_to_graph(v0), 1: data_to_graph(v1)}),
					1: to,
				})
			}),
			1: cont
		})

	# gotoIfとlabelの解決される順番に依る
	label_to_graph = {}
	graph_resolved_by_label = {}

	def ops_to_graph(ops,res):
		for op in ops[::-1]:
			ty = op[0]
			if ty == 'set':
				(_,to,fr) = op
				res = setOp(to,fr,res)
				continue
			elif ty == 'new':
				(_,to,v0v1) = op
				res = newOp(to,v0v1,res)
				continue
			elif ty in ['gotoIfEq','gotoIfNe']:
				(_,v0v1,label) = op
				gthen = None
				if label in label_to_graph:
					gthen = label_to_graph[label]
				
				if ty == 'gotoIfEq':
					res = branchOp(v0v1,gthen,res)
					tmpg = res[0][1]
				elif ty == 'gotoIfNe':
					res = branchOp(v0v1,res,gthen)
					tmpg = res
				else:
					assert False

				if gthen is None:
					if not label in graph_resolved_by_label:
						graph_resolved_by_label[label] = []
					print(op,label_to_graph.keys(),graph_resolved_by_label)
					
					assert(tmpg[1] is None)
					# print('Lazy update',id(tmpg))
					# lam = lambda tmpg: lambda g: print('upd',id(tmpg),label,tmpg.update({1: g}))
					lam = lambda tmpg: lambda g: tmpg.update({1: g})
					graph_resolved_by_label[label].append(lam(tmpg))
				continue
			elif ty == 'label':
				(_,label) = op
				label_to_graph[label] = res
				# print('Update',label)
				if not label in graph_resolved_by_label:
					continue
				for f in graph_resolved_by_label[label]:
					# print('Update',label,f)
					f(res)
				continue
			elif ty == 'br':
				(_,v0v1,thenbr,elsebr) = op
				gthen = ops_to_graph(thenbr,res)
				gelse = ops_to_graph(elsebr,res)
				res = branchOp(v0v1,gthen,gelse)
				continue
			print('Unknown op',op)
			assert False
		return res
	

	cont = B0
	# cont = setOp('1' + '11111111', decl_gs[code['output']], cont)
	cont = setOp(('b','1'), ('b',decl_gs[code['output']]), cont)
	
	codeGraph = ops_to_graph(operations,cont)
	# codeGraph[0][1] [0][0] [1][1][0] = B1  
	print(graph_resolved_by_label)
	finalCode[1] = codeGraph
	# finalCode[1] = ops_to_graph(operations,cont)
	"""
	cont = B0
	h = {}
	B0[0] = B0[1] = h
	h[0] = B0
	h[1] = setOp(('b','10'),('b','001'),cont)
	B0addr = ('b','000')
	gtaddr = ('b','0001')
	finalCode[1] = branchOp((B0addr,B0addr),gtaddr,cont)
	"""
	return finalCode

def B0():
	return ('c','B0')

def B1():
	return ('c','B1')

def New(v0,v1):
	return ('N',v0,v1)

def char(n):
	return ('b','1' + '1'*n + '0')

def rel(v,rel):
	return ('ra',v,rel)

def var(x):
	return ('v',x)

############## Graph related codes ####################################

def node_num(g):
	gone = set()	
	def aux(g):
		n = g['n']
		if n in gone:
			return
		gone.add(n)
		aux(g[0])
		aux(g[1])
	aux(g)
	return len(gone)

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
	genV = gengenVar('')
	genVar = lambda: genV().encode('ascii')

	v = genVar()
	res = [v]
	g['n'] = v
	def dfs(g):
		for nxt in [0,1]:
			t0 = g[nxt]
			if t0 is None:
				print('Found None node',id(g))
				assert False
				continue
			if not 'n' in t0:
				v = genVar()
				t0['n'] = v
				res.append(v)
				dfs(t0)
			else:
				res.append(t0['n'])
	
	dfs(g)
	# check_all_node_has_n(g)
	print('Num of nodes',node_num(g))
	# print_graph(g)
	
	import string
	cs = list(set(string.printable)-set(string.whitespace))
	def conv(n):
		N = len(cs)
		res = b""
		while n > 0:
			res += bytes([ord(cs[n%N])])
			n //= N
		return res
	
	res = list(map(lambda d: conv(int(d)),res))
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
