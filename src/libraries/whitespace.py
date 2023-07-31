#coding: utf-8

def i2w(x):
	if x>=0:
		res = " "
	else:
		res = "\t"
		x *= -1
	ad = ''
	while x>0:
		ad = ("\t" if x%2==1 else " ") + ad
		x //= 2
	res += ad + "\n"
	return res 

#http://www.kembo.org/whitespace/tutorial.html
#http://koturn.hatenablog.com/entry/2015/08/10/000000

def push(x):
	return "  " + i2w(x)

geti = "\t\n\t\t"
getc = "\t\n\t "
outi ="\t\n \t"
putc = "\t\n  "

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

def jmpng(x): 
	return "\n\t\t" + x + "\n"
def jz(x): 
	return "\n\t " + x + "\n"

#print map(ord,i2w(-11))

#print push(11) + outi + endp

def load(x):
	return push(x) + heap_l
def store(x):
	return push(x) + swap + heap_s


def jnz(x): 
	return dup + mul + push(0) + swap + sub + jmpng(x)


def label(x):
	return mark(x)

getc = push(0) + getc + load(0)

s = (
	label(" ") + 
		getc + dup + putc +  
		push(3) + 
		mod + 
	jnz(" ") +
	push(0) + 
	label("\t") + 
		push(49) + 
		label("\t ") + 
			swap + 
			dup + getc + add + dup + putc + 
			push(3) +
			mod + 
			jnz("\t\t") + 
				push(1) + add + 
			label("\t\t") +
			swap + 
			dup + push(1) + sub + swap + 
		jnz("\t ") + 
		getc + swap + sub + putc + 
		dup + push(2) + sub + 
	jnz("\t") + endp
)

#s = getc + endp
#r.clipboard_append(s)
open('o','w').write(s)
#print getc + getc + endp[:-1]
