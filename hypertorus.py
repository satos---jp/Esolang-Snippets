






class MyEx(Exception):
	def __init__(sl,data):
		sl.data = data


def gen_code_sub(code,hints,jump_prog):

	ip = 0
	ip_dir = 1

	def turn(c):
		nonlocal ip_dir,ip
		if c == ord('<'):
			ip_dir *= 2
			if ip_dir == n:
				ip_dir = 1
		else:
			if ip_dir == 1:
				ip_dir = n
			ip_dir //= 2
	
	N = 8
	n = 2 ** N
	prog = [0 for _ in range(n)]
	prog[1] = ord('<')
	#prog[129] = ord('<')
	#prog[193] = ord('>')

	dcs = list(map(ord,'<>'))
	
	for k,v in hints:
		prog[k] = v
	
	"""
	rsps = [] #[385,508,391]
	lsps = [257,448] #[384,257,480,448,464,496,504,511]
	
	for d in rsps:
		prog[d] = ord('>')
	for d in lsps:
		prog[d] = ord('<')
		
	#prog[11] = 33

	dots = [131,128,134,138,146,102,359,356,354,366,374,] #[390,135,263,455,423,507,503,495,] #[256,448,321,257,353,337,329]
	for d in dots:
		prog[d] = ord('_')
	"""
	
	logs = []
	lastset = None
	def untilget(c,isprint=True):
		nonlocal lastset
		while True:
			if prog[ip] == 0:
				lastset = ip
				prog[ip] = ord(c)
				step(isprint)
				break
			else:
				if prog[ip] != 0 and prog[ip] in dcs:
					turn(prog[ip])
					step(isprint)
				elif c == prog[ip]:
					step(isprint)
					break
				else:
					print('failure at ',ip,ip_dir,prog[ip],chr(prog[ip]))
					raise MyEx({'logs': logs,'lastset': lastset})	
	
	def i2bs(x):
		return bin(x)[2:].zfill(N)
	
	def step(p=True):
		nonlocal ip,prog
		if p:
			logs.append((ip,ip_dir,prog[ip]))
			print(i2bs(ip),"%03d" % ip,i2bs(ip_dir),"%03d" % ip_dir,prog[ip],chr(prog[ip]))
		ip ^= ip_dir
	
	jumps = {}
	jump_from_to = []

	for d in code:
		assert ip_dir > 0
		if type(d) is str:
			for c in d:
				untilget(c)
		else:
			assert type(d) is int
			mip = ip ^ ip_dir
			if d >= 0:		
				jumps[d] = (mip,ip_dir)
				print('jump',d,mip,ip_dir)
			else:
				#non zero de jump
				untilget('?',False)
				step()
				prog[ip] = ord('?')
				print('loop jump')
				turn(ord('>'))
				step(False)
				jump_from_to.append(((ip,ip_dir),jumps[-d],-d))
				step(False)
				turn(ord('<'))
				
				turn(ord('<'))
				step()
	
	over_writes = {}
	for (frp,frd),(top,tod),d in jump_from_to:
		print(d,"frp,frd",(frp,frd),"top,tod",(top,tod))
		over_writes[d] = []
		
		ip = frp
		ip_dir = frd
		while True:
			if prog[ip] in dcs:
				turn(prog[ip])
				step()
			elif prog[ip] == ord('_') or prog[ip] == ord('.'):
				step()
			elif prog[ip] == ord('j'):
				if ip_dir == tod:
					break
				else:
					print('invalid jump')
					exit()
			elif prog[ip] == 0:
				prog[ip] = ord('_')
				over_writes[d].append(ip)
				step()
			else:
				print((ip,ip_dir),(top,tod))
				print(prog[ip],chr(prog[ip]))
				assert False

	
	for k,v in jump_prog.items():
		ovs = over_writes[k]
		for i,c in enumerate(v):
			if prog[ovs[i]] != ord('_'):
				print('overwrap',k,ovs[i])
				assert False
			prog[ovs[i]] = ord(c)
	
	def conv(c):
		if c == 0:
			return ord('.')
		elif c == ord('_'):
			return ord('.')
		return c
	prog = list(map(conv,prog))
	
	
	with open('o','wb') as fp:
		fp.write(bytes(prog))
	
	exit()


code = [
	"ii2-&.",
	1,
	"&:&4gw.",
	2,
	"2gw1-:.",
	-2,
	"~4gwaw",
	"1-:0=a*76*$-2$p:.",
	-1,"q",
]

code = [
	"67*i2-.",
	1,
	"84*$1-:",
	-1,
	"76*$",
	"i2-&.",
	2,
	"67*:w&:&.",
	3,
	"{:w}1-:",
	-3,
	"+waw{*{:}",
	-2,
	"q"
]


code = [
	"..",
	1,
		"r:wc7*-.",
	-1,
	"0.",
	2,
		"5a*.",
		3,
			"r:{:}+wf5*={+}",
			"1-:.",
		-3,
		"r1++w",
		":1-.",
	-2,
	"q"
]

def f(x):
	v = ord(x)
	return "%xf*%x+w" % (v//15,v%15)
#code = [''.join(map(f,'Hello, World!\n'))+'q']

def gen_code(code):
	
	nhints = [
		(143,ord('>')), (206,ord('>')),(238,ord('>')),(246,ord('>')),(244,ord('j')),
		(189,ord('>')), (185,ord('>')),(187,ord('j')),
		(103,ord('>')), (101,ord('<')),(37,ord('j')), #(174,ord('j')),
		#(158,ord('<')), (142,ord('<')),(174,ord('j')),
		#(252,ord('<')),(508,ord('>')), (380,ord('j')),
	]
	
	jump_prog = {
		1: "3",
		2: "cde*+",
		3: "bc*",
	}
	
	while True:
		print('-' * 100)
		try:
			gen_code_sub(code,nhints,jump_prog)
		except MyEx as e:
			d = e.data
			lp = d['lastset']
			if lp==0:
				raise "Fail"
			nhints.append((lp,ord('>')))
			
			
	

gen_code(code)


for i in range(16):
	for j in range(16):
		for p in range(16):
			for q in range(16):
				s = i*j+p*q
				if s==194:
					print(i,j,p,q)
					exit()

