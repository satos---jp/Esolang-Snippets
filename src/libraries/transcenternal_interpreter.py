import sys

def interpreter(g,input,binDep=30):
	def gengenVar(prefix):
		vn = 0
		def genVar():
			nonlocal vn
			vn += 1
			return "%s%d" % (prefix,vn)
		return genVar
	genVar = gengenVar('D')

	B0 = g[0][0]
	B1 = g[0][1]
	def bin_to_g(s):
		res = B0
		for c in s[::-1]:
			c = B0 if c == '0' else B1
			res = { 0: c, 1: res, 'n': genVar() }
		return res
	def g_to_addr(g):
		res = []
		# print('g_to_addr',res,g.keys())
		cnt = 0
		while g['n'] != B0['n']:
			cnt += 1
			if cnt > binDep:
				print("Address too Deep",res)
				assert False
			c = 0 if g[0]['n'] == B0['n'] else 1
			res.append(c)
			# print('g_to_addr',res,g['n'])
			g = g[1]
		return res
	
	def getg(g,addr):
		while len(addr) > 0:
			g = g[addr[0]]
			addr = addr[1:]
		return g
	
	def setg(g,addr,h):
		assert(len(addr) > 0)
		while len(addr) > 1:
			g = g[addr[0]]
			addr = addr[1:]
		g[addr[0]] = h

	input = ''.join(map(lambda c: format(c,"08b")[::-1],input))
	g = {0:g, 1: bin_to_g(input)}
	opcnt = 0
	while True:
		opcnt += 1
		if opcnt > 1000:
			print('Too many operations')
			assert False
		if g[0][1]['n'] == B0['n']:
			break
		op = g[0][1]
		ty = op[0][0]['n']
		if ty == B0['n']:
			sys.stdout.write('Set ')
			a1 = g_to_addr(op[0][1][0])
			a2 = g_to_addr(op[0][1][1])
			print(a1,a2)
			g2 = getg(g,a2)
			setg(g,a1,g2)
			g[0][1] = g[0][1][1]
		elif ty == B1['n']:
			sys.stdout.write('New ')
			a1 = g_to_addr(op[0][1][0])
			a2 = g_to_addr(op[0][1][1][0])
			a3 = g_to_addr(op[0][1][1][1])
			print(a1,a2,a3)
			g2 = getg(g,a2)
			g3 = getg(g,a3)
			h = {0: g2, 1: g3, 'n': genVar()}
			setg(g,a1,h)
			g[0][1] = g[0][1][1]
		else:
			sys.stdout.write('Branch ')
			a1 = g_to_addr(op[0][1][0][0])
			a2 = g_to_addr(op[0][1][0][1])
			g1 = getg(g,a1)
			g2 = getg(g,a2)
			gt = op[0][1][1]
			gf = g[0][1][1]
			print(a1,a2,gt['n'],gf['n'])
			g[0][1] = gt if g1['n'] == g2['n'] else gf

	output = g_to_addr(g[1])
	outarr = output
	outs = []
	output += [0 for _ in range((8-len(output)%8)%8)]
	for i in range(len(output)//8):
		c = output[i*8:][:8]
		c = ''.join(map(lambda v: "%d" % v,c))[::-1]
		c = int(c,2)
		outs.append(c)
	outs = bytes(outs)
	print(outs,output)

