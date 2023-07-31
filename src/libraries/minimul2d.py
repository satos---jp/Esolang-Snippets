import brainf_ck

"""
abcd/D    /LRijkl
     Refgh/UU
"""

def compile(prog):
	maxd = 0
	dep = 10
	res = ["" for _ in range(dep)]
	d = 0
	def addc(dic):
		for t in range(dep):
			tc = " "
			if dic.get(t,None):
				tc = dic[t]
			res[t] += tc
	for c in prog:
		if c=='[':
			addc({d:'/'})
			addc({d:'D',d+1:'R'})
			d += 1
			maxd = max(d,maxd)
		elif c==']':
			d -= 1
			addc({d:'/',d+1:'/'})
			addc({d:'L',d+1:'U'})
			addc({d:'R',d+1:'U'})
		else:
			addc({d: c})
	res = '\n'.join(res[:maxd+1])
	return res



# flag,cnt,chr,buf

prog = "+[,.84-]+[>50+[>,+<<[>>->+<<<-]>>.75-[>[<<<+>>>-]<[-]]>[-]<<-]>,+.<<]"
prog = "+[,.84-]+[>50+[>,+<<[>>->+<<<-]>>.75-[>[<<<+>>>-]<[+]]>[-]<<-]>,+.<<]"

# flag,cnt,chr,buf
prog = "+[,.>12+[<7->-]<]+[>>[-]+++++[<++++++++++>-]<[>,+<<[>>->+<<<-]>>.<<+++++[>>---------------<<-]>>[>[<<<+>>>-]<[+]]>[-]<<-]>,+.<<]"

#prog = "+[>6+[>[-]65+.<-]<,.84-]"
prog = brainf_ck.compile(prog)
prog = compile(prog)
print(len(prog))
open('o','w').write(prog)
