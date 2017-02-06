#coding: utf-8
from Tkinter import Tk

def i2w(x):
	res = ""
	if x>=0:
		res += " "
	else:
		res += "\t"
		x *= -1
	ad = ''
	while x>0:
		ad = ("\t" if x%2==1 else " ") + ad
		x /= 2
	res += " " + ad
	return res

#http://www.kembo.org/whitespace/tutorial.html
#http://koturn.hatenablog.com/entry/2015/08/10/000000

def push(x):
	return "  " + i2w(x) + "\n"

geti = "\t\n\t\t"

getc = "\t\n\t "
	
outi ="\t\n \t"

endp = "\n\n\n" 

heap_s = "\t\t "
heap_l = "\t\t\t"

dup = " \n "

add = "\t   "
sub = "\t  \t"
mul = "\t  \n"
mod = "\t \t\t"
div = "\t \t "

swap = " \n\t"

def mark(x):
	return "\n  " + x + "\n"

def jmpng(x): #負だったら飛ぶやつ
	return "\n\t\t" + x + "\n"

#print map(ord,i2w(-11))

#print push(11) + outi + endp

def load(x):
	return push(x) + heap_l
def store(x):
	return push(x) + swap + heap_s

r = Tk()
r.clipboard_clear()

#s = push(0) + geti + push(0) + heap_l + outi + endp
s = (
	#push(0) + geti + # ここまで、inputをheap(0)にload(ideoneの内部実装はHaskellらしい)
	push(100) + store(1) + #カウンタをheap(1)に
	push(0) + store(2) + #答えをheap(2)に
	mark("\t \t ") + #ラベル
	
	load(2) + push(2) + mul +  #ansを二倍
	push(0) + getc + load(0) + #入力をpush
	push(ord('0')) + sub + add + 
	store(2) + #getcの結果を足してstore
	
	load(1) + #カウンタロード
	push(1) + sub + dup + store(1) + #デクリメントしてstore.
	push(0) + swap + sub + jmpng("\t \t ") + #正だったら飛ぶ
	load(2) + outi + #出力
	endp
)
r.clipboard_append(s)
#print getc + getc + endp[:-1]
