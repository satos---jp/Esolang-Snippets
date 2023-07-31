#coding: utf-8
from Tkinter import Tk


init = """
0 0 0
0 0 0 
1 1 1 
"""

#33����126�܂ł�printable.

var_num = 0
def getv():
	#�ꌅ�ϐ��͔�����B
	global var_num
	var_num += 1
	res = ""
	nv = var_num
	d = 127-33
	ok = True
	while nv>0:
		nc = nv%d+33
		"""
		if (
			(0x20<=nc and nc <= 0x2f) or  
			(0x3a<=nc and nc <= 0x40) or 
			(0x5b<=nc and nc <= 0x40) or 
		"""
		res += chr(nc)
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

#�ꎞ�ϐ����̏Փ˂�h�����߂�d�Ő[��������B
#���ƁA�������O�������Ă��Ă����v�Ȃ悤�ɐ݌v���܂��傤...
#��̓I�ɂ́As�ɑ���������ƂɁAa��b���Q�Ƃ���Ɖ��Ă�\��������B

def nand(s,a,b): # s = a nand b
	return "%s %s %s\n" % (s,a,b)

def one(a): #a��1����
	return nand(a,a,'0')

def not_(s,a): #s = !a
	if s==a: #174122 -> 144684
		return "%s %s\n" % (s,'1')
	else:
		return nand(s,a,a)

def zero(a): #a��0����
	#return one(a) + not_(a,a)
	return "%s 1 1\n" % a #144684 -> 144098

def and_(s,a,b): # s = a & b
	return nand(s,a,b) + not_(s,s)

def mov(s,a): # s := a
	return and_(s,a,a)

def or_(s,a,b): # s = a | b
	return not_(a,a) + not_(b,b) + nand(s,a,b) #������a,b�𔽓]�����Ă�̂�΂��Ȃ��ł���...?????

def xor(s,a,b): # s = a ^ b
	#return mov(mb,b) + not_(ta,a) + not_(tb,b) + nand(s,a,tb) + nand(tb,ta,mb) + nand(s,s,tb)
	tc,td,te = getvs(3)
	return (
		nand(tc,a,b) + 
		nand(td,a,tc) + 
		nand(te,b,tc) + 
		nand(s,td,te) #144098 -> 119922
	)
def ha(c,s,a,b): #�n�[�t�A�_�[�B
	#s = a ^ b
	#c = a & b
	ma, mb = getvs(2)
	return mov(ma,a) + mov(mb,b) + xor(s,ma,mb) + and_(c,ma,mb)

def fa(c,s,p,q,r): #�t���A�_�[�B #���ꂪ����ɂ���������
	#���ۂ́Aa,b,a,b,c�̌`�̂݁B
	#s = a ^ b
	#c = a & b
	mp, mq, mr, tp= getvs(4)
	res =  (
		mov(mp,p) + mov(mq,q) + mov(mr,r) + 
		ha(c,s,mp,mq) + ha(tp,s,s,mr) + or_(c,tp,c)
	) #29���߂�217��������B�����B
	#print res.count("\n"),
	return res
	
def inc(ds): #ds�ŕ\�����z����C���N�������g����B
	tp,tq = getvs(2)
	res = one(tp)
	for s in ds:
		res += and_(tq,tp,s)
		res += xor(s,tp,s)
		res += mov(tp,tq)
	return res

def neq(r,cs,ds): #cs��ds���ׂ����ʂ�r�Ɋi�[����B�������Ȃ�0�B
	res = zero(r)
	tt = getv()
	for p,q in zip(cs,ds):
		res += xor(tt,p,q)
		res += or_(r,r,tt)
	return res

"""
def add(c,cs,ds): #cs += ds, c�ɂ͌��オ�肪����
	#print cs,ds
	#nc,ns = getvs(2)
	res = zero(c)
	for p,q in zip(cs,ds):
		res += fa(c,p,c,p,q) #�����Ȃ�ȁ[�B
		#res += fa(nc,ns,nc,p,q)
		#res += mov(p,ns) # 88618 -> 84978 -> 84068
	#res += mov(c,nc) 
	#print len(res) #��������945���� ��65�񂠂����̂ł������킩��߁B
	return res

def movv(cs,ds): #cs := ds
	res = ""
	for t,d in zip(cs,ds):
		res += mov(t,d)
	return res

def sub(c,cs,ds): #cs += ds, c�ɂ͕����łȂ����ǂ���������
	td = getvs(len(ds))
	res = movv(td,ds)
	for t in td:
		res += not_(t,t)
	res += inc(td)
	res += add(c,cs,td)
	return res

def geq(r,ds,cs): #ds>=cs��
	td = getvs(len(ds))
	return movv(td,ds) + sub(r,td,cs) #+ "0 0 1 1 %s %s %s %s" % (td[3],td[2],td[1],td[0]) + "\n"
"""


def lls(ds): #�_�����V�t�g
	#�ϐ����������Ƃ����׈��ȕ��@���Ƃ��1600�ւ�
	res = ""
	for i in range(0,len(ds)-1)[::-1]:
		res += mov(ds[i+1],ds[i])
	res += mov(ds[0],'0')
	return res

"""
def andv(ds,a): #ds = map(lambda x: x & a,ds)
	res = ""
	for d in ds:
		res += and_(d,d,a)
	return res
"""

#add��1000����������̂�΂����B

#def sub5(r,ds): #ds -= 5���v�Z���āA�񕉂Ȃ�r��1


def add0or5(a,b,c,r): # cba += r0r ������
	tp,ic,ib = getvs(3)
	#return add(tp,[a,b,c],[r,'0',r])
	res = ""
	res += and_(ib,a,r)
	res += and_(ic,ib,b)
	res += xor(ic,ic,r)
	res += xor(c,c,ic)
	res += xor(b,b,ib)
	res += xor(a,a,r) #64740 -> 49252
	return res

def sub5(r,a,b,c,d): # dcba -= 0101 ������B�ŁAr�ɁAdcba += 1011�̌J��オ��̌��ʂ�����
	#return sub(r,[a,b,c,d],['1','0','1','0'])
	#return add(r,[a,b,c,d],['1','1','0','1']) #49252 -> 38372
	
	ib,ic,id,ir = getvs(4) #38372 -> 15662
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
	
def mo5sub5(r,ds): 
	#if ds>=5 then {ds -= 5; r=1;} else {r=0;}
	tq = getvs(1)
	res = ""
	#res += geq(r,ds,['1','0','1','0'])
	#res += sub(tq,ds,[r,'0',r,'0']) 
	#res += not_(r,r)

	#res += sub(r,ds,['1','0','1','0'])
	res += sub5(r,ds[0],ds[1],ds[2],ds[3])
	#res += not_(r,r)
	#res += add(tq,ds,[r,'0',r,'0']) #84068 -> 71716

	res += add0or5(ds[0],ds[1],ds[2],r) #������0����4�̂ǂꂩ�B
	
	print res.count("\n"),
	res += zero(ds[3])
	return res


def nibai(dss): #4bit���g���C���f�B�A��(10�i)�̂��̂��e�����Ƃɏォ��2�{���Ă���
	ls = len(dss)
	res = ""
	tp,tq = getvs(2)
	tds = getvs(4)
	for i in range(0,ls-1)[::-1]:
		ds = dss[i]
		res += mo5sub5(tp,ds)
		
		#res += add(tq,dss[i+1],[tp,'0','0','0'])
		res += not_(dss[i+1][0],tp) #119922 -> 90322
		res += lls(ds)
	return res


r = Tk()
r.clipboard_clear()

import sys

ketan = 33
if len(sys.argv)>=2:
	ketan = 3

cnt = [getv() for i in xrange(7)] #38372 -> 38030
ans = [[getv() for j in xrange(4)] for i in xrange(ketan)]
#�ϐ����Z������
#cnt = ['c' + str(i) for i in xrange(10)]
#ans = [['a' + str(i) + ',' + str(j) for j in xrange(4)] for i in xrange(33)]

s = (
	init + 
	#movv(cnt,['0'] * 10) + 
	""
)

""" 90322 -> 88618
for ds in ans:
	s += movv(ds,['0'] * 4)
"""

tp = getv()
s += (
	'x' + "\n" + 
	nibai(ans) + 
	'x x x x x x x x b' + "\n" + 
	#add(tp,ans[0],['b','0','0','0']) +   #700�㌸�肻��
	mov(ans[0][0],'b') + #�͂��B 15662 -> 14807
	inc(cnt) + 
	#"0 0 1 1 %s %s %s %s" % (cnt[3],cnt[2],cnt[1],cnt[0]) + "\n" + 
	#geq(tp,cnt,['1','1','0','0']) + 
	#"0 0 1 1 0 0 0 %s" % tp + "\n" + 
	neq('x',cnt,map(chr,map(ord,'1100100'[::-1]))) + 
	#neq('x',cnt,map(chr,map(ord,'0010000'[::-1]))) + 
	'x' + "\n" +
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

"""
s = (
	init + 
	't x x x x a b c d' + "\n" + 
	mo5sub5('r',['d','c','b','a']) + 
	'0 0 1 1 a b c d' + "\n" + 
	'0 0 1 1 0 0 0 r' + "\n" + 
	""
)
"""
"""
s = (
	init + 
	't x x x x x c b a' + "\n" + 
	't x x x x x x x r' + "\n" + 
	add0or5('a','b','c','r') + 
	'0 0 1 1 0 c b a' + "\n" + 
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