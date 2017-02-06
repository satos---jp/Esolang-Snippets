#coding: utf-8
from Tkinter import Tk


init = """
0 0 0
0 0 0 
1 1 1 
"""

def nand(s,a,b): # s = a nand b
	if s==a: #それはそう。 10242 -> 10162
		return "%s %s\n" % (s,b)
	elif s==b:
		return "%s %s\n" % (s,a)
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
	return not_(a,a) + not_(b,b) + nand(s,a,b) #ここでa,bを反転させてるのやばくないですか...?????

def xor(s,a,b): # s = a ^ b
	#return mov(mb,b) + not_(ta,a) + not_(tb,b) + nand(s,a,tb) + nand(tb,ta,mb) + nand(s,s,tb)
	tc,td,te = ('A','B','C')
	if a==s:
		te = s #これ!!。 10162 -> 9798
	return (
		nand(tc,a,b) + 
		nand(td,a,tc) + 
		nand(te,b,tc) + 
		nand(s,td,te) #144098 -> 119922
	)

def inc(ds): #dsで表される配列をインクリメントする。
	tp,tq = ('D','E')
	res = one(tp)
	for s in ds:
		res += and_(tq,tp,s)
		res += xor(s,tp,s)
		res += mov(tp,tq)
	return res

def neq(r,cs,ds): #csとdsを比べた結果をrに格納する。等しいなら0。
	res = zero(r)
	tt = 'F'
	for p,q in zip(cs,ds):
		res += xor(tt,p,q)
		res += or_(r,r,tt)
	return res


def add0or5(a,b,c,r): # cba += r0r をする
	tp,ic,ib = ('G','H','I')
	#return add(tp,[a,b,c],[r,'0',r])
	res = ""
	res += and_(ib,a,r)
	res += and_(ic,ib,b)
	res += xor(ic,ic,r)
	res += xor(c,c,ic)
	res += xor(b,b,ib)
	res += xor(a,a,r)
	return res

def sub5(r,a,b,c,d): # dcba -= 0101 をする。で、rに、dcba += 1011の繰り上がりの結果が入る
	#return sub(r,[a,b,c,d],['1','0','1','0'])
	#return add(r,[a,b,c,d],['1','1','0','1']) #49252 -> 38372
	
	ib,ic,id,ir = ('J','K','L','M') #38372 -> 15662
	res = ""
	res += not_(a,a)
	res += not_(ic,b)
	res += nand(ic,ic,a)
	res += nand(id,ic,c)
	res += not_(d,d)
	res += nand(ir,id,d) #圧縮!!. 10498 -> 10242
	res += xor(b,b,a)
	res += xor(c,c,ic)
	res += xor(d,d,id)
	res += not_(r,ir)
	return res
	"""
	res = ""
	res += not_(a,a)
	res += not_(ic,b)
	res += nand(ic,ic,a)
	res += and_(id,ic,c)
	res += or_(ir,id,d)
	res += xor(b,b,a)
	res += xor(c,c,ic)
	res += xor(d,d,id)
	res += not_(r,ir)
	return res
	"""

def mo5sub5(r,ds): 
	#if ds>=5 then {ds -= 5; r=1;} else {r=0;}
	tq = 'N'
	res = ""

	res += sub5(r,ds[0],ds[1],ds[2],ds[3])
	res += add0or5(ds[0],ds[1],ds[2],r) #答えは0から4のどれか。
	
	#print res.count("\n"),
	#ls = len(res)  #3/4なので、30命令程に抑えればよい(抑えたい)
	#というか、あと10命令程削ればよい。
	#res = res[0:ls*3/4]
	#res += zero(ds[3]) #シフトするので不要。 11935 -> 11711
	return res

def lls(ds): #論理左シフト
	#変数名つけかえという邪悪な方法をとると1600へる?
	#一周させないといけないのでだめ....つらいなぁ
	"""
	ds[3] = ds[2]
	ds[2] = ds[1]
	ds[1] = ds[0]
	ds[0] = getv()
	return ""
	"""
	
	res = ""
	for i in range(0,len(ds)-1)[::-1]:
		res += mov(ds[i+1],ds[i]) 
	#res += mov(ds[0],'0') 
	#res += zero(ds[0]) #それはそう。 11711 -> 11551
	#どうやらこれも落とせそうらしい。(たいていは下からnotが繰り上がるため。下一桁はinputで消える) 消すと230減るので、
	#10704 -> 10498になる
	return res


def nibai(dss): #4bitリトルインディアン(10進)のものを各桁ごとに上から2倍していく
	ls = len(dss)
	res = ""
	tp,tq = ('O','P')
	for i in range(0,ls-1)[::-1]:
		ds = dss[i]
		res += mo5sub5(tp,ds)
		
		res += not_(dss[i+1][0],tp) #119922 -> 90322
		#print ds,
		res += lls(ds)
		#print ds
	return res

#変数名をAからRまで割り振ることにより、
#14807 -> 11935

#33から126までがprintable.

var_num = 0
def getv():
	global var_num
	var_num += 1
	res = ""
	nv = var_num
	d = 127-33
	ok = True
	while nv>0:
		nc = nv%d+33
		res += chr(nc)
		nv /= d
	if len(res)<=1:
		c = res[0]
		if c=='0' or c=='1' or c=='?' or (ord('A') <= ord(c) and ord(c) <= ord('R')):
			#はてな!! 11511 -> 10704
			return getv()
	
	return res

def getvs(x):
	if x==1:
		return getv()
	else:
		return [getv() for i in xrange(x)]

#一時変数名の衝突を防ぐためにdで深さを入れる。
#あと、同じ名前が入ってきても大丈夫なように設計しましょう...
#具体的には、sに代入したあとに、aやbを参照すると壊れてる可能性がある。


r = Tk()
r.clipboard_clear()

import sys

ketan = 33
if len(sys.argv)>=2:
	ketan = 3

ans = [[getv() for j in xrange(4)] for i in xrange(ketan)]
cnt = [getv() for i in xrange(7)] #38372 -> 38030
#変数名短くする
#cnt = ['c' + str(i) for i in xrange(10)]
#ans = [['a' + str(i) + ',' + str(j) for j in xrange(4)] for i in xrange(33)]

s = (
	init + 
	""
)

s += (
	'Q' + "\n" + 
	nibai(ans) + 
	'Q Q Q Q Q Q Q Q R' + "\n" + 
	mov(ans[0][0],'R') + #はい。 15662 -> 14807
	inc(cnt) + 
	#"0 0 1 1 %s %s %s %s" % (cnt[3],cnt[2],cnt[1],cnt[0]) + "\n" + 
	#geq(tp,cnt,['1','1','0','0']) + 
	#"0 0 1 1 0 0 0 %s" % tp + "\n" + 
	neq('Q',cnt,map(chr,map(ord,'1100100'[::-1]))) + 
	#neq('x',cnt,map(chr,map(ord,'0010000'[::-1]))) + 
	'Q' + "\n" +
	""
)

for ds in ans[::-1]:
	s += ("0 0 1 1 %s %s %s %s" % (ds[3],ds[2],ds[1],ds[0])) + "\n"

"""
1010110101001011
000000000000000000000000000044363

1010110101010100101010101101010101001010101011010101010010101010110101010100101010101101010101001010
000858292211276479224037767828810
"""

print len(s)
r.clipboard_append(s)
