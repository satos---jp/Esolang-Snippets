#coding: utf-8

import copy


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
		red = App(App(sl,Val("s")),Val("z"))
		#print red
		red = red.reduce()
		#print "red .. ",red
		res = 0
		while True:
			if red == Val("z"):
				return res
			elif isinstance(red,App):
				if red.p == Val("s"):
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


#de Bruijn index とは逆のことをしてる。
#外側からn番目の抽象と対応してる変数にインデックスnがつく。
#簡約時には、代入するほうの項を代入の瞬間に代入される場所の深さ分liftする必要がある。
#また、簡約終了時に、全体を-1分liftする必要がある。

class Val(Lam):
	#de burjan index を使う
	def __init__(sl,iv):
		sl.v = iv #intもしくはstr。strは、lambda2intとかで必要になる。
	
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

class Abs(Lam):
	def __init__(sl,ip):
		sl.p = ip
	def step(sl):
		return None
	def subst(sl,d,x):
		return Abs(sl.p.subst(d+1,x))
	def __str__(sl):
		return ("λ.%s" % sl.p)
	def __eq__(sl,x):
		return isinstance(x,Abs) and sl.p==x.p
	def __ne__(sl,x):
		return not sl.__eq__(x)
	def lift(sl,d):
		return Abs(sl.p.lift(d))

class App(Lam):
	def __init__(sl,ip,iq):
		sl.p,sl.q = ip,iq
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


def int2lam(x):
	res = Val(1)
	for i in xrange(x):
		res = App(Val(0),res)
	res = Abs(Abs(res))
	return res

"""
sym ::= () .以外で構成された文字列

term ::= (apps)
	   | sym.apps
	   | sym
	   
apps ::= term
	   | term apps

このとき、例えば、
x.y z は、
(x.y) z ではなく、
x.(y z) とパースされる。
"""

def str2lam(ins):
	sgs = '() .'
	#記号以外の文字列は全てsymとする。
	def sym(s):
		if len(s)==0 or s[0] in sgs:
			return '',s
		else:
			tp,ts = sym(s[1:])
			return (s[0]+ tp,ts)
	
	def term(s,ctx):
		#print 'term .. ',s,ctx
		if s[0]=='(':
			tt,ts = apps(s[1:],ctx)
			assert ts[0]==')'
			return (tt,ts[1:])
		sy,ts = sym(s)
		if len(ts)!=0 and ts[0]=='.':
			tt,ts = apps(ts[1:],[sy] + ctx)
			return Abs(tt),ts
		else:
			if sy in ctx:
				return Val(len(ctx) - ctx.index(sy) - 1),ts
			else:
				#zやsなどのシンボル、もしくは既に定義されている変数。
				#パースの段階では、そのままにしておく。
				return Val(sy),ts
	
	def apps(s,ctx):
		#print 'apps .. ',s,ctx
		rt,ts = term(s,ctx)
		while len(ts)>0 and ts[0]==' ':
			at,ts = term(ts[1:],ctx)
			rt = App(rt,at)
		return rt,ts
	
	
	rt,rs = apps(ins,[])
	#print rt,rs
	assert rs == ''
	return rt

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
x = str2lam("pair 4 6")
print str2lam("fst x").to_i()
print str2lam("snd x").to_i()
"""
add = str2lam("n.m.n succ m")
mult = str2lam("n.m.n (x.add m x) zero")
pow = str2lam("n.m.n m")
"""
print str2lam("add 5 3").to_i()
print str2lam("mult 5 3").to_i()
print str2lam("pow 3 4").to_i()
"""

pred = str2lam("n.snd (n (p.pair (succ (fst p)) (fst p)) (pair 0 0))")
sub = str2lam("n.m.m pred n")
"""
print str2lam("pred 6").to_i()
print str2lam("pred 0").to_i()
print str2lam("sub 6 2").to_i()
"""

lamtrue = str2lam("t.f.t")
lamfalse = str2lam("t.f.f")
lamif = str2lam("b.b")
iszero = str2lam("n.n (x.lamfalse) lamtrue")
"""
print str2lam("lamif (iszero 0) 6 2").to_i()
print str2lam("lamif (iszero 3) 6 2").to_i()
"""

ycon = str2lam("f.(x.f (x x)) (x.f (x x))")
fact = str2lam("ycon (f.n.lamif (iszero n) 1 (mult (f (pred n)) n))")

"""
print str2lam("fact 0").to_i()
print str2lam("fact 3").to_i()
print str2lam("fact 5").to_i() #2秒くらいかかる。
print str2lam("fact 6").to_i() #15秒くらいかかる。
"""

omega = str2lam("(x.(x x)) x.(x x)")

#チャーチエンコーディング
nil = str2lam("c.n.n")
cons = str2lam("x.l.(c.n.c x (l c n))")
isnil = str2lam("l.l (a.r.lamfalse) lamtrue")
fold = str2lam("l.l")
"""
x = str2lam("cons 3 (cons 4 (cons 5 nil))")
print str2lam("fold x add 0").to_i()
print str2lam("isnil nil").to_b()
print str2lam("isnil x").to_b()
"""

head = str2lam("l.l (a.r.a) omega")
tail = str2lam("l.snd (l (a.r.pair (cons a (fst r)) (fst r)) (pair nil nil))")
#predと同じ要領ですね。

"""
x = list2lam(map(lambda p: int2lam(p),[3,4,5]))
print str2lam("head x").to_i()
print str2lam("head (tail x)").to_i()
print map(lambda l: l.to_i(),x.to_list())
"""

isge = str2lam("n.m.iszero (sub m n)") #>=
isle = str2lam("n.m.iszero (sub n m)") #<=
"""
print str2lam("isge 5 3").to_b()
print str2lam("isle 5 3").to_b()
print str2lam("isge 5 5").to_b()
"""

#比較関数(cpf)と挿入要素(x)とリスト(l)をこの順番で受け取り、
#l 内で最初にcpf(x,y)がTrueを返す要素yの次の位置に、
#xを挿入したリスト、を返す関数。
insert = str2lam(
	"cpf.x.ycon (rf.l.(" +
		"lamif (isnil l) (cons x nil) (" + 
			"lamif (cpf (head l) x) (cons x l) (cons (head l) (rf (tail l)))" + 
	")))")
"""
x = list2lam(map(lambda p: int2lam(p),[3,4,6,8]))
tx = str2lam("insert isge 5 x")
print map(lambda l: l.to_i(),tx.to_list())
"""

#比較関数(cpf)とリスト(l)をこの順番で受け取り、
#リストlをcpfに従ってソートしたリストを返す関数。
#挿入ソートに基づいてソートしている。
sort = str2lam("cpf.ycon (rf.l.lamif (isnil l) nil (insert cpf (head l) (rf (tail l))))")

"""
x = list2lam(map(lambda p: int2lam(p),[3,5,4,1]))
tx = str2lam("sort isge x") #10秒弱かかる。
print map(lambda l: l.to_i(),tx.to_list())
tx = str2lam("sort isle x")
print map(lambda l: l.to_i(),tx.to_list())
"""

#以下、サンプル
if __name__ == '__main__':
	print str2lam("fact 5").to_i()
	x = list2lam(map(lambda p: int2lam(p),[3,5,4,1]))
	print map(lambda l: l.to_i(),x.to_list())
	tx = str2lam("sort isge x")
	print map(lambda l: l.to_i(),tx.to_list())


funcx = str2lam("a.b.add (mult ((iszero (sub a 4)) a (sub a 5)) 2) ((iszero (sub b 4)) 0 1)")
cons = str2lam("a.v.f.x.f a (v f x)")

