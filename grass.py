import lambda_calculus
from lambda_calculus import str2lam,Var,Abs,App


"""

x1. x2. ... xn. app* => Abs(n,だんだんスタックに適用が積まれるやつ)
M N => App(stack(M),stack(N))

x. (y. M) N => (d. x. d N) (y. M) する (M中にxの出現がないとき)


lambda lifiting は、

let f x = 
	let g y = 
		M 
	in 
		N 

を

let g x y = 
	M
in
let f g' x = 
	let g = g' x in
	N

にするやつ 
"""

# E0 = Out :: Succ :: w :: In :: ε

env = ["id","out","succ","w","in"][::-1]
entire_prog = "wv"
def add_def(name,prog):
	global env,entire_prog
	tmpenv = [x for x in env]
	_,lamstr,_ = str2lam(prog).grass(tmpenv)
	entire_prog += lamstr + 'v'
	if lamstr[0]!='w':
		env = tmpenv
		env[-1] = name
	else:
		env.append(name)
	#print(env,tmpenv,lamstr[0])
	print('ok',name)

#add_def('id','(x. x)')

"""
add_def('_','''
	out (succ (in id)) 
''')
"""

#zcon :: f. (x. y. f (x x) y) (x. y. f (x x) y)

#zcon_base :: (f. x. y. f (x x) y)

#zcon :: (f. (zcon_base f) (zcon_base f))

#add_def('zcon_base','f. x. y. f (x x) y')




add_def('num_1','s. z. s z')
for i in range(1,8):
	bi = pow(2,i-1)
	add_def('num_%d' % pow(2,i),'s. z. num_%d s (num_%d s z)' % (bi,bi))

def register_num(x):
	mx = x
	b = 1
	hd = 's. z. '
	tl = ''
	while x>0:
		if x & b:
			x -= b
			hd += '(num_%d s ' % b
			tl += ')'
		b *= 2
	bo = hd + 'z' + tl
	add_def('num_%d' % mx,bo)

dTw = 256+(ord('T')-ord('w'))
print(dTw)
register_num(dTw)
add_def('chr_T','num_%d succ w' % dTw)

dKw = 256+(ord('K')-ord('w'))
register_num(dKw)
add_def('chr_K','num_%d succ w' % dKw)
register_num(50)

add_def('in','id in')
add_def('out','id out')
add_def('succ','id succ')
#add_def('w','id w')

add_def('zcon_base','f. x. y. f (x x) y')
add_def('zcon','f. (zcon_base f) (zcon_base f)')

add_def('rec_1_c_x','f. r. c. x. (chr_T c) id f r')

add_def('rec_1_c','(f. r. c. (rec_1_c_x f r c) (out c))')
add_def('rec_1','(f. r. (rec_1_c f r) (in id))')

add_def('_','zcon rec_1 id')

env.append('id')
entire_prog += "wv"
add_def('true','a. b. a')
add_def('false','a. b. b')

add_def('rec_2_q_c','q. c. false (out (q c (succ c))) (chr_K c) false q')
add_def('rec_2_q','q. rec_2_q_c q (in q)')
add_def('rec_2','f. r. true (num_50 rec_2_q r) (out (succ (in r))) f id r')
add_def('_','zcon rec_2 true')

#add_def('_','out (true w (succ w))')

"""
prog = str2lam('''
	($zcon (f. r. 
		(e. (f. g. e) (P *33 N) (G N))
		(*50 
			(q. (c. 
				(t. 
					(($isle32 c) q $false)
				) 
				(P (q c *33) N)
			) (G N))
			r
		)
		f (a. a) r
	))
''')
"""

add_def('_','''
	(x. x)
''')

print(len(entire_prog))
print(entire_prog)
open('o','w').write(entire_prog)



