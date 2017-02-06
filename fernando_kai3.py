#coding: utf-8
from Tkinter import Tk


init = """
0 0 0
0 0 0 
1 1 1 
"""

def nand(s,a,b): # s = a nand b
	if s==a: #����͂����B 10242 -> 10162
		return "%s %s\n" % (s,b)
	elif s==b:
		return "%s %s\n" % (s,a)
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
	tc,td,te = ('A','B','C')
	if a==s:
		te = s #����!!�B 10162 -> 9798
	return (
		nand(tc,a,b) + 
		nand(td,a,tc) + 
		nand(te,b,tc) + 
		nand(s,td,te) #144098 -> 119922
	)

def inc(ds): #ds�ŕ\�����z����C���N�������g����B
	tp,tq = ('D','E')
	res = one(tp)
	for s in ds:
		res += and_(tq,tp,s)
		res += xor(s,tp,s)
		res += mov(tp,tq)
	return res

def neq(r,cs,ds): #cs��ds���ׂ����ʂ�r�Ɋi�[����B�������Ȃ�0�B
	res = zero(r)
	tt = 'F'
	for p,q in zip(cs,ds):
		res += xor(tt,p,q)
		res += or_(r,r,tt)
	return res


def add0or5(a,b,c,r): # cba += r0r ������
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

def sub5(r,a,b,c,d): # dcba -= 0101 ������B�ŁAr�ɁAdcba += 1011�̌J��オ��̌��ʂ�����
	#return sub(r,[a,b,c,d],['1','0','1','0'])
	#return add(r,[a,b,c,d],['1','1','0','1']) #49252 -> 38372
	
	ib,ic,id,ir = ('J','K','L','M') #38372 -> 15662
	res = ""
	res += not_(a,a)
	res += not_(ic,b)
	res += nand(ic,ic,a)
	res += nand(id,ic,c)
	res += not_(d,d)
	res += nand(ir,id,d) #���k!!. 10498 -> 10242
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
	res += add0or5(ds[0],ds[1],ds[2],r) #������0����4�̂ǂꂩ�B
	
	#print res.count("\n"),
	#ls = len(res)  #3/4�Ȃ̂ŁA30���ߒ��ɗ}����΂悢(�}������)
	#�Ƃ������A����10���ߒ����΂悢�B
	#res = res[0:ls*3/4]
	#res += zero(ds[3]) #�V�t�g����̂ŕs�v�B 11935 -> 11711
	return res

def lls(ds): #�_�����V�t�g
	#�ϐ����������Ƃ����׈��ȕ��@���Ƃ��1600�ւ�?
	#��������Ȃ��Ƃ����Ȃ��̂ł���....�炢�Ȃ�
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
	#res += zero(ds[0]) #����͂����B 11711 -> 11551
	#�ǂ���炱������Ƃ������炵���B(�����Ă��͉�����not���J��オ�邽�߁B���ꌅ��input�ŏ�����) ������230����̂ŁA
	#10704 -> 10498�ɂȂ�
	return res


def nibai(dss): #4bit���g���C���f�B�A��(10�i)�̂��̂��e�����Ƃɏォ��2�{���Ă���
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

#�ϐ�����A����R�܂Ŋ���U�邱�Ƃɂ��A
#14807 -> 11935

#33����126�܂ł�printable.

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
			#�͂Ă�!! 11511 -> 10704
			return getv()
	
	return res

def getvs(x):
	if x==1:
		return getv()
	else:
		return [getv() for i in xrange(x)]

#�ꎞ�ϐ����̏Փ˂�h�����߂�d�Ő[��������B
#���ƁA�������O�������Ă��Ă����v�Ȃ悤�ɐ݌v���܂��傤...
#��̓I�ɂ́As�ɑ���������ƂɁAa��b���Q�Ƃ���Ɖ��Ă�\��������B


r = Tk()
r.clipboard_clear()

import sys

ketan = 33
if len(sys.argv)>=2:
	ketan = 3

ans = [[getv() for j in xrange(4)] for i in xrange(ketan)]
cnt = [getv() for i in xrange(7)] #38372 -> 38030
#�ϐ����Z������
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
	mov(ans[0][0],'R') + #�͂��B 15662 -> 14807
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
