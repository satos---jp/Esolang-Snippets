#coding: utf-8

from lambda_calculus import *


def isfree(sl,qd): #sl中に名前qdのvalが存在するか (今回はでばじゃんindexなので単に名前比較でよい。)
	if isinstance(sl,Val):
		return sl.v == qd
	elif isinstance(sl,Abs):
		return isfree(sl.p,qd)
	elif isinstance(sl,App):
		return isfree(sl.p,qd) or isfree(sl.q,qd)
	else:
		assert False,"Invalid Lambda"

"""
wikipedia. 
1.T[x] => x
2.T[(E1 E2)] => (T[E1] T[E2])
3.T[λx.E] => (K T[E]) (if x does not occur free in E)
4.T[λx.x] => I
5.T[λx.λy.E] => T[λx.T[λy.E]] (if x occurs free in E)
6.T[λx.(E1 E2)] => (S T[λx.E1] T[λx.E2])
"""

def rec_show(sl,d):
	if isinstance(sl,Val):
		print str(d),d*"  " + 'Val' , str(sl.v)
	elif isinstance(sl,Abs):
		print str(d),d*"  " + 'Abs'
		rec_show(sl.p,d+1)
	elif isinstance(sl,App):
		print str(d),d*"  " + 'App'
		rec_show(sl.p,d)
		rec_show(sl.q,d)
	else:
		assert False,"Invalid Lambda"

def to_unl_rec(sl,d):
	if isinstance(sl,Val):
		return sl #1.T[x] => x
	elif isinstance(sl,Abs):
		#print 'isinst .. ',sl,d,isfree(sl,d)
		if not isfree(sl,d):
			return App(Val('k'),to_unl_rec(sl.p,d+1)) #3.T[λx.E] => (K T[E]) (if x does not occur free in E)
		if isinstance(sl.p,Val):
			if sl.p.v == d:
				return Val('i') #4.T[λx.x] => I
			else:
				assert False,"最初のif文で回収されてるはず"
		elif isinstance(sl.p,Abs):
			#print 'rec inst',sl,d
			#print 'rec q',sl.p
			recget = to_unl_rec(sl.p,d+1)
			#print 'rec get',recget
			return to_unl_rec(Abs(recget),d) #5.T[λx.λy.E] => T[λx.T[λy.E]] (if x occurs free in E)
		elif isinstance(sl.p,App):
			if isinstance(sl.p.q,Val) and sl.p.q.v == d and (not isfree(sl.p.p,d)) and False: #Unlambdaの場合はη変換すると評価順が変わりそう。
				return to_unl_rec(sl.p.p,d+1) #6.5.T[λx.(E1 x)] => E1
			else:
				return App(App(Val('s'),to_unl_rec(Abs(sl.p.p),d)),to_unl_rec(Abs(sl.p.q),d))#6.T[λx.(E1 E2)] => (S T[λx.E1] T[λx.E2])
		else:
			assert False,"Invalid Lambda"
	elif isinstance(sl,App):
		return App(to_unl_rec(sl.p,d),to_unl_rec(sl.q,d)) #2.T[(E1 E2)] => (T[E1] T[E2])
	else:
		assert False,"Invalid Lambda"
	#return sl

def to_unl(sl):
	return to_unl_rec(sl,0)

#``s`kc``s`k`s`k`k`ki``ss`k`kk
#vi-boor -> ki-boor
#`?a`@i
#a?i:v
def to_ski_rec(sl):
	#print sl
	#return
	if isinstance(sl,Val):
		if sl.v=='getiszero': #とりま応急。
			return "```s`kc``s`k`s`k`k`ki``ss`k`kk`?0`@i"
		if len(sl.v)==1 and ord('a') <= ord(sl.v) and ord(sl.v) <= ord('z'):
			return sl.v
		elif len(sl.v)==1 and ord('A') <= ord(sl.v) and ord(sl.v) <= ord('Z'):
			return '.' + chr(ord(sl.v)-0x11)
		elif len(sl.v)==1 and ord('0') <= ord(sl.v) and ord(sl.v) <= ord('9'):
			return int2lam(int(sl.v,10)).to_ski()
		else:
			return globals()[sl.v].to_ski()
	elif isinstance(sl,App):
		return '`' + to_ski_rec(sl.p)  + to_ski_rec(sl.q) 
	else:
		assert False,"Invalid ski"

def to_ski(sl):
	return to_ski_rec(sl.to_unl())

Lam.to_unl = to_unl
Lam.rec_show = rec_show
Lam.to_ski = to_ski

from Tkinter import Tk


#print ycon.to_ski()
ycon = str2lam("f.(x.f (y.x x y)) (x.f (y.x x y))") #zにしておく。
#print ycon.to_ski()

#``s``s``s`ksk`k``sii``s``s`ksk`k``sii

#nq = str2lam("a.b.b a")
nq = int2lam(100)
#print nq
#nq.rec_show(0)
#print nq.to_ski()
#print str2lam("mult 5 3").to_ski()
#print ycon.to_ski()
#s =  str2lam("ycon (f.a.f (a a))").to_ski()
#print s

#s = str2lam("fact 3").to_ski() #んー、動かん...

def arr2lam(v):
	res = "x"
	for c in v:
		res = "(f %d %s)" % (c,res)
	res = "f.x." + res
	return res

#s = arr2lam([3,1,4,1,5,9,2,6,5,3,5])

def int_v_out(): #vを出力する
	res = "i"
	for i in range(0,10)[::-1]:
		res = "(pair %s %s)" % (chr(i+ord('A')),res)
	print res
	res = "v.v (x.fst (x snd %s)) 0" % res
	return str2lam(res)

outvi = int_v_out()
print outvi
print outvi.to_ski()

#a.b.(a>=5?a:a-5)*2+(b>=5 ? 1 : 0)
#funcx = str2lam("a.b.add (mult ((iszero (sub a 4)) a (sub a 5)) 2) ((iszero (sub b 4)) 0 1)")

#funcx = str2lam("a.b.1")

def nibai(): #vを二倍にする。で、下に1を足す。
	res = "v.(v (x.r.pair (cons (funcx (snd r) x) (fst r)) x) (pair 0 0))" #vを二倍する関数
	res2 = "t.cons (add (mult ((iszero (sub (snd t) 4)) (snd t) (sub (snd t) 5)) 2) (getiszero 0 1)) (fst t)"
	#res2 = "t.cons (snd t) (fst t)"
	return App(Val('d'),str2lam("vv.((%s) ((%s) vv))" % (res2,res)))
	#return str2lam(res2)

print outvi
#s = App(outvi,str2lam(arr2lam([3,1,4,1,5,9,2,6,5,3,5]))).to_ski()
#s = str2lam("((getiszero F G) C)").to_ski()
#s = str2lam("getiszero").to_ski()

"""
for i in xrange(10):
	for j in xrange(10):
		s = App(App(funcx,Val(str(i))),Val(str(j)))
		print i,j,s.reduce().to_i()
print funcx
"""

#s = App(outvi,App(nibai(),str2lam(arr2lam([3,1,4,1,5,9,2,6,5,3,5])))).to_ski()


s = App(outvi,App(App(int2lam(100),nibai()),str2lam(arr2lam([0])))).to_ski()

print s

#s = ycon.to_ski()
r = Tk()
r.clipboard_clear()
r.clipboard_append(s)

"""
1010110101010100101010101101010101001010101011010101010010101010110101010100101010101101010101001010

```s``si`k``s`k``si`k``s`kki``s``si`k``si`k`ki`k````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki.0````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki.1````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki.2````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki.3````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki.4````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki.5````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki.6````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki.7````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki.8````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki.9i`k`ki````s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki`ki`d``s`k``s``s`k``s``s`ks``s`kk``s`ks``s`k`s`ks``s`k`s`kk``s`k`si``s`kki`k``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki``s``s`k``s``s`ks``s`kk``si`k``s`k`s``s`ks``s`kki``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki`ki``s``s`k``s``s`ks``s``s`ks``s`kki`k``s``s`ks``s`kk``s`k``s``s`ks``s`kk``si`k``s`k`s``s`ks``s`kki``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki`kii`ki`k`k`ki``s``s``s`k``s``si`k`k`ki`k``s`kki``s``s`k``s`k`s``si`k``s`k``si`k`ki``s``si`k``s``s`k``s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki``s`k``s`k`s``s`ks``s`kki``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki``s`k``si`k``s`kkii``s`k``si`k``s`kkii`k````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki`ki`ki``s`kki``s`k``si`k`kii`k``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki`ki``s`k``si`k`kii``s``s`k``s`k`s``si`k``s`k``si`k`ki``s``si`k``s``s`k``s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki``s`k``s`k`s``s`ks``s`kki``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki``s`k``si`k``s`kkii``s`k``si`k``s`kkii`k````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki`ki`ki``s`kki``s`k``si`k`kii`k``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki`ki`k``s``s`ks``s`kki``s``s`ks``s`kki`ki`k`````s`kc``s`k`s`k`k`ki``ss`k`kk`?0`@i`ki``s``s`ks``s`kki`ki``s`k``si`k``s`kkii``s`k``s``si`k``s``s`ks``s`k`s`k``s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki``s``s`ks``s`k`s`k``s``s`ks``s`kk``s`ks``s`k`s`ks``s`k`s`kk``s`k`si``s`kki`k``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki``s`k`s``s`k``s``s`ks``s`kk``s`k``s``s`ks``s`kk``si`k``s`k`s``s`ks``s`kki``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki`ki``s``s`k``s``s`ks``s``s`ks``s`kki`k``s``s`ks``s`kk``s`k``s``s`ks``s`kk``si`k``s`k`s``s`ks``s`kki``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki`kii`ki`k`k`ki``s``s``s`k``s``si`k`k`ki`k``s`kki``s``s`k``s`k`s``si`k``s`k``si`k`ki``s``si`k``s``s`k``s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki``s`k``s`k`s``s`ks``s`kki``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki``s`k``si`k``s`kkii``s`k``si`k``s`kkii`k````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki`ki`ki``s`kkii`k``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki`kii``s``s`k``s`k`s``si`k``s`k``si`k`ki``s``si`k``s``s`k``s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki``s`k``s`k`s``s`ks``s`kki``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki``s`k``si`k``s`kkii``s`k``si`k``s`kkii`k````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki`ki`ki``s`kkii`k``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki`ki`k``s``s`ks``s`kki``s``s`ks``s`kki`ki`k``s``s``s`k``s``si`k`k`ki`k``s`kki``s``s`k``s`k`s``si`k``s`k``si`k`ki``s``si`k``s``s`k``s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki``s`k``s`k`s``s`ks``s`kki``s``s`ks``s`k`s`ks``s`k`s`kk``s``s`ks``s`kki`ki`k`ki``s`k``si`k``s`kkii``s`k``si`k``s`kkii`k````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki`ki`ki``s`kkii`k``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki``s``s`ks``s`kki`ki`k`ki`k``s``s`ks``s`kki`ki``s`k``si`k`kii``s`kki`k``s`k``si`k``s`kkii``s`kki`k````s``s`ks``s`kk``s`ks``s`k`si``s`kki`k``s`kki`ki`kii``s``s`ks``s`kk``si`k`ki`ki
"""
