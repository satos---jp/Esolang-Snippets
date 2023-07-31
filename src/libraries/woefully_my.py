
def d2p(ss):
	th = []
	bd = 0
	for p in ss:
		nd = p[0]
		if nd!=bd:
			td = 0-(nd+bd)
		else:
			td = (nd+2)%3-1
		th.append(td)
		for i in xrange(p[1]-1):
			th.append(nd)
		bd = nd
	th = [0] + th
	ls = len(th)
	for i in xrange(ls-1):
		th[i+1] += th[i]
	ml = -min(th)
	res = ""
	for d in th:
		res += (ml+d+1) * '|' + " |\n" 
	return res

#print d2p([(-1,4),(1,6)])

print d2p([(1,7),(1,5),(1,7),(1,6)])
