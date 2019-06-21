#coding: utf-8

import copy
import re


class Lam:
	def reduce(sl):
		res = sl
		while True:
			#print res
			tr = res.step()
			if tr==None:
				break
			res = tr
		#print res
		return res
	
	def to_i(sl):
		red = App(App(sl,Var("s")),Var("z"))
		#print red
		red = red.reduce()
		#print "red .. ",red
		res = 0
		while True:
			if red == Var("z"):
				return res
			elif isinstance(red,App):
				if red.p == Var("s"):
					res += 1
					red = red.q
					continue
			assert False,("This reduced lambda isn't nat lambda .. %s" % red)
		return res
	
	def to_b(sl):
		red = App(App(sl,Val("t")),Val("f")).reduce()
		if red == Val("t"):
			return True
		if red == Val("f"):
			return False
		
		assert False,("This reduced lambda isn't bool lambda .. %s" % red)
	
	def to_list(sl):
		res = []
		red = sl
		while not App(isnil,red).reduce().to_b():
			res.append(App(head,red))
			red = App(tail,red).reduce()
		return res

class Var(Lam):
	#de burjan index を使う
	def __init__(sl,v):
		sl.v = v
	def init_debruijn(sl,env=[]):
		#print(env)
		if sl.v in env:
			sl.idx = env[::-1].index(sl.v)
	
	def lift(sl,d):
		if isinstance(sl.v,int):
			return Val(sl.v + d)
		else:
			return Val(sl.v)
	
	def subst(sl,d,x):
		if isinstance(sl.v,int):
			if sl.v == 0:
				#ここで置換する。
				return x.lift(d)
			else:
				#外側のが1個はずれてるので減らす。
				return Val(sl.v-1)
		else:
			return Val(sl.v) 
	def step(sl):
		if isinstance(sl.v,int):
			assert False,"this is naked val!!"
		#いちばん外側なので、liftはしなくてよい。
		#step時まで展開しないようにすることで、だいたい,1.5倍くらい早くなった。
		if sl.v.isdigit():
			#数字を直で変換してくれるようにする。
			return int2lam(int(sl.v,10))
		elif sl.v in globals():
			#既に定義されてるなら、それを使う。
			return globals()[sl.v]
		else:
			return None
	def __str__(sl):
		return repr(sl.v)
	def __eq__(sl,x):
		return isinstance(x,Val) and sl.v==x.v
	def __ne__(sl,x):
		return not sl.__eq__(x)
	
	def grass(sl,env):
		return sl.v,"",env

class Abs(Lam):
	def __init__(sl,v,p):
		sl.v = v
		sl.p = p
	def init_debruijn(sl,env=[]):
		#print(env,sl.v)
		sl.p.init_debruijn(env + [sl.v])
	
	def step(sl):
		return None
	def subst(sl,d,x):
		return Abs(sl.p.subst(d+1,x))
	def __str__(sl):
		return ("%s.%s" % (sl.v,sl.p))
	def __eq__(sl,x):
		return isinstance(x,Abs) and sl.p==x.p
	def __ne__(sl,x):
		return not sl.__eq__(x)
	def lift(sl,d):
		return Abs(sl.p.lift(d))
		
	def grass(sl,env):
		env.append(sl.v)
		if isinstance(sl.p,Var):
			_,res,_ = App(Var("id"),sl.p).grass(env)
		else:
			_,res,_ = sl.p.grass(env)	
		return None,'w'+res,None		

class App(Lam):
	def __init__(sl,ip,iq):
		sl.p,sl.q = ip,iq
	
	def init_debruijn(sl,env=[]):
		#print(env)
		sl.p.init_debruijn(env)
		sl.q.init_debruijn(env)

	def step(sl):
		#print sl
		if isinstance(sl.p,Abs):
			#ここをβ簡約する
			return sl.p.p.subst(0,sl.q)
		else: #App or Val
			pt = sl.p.step()
			if pt != None:
				return App(pt,sl.q)
			else:
				#左がValで、かつ右が簡約できる可能性があるかもしれないので、
				#右側も簡約する。
				qt = sl.q.step()
				if qt != None:
					return App(sl.p,qt)
				else:
					return None
	
	def lift(sl,d):
		return App(sl.p.lift(d) ,sl.q.lift(d))
	def subst(sl,d,x):
		return App(sl.p.subst(d,x) ,sl.q.subst(d,x))
		
	def __str__(sl):
		return ("(%s %s)" % (sl.p,sl.q))
	def __eq__(sl,x):
		return isinstance(x,App) and sl.p==x.p and sl.q==x.q
	def __ne__(sl,x):
		return not sl.__eq__(x)
	
	def grass(sl,env):
		psym,ps,env = sl.p.grass(env)
		qsym,qs,env = sl.q.grass(env)
		pi = env[::-1].index(psym)
		qi = env[::-1].index(qsym)
		if pi<0:
			print('var %s not found in env %s' % (psym,env))
			exit()
		if qi<0:
			print('var %s not found in env %s' % (qsym,env))
			exit()
		
		ts = ps + qs + 'W'*(pi+1) + 'w'*(qi+1) 
		#print(psym,qsym,ps,qs,ts)
		rsym = "sym%s" % len(env)
		env.append(rsym)
		return rsym,ts,env
		


def int2lam(x):
	res = Var('z')
	for i in range(x):
		res = App(Var('s'),res)
	res = Abs('s',Abs('z',res))
	return res

def str2lam(prog):
	def tokenize(prog):
		res = re.split("(\$\w+|\w+\.|\w+|\.\w|\.|->|\)|\(|\?\w|\*\d+,\d+|\*\d+)",prog)
		res = list(filter(lambda x: x.strip() != "",res))
		#print(res)
		return res
	
	def parse(x):
		if x == []:
			raise "failure"
		def parse_apps(x):
			res = None
			while x[0] != ')':
				v,x = parse(x)
				if res is None:
					res = v
				else:
					res = App(res,v)
			return res,x
		
		if x[0] == '(':
			res,x = parse_apps(x[1:])
			return res,x[1:]
		elif x[0][-1] == '.':
			v = x[0][:-1]
			#print(v)
			bo,x = parse_apps(x[1:])
			return Abs(v,bo),x
		else:
			v = x[0]
			if v[0]=='*':
				v = int2lam(int(v[1:],10))
			elif v[0]=='$':
				v = globals()[v[1:]]
			else:
				v = Var(v)
			return v,x[1:]
	res,rem = parse(tokenize('(%s)' % prog))
	#print(res,rem)
	assert len(rem)==0
	res.init_debruijn([])
	return res

def list2lam(x):
	res = nil
	for p in x[::-1]:
		res = App(App(cons,p),res)
	return res

import sys
sys.setrecursionlimit(100000)
#再帰のリミットを外しておく。

zero = str2lam("s.z.z")
succ = str2lam("n.s.z.s (n s z)")

pair = str2lam("a.b.f.f a b")
fst = str2lam("p.p a.b.a")
snd = str2lam("p.p a.b.b")
"""
x = str2lam("$pair 4 6")
print str2lam("$fst x").to_i()
print str2lam("$snd x").to_i()
"""
add = str2lam("n.m.n $succ m")
mult = str2lam("n.m.n (x.$add m x) $zero")
pow = str2lam("n.m.n m")
"""
print str2lam("add 5 3").to_i()
print str2lam("mult 5 3").to_i()
print str2lam("pow 3 4").to_i()
"""

pred = str2lam("n.$snd (n (p.$pair ($succ ($fst p)) ($fst p)) ($pair *0 *0))")
sub = str2lam("n.m.m $pred n")
"""
print str2lam("pred 6").to_i()
print str2lam("pred 0").to_i()
print str2lam("sub 6 2").to_i()
"""

lamtrue = str2lam("t.f.t")
true = lamtrue
lamfalse = str2lam("t.f.f")
false = lamfalse
lamif = str2lam("b.b")
iszero = str2lam("n.n (x.$lamfalse) $lamtrue")
"""
print str2lam("lamif (iszero 0) 6 2").to_i()
print str2lam("lamif (iszero 3) 6 2").to_i()
"""

ycon = str2lam("f.(x.f (x x)) (x.f (x x))")
zcon = str2lam("f.(x.y. f (x x) y) (x.y. f (x x) y)")
fact = str2lam("$ycon (f.n.$lamif ($iszero n) *1 ($mult (f ($pred n)) n))")


omega = str2lam("(x.(x x)) x.(x x)")

#チャーチエンコーディング
nil = str2lam("c.n.n")
cons = str2lam("x.l.(c.n.c x (l c n))")
isnil = str2lam("l.l (a.r.$lamfalse) $lamtrue")
fold = str2lam("l.l")
"""
x = str2lam("cons 3 (cons 4 (cons 5 nil))")
print str2lam("fold x add 0").to_i()
print str2lam("isnil nil").to_b()
print str2lam("isnil x").to_b()
"""

head = str2lam("l.l (a.r.a) $omega")
tail = str2lam("l.$snd (l (a.r.$pair ($cons a ($fst r)) ($fst r)) ($pair $nil $nil))")
#predと同じ要領ですね。

"""
x = list2lam(map(lambda p: int2lam(p),[3,4,5]))
print str2lam("head x").to_i()
print str2lam("head (tail x)").to_i()
print map(lambda l: l.to_i(),x.to_list())
"""

isge = str2lam("n.m.$iszero ($sub m n)") #>=
isle = str2lam("n.m.$iszero ($sub n m)") #<=

band = str2lam("n. m. n m $false") 
iseq = str2lam("n. m. $band ($isge n m) ($isle n m)")
"""
print str2lam("isge 5 3").to_b()
print str2lam("isle 5 3").to_b()
print str2lam("isge 5 5").to_b()
"""



#以下、サンプル
if __name__ == '__main__':
	print(str2lam("$fact *5").to_i())
	x = list2lam(map(lambda p: int2lam(p),[3,5,4,1]))
	print(map(lambda l: l.to_i(),x.to_list()))
	#tx = str2lam("sort isge x")
	#print(map(lambda l: l.to_i(),tx.to_list()))


