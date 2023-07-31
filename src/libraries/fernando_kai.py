#coding: utf-8
from Tkinter import Tk


init = """
0 0 0
0 0 0 
1 1 1 
"""

#33から126までがprintable.

var_num = 0
def getv():
	#一桁変数は避ける。
	global var_num
	var_num += 1
	res = ""
	nv = var_num
	d = 127-33
	while nv>0:
		res += chr(nv%d+33)
		nv /= d
	if len(res)<=1:
		return getv()
	else:
		return res

def getvs(x):
	if x==1:
		return getv()
	else:
		return [getv() for i in xrange(x)]

#一時変数名の衝突を防ぐためにdで深さを入れる。
#あと、同じ名前が入ってきても大丈夫なように設計しましょう...
#具体的には、sに代入したあとに、aやbを参照すると壊れてる可能性がある。

def nand(s,a,b): # s = a nand b
	return "%s %s %s\n" % (s,a,b)

def one(a): #aに1を代入
	return nand(a,a,'0')

def not_(s,a): #s = !a
	if s==a: #174122 -> 144684
		return "%s %s\n" % (s,'1')
	else:
		return nand(s,a,a)

def zero(a): #aに0を代入
	#return one(a) + not_(a,a)
	return "%s 1 1\n" % a #144684 -> 144098

def and_(s,a,b): # s = a & b
	return nand(s,a,b) + not_(s,s)

def mov(s,a): # s := a
	return and_(s,a,a)

def or_(s,a,b): # s = a | b
	return not_(a,a) + not_(b,b) + nand(s,a,b)

def xor(s,a,b): # s = a ^ b
	#return mov(mb,b) + not_(ta,a) + not_(tb,b) + nand(s,a,tb) + nand(tb,ta,mb) + nand(s,s,tb)
	tc,td,te = getvs(3)
	return (
		nand(tc,a,b) + 
		nand(td,a,tc) + 
		nand(te,b,tc) + 
		nand(s,td,te) #144098 -> 119922
	)
def ha(c,s,a,b): #ハーフアダー。
	#s = a ^ b
	#c = a & b
	ma, mb = getvs(2)
	return mov(ma,a) + mov(mb,b) + xor(s,ma,mb) + and_(c,ma,mb)

def fa(c,s,p,q,r): #フルアダー。
	#s = a ^ b
	#c = a & b
	mp, mq, mr, tp= getvs(4)
	return (
		mov(mp,p) + mov(mq,q) + mov(mr,r) + 
		ha(c,s,mp,mq) + ha(tp,s,s,mr) + or_(c,tp,c)
	)
	
def inc(ds): #dsで表される配列をインクリメントする。
	tp,tq = getvs(2)
	res = one(tp)
	for s in ds:
		res += and_(tq,tp,s)
		res += xor(s,tp,s)
		res += mov(tp,tq)
	return res

def neq(r,cs,ds): #csとdsを比べた結果をrに格納する。等しいなら0。
	res = zero(r)
	tt = getv()
	for p,q in zip(cs,ds):
		res += xor(tt,p,q)
		res += or_(r,r,tt)
	return res

def add(c,cs,ds): #cs += ds, cには桁上がりが入る
	nc,ns = getvs(2)
	res = zero(nc)
	for p,q in zip(cs,ds):
		res += fa(nc,ns,nc,p,q)
		res += mov(p,ns)
	res += mov(c,nc)
	return res

def movv(cs,ds): #cs := ds
	res = ""
	for t,d in zip(cs,ds):
		res += mov(t,d)
	return res

def sub(c,cs,ds): #cs += ds, cには負数でないかどうかが入る
	td = getvs(len(ds))
	res = movv(td,ds)
	for t in td:
		res += not_(t,t)
	res += inc(td)
	res += add(c,cs,td)
	return res

def geq(r,ds,cs): #ds>=csか
	td = getvs(len(ds))
	return movv(td,ds) + sub(r,td,cs) #+ "0 0 1 1 %s %s %s %s" % (td[3],td[2],td[1],td[0]) + "\n"

def lls(ds): #論理左シフト
	res = ""
	for i in range(0,len(ds)-1)[::-1]:
		res += mov(ds[i+1],ds[i])
	res += mov(ds[0],'0')
	return res

def andv(ds,a): #ds = map(lambda x: x & a,ds)
	res = ""
	for d in ds:
		res += and_(d,d,a)
	return res

def nibai(dss): #4bitリトルインディアン(10進)のものを各桁ごとに上から2倍していく
	ls = len(dss)
	res = ""
	tp,tq = getvs(2)
	tds = getvs(4)
	for i in range(0,ls-1)[::-1]:
		ds = dss[i]
		res += geq(tp,ds,['1','0','1','0'])
		res += sub(tq,ds,[tp,'0',tp,'0'])
		#res += add(tq,dss[i+1],[tp,'0','0','0'])
		res += mov(dss[i+1][0],tp) #119922 -> 90322
		res += lls(ds)
	return res

r = Tk()
r.clipboard_clear()

import sys

ketan = 33
if len(sys.argv)>=2:
	ketan = 3

cnt = [getv() for i in xrange(10)]
ans = [[getv() for j in xrange(4)] for i in xrange(ketan)]
#変数名短くする
#cnt = ['c' + str(i) for i in xrange(10)]
#ans = [['a' + str(i) + ',' + str(j) for j in xrange(4)] for i in xrange(33)]

s = (
	init + 
	movv(cnt,['0'] * 10) + 
	""
)

for ds in ans:
	s += movv(ds,['0'] * 4)

tp = getv()
s += (
	'x' + "\n" + 
	nibai(ans) + 
	'x x x x x x x x b' + "\n" + 
	add(tp,ans[0],['b','0','0','0']) + 
	inc(cnt) + 
	#"0 0 1 1 %s %s %s %s" % (cnt[3],cnt[2],cnt[1],cnt[0]) + "\n" + 
	#geq(tp,cnt,['1','1','0','0']) + 
	#"0 0 1 1 0 0 0 %s" % tp + "\n" + 
	#neq('x',cnt,map(chr,map(ord,'0001100100'[::-1]))) + 
	neq('x',cnt,map(chr,map(ord,'0000000110'[::-1]))) + 
	'x' + "\n" +
	""
)

for ds in ans[::-1]:
	s += ("0 0 1 1 %s %s %s %s" % (ds[3],ds[2],ds[1],ds[0])) + "\n"

"""
s = (
	init + 
	't x x x x a b c d' + "\n" + 
	't x x x x e f g h' + "\n" + 
	geq('r',['d','c','b','a'],['h','g','f','e']) + 
	#'0 0 1 1 0 a b c' + "\n" + 
	'0 0 1 1 0 0 0 r' + "\n" + 
	""
)
"""

print len(s)
r.clipboard_append(s)


"""

	init + 
	't x x x x a b c d' + "\n" + 
	't x x x x e f g h' + "\n" + 
	#fa('cc','ss','b','c','d') + 
	#'0 0 1 1 0 0 cc ss' + "\n" + 
	#sub('r',['d','c','b','a'],['h','g','f','e']) + 
	lls(['d','c','b','a']) + 
	'0 0 1 1 a b c d' + "\n" + 
	'r' + "\n" +
	""

"""