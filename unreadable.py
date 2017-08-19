#coding: utf-8

def putc(x):
	return '\'"' + x

def inc(x):
	return '\'""' + x

def ret1():
	return '\'"""'

def tikuzi(x,y):
	return '\'""""' + x + y

def wnz(x,y):
	return '\'"""""' + x + y

def let(x,y): #x .. number(expression) , let x := y  numberは0以上とする。
	return '\'""""""' + x + y

def get(x):
	return '\'"""""""' + x

def dec(x):
	return '\'""""""""' + x

def tern(x,y,z):
	return '\'"""""""""' + x + y + z

def getc():
	return '\'""""""""""'


def retx(x):
	res = ret1()
	if x>=1:
		while x>1:
			res = inc(res)
			x -= 1
	else:
		while x<1:
			res = dec(res)
			x += 1
	return res


def incmem(x):
	return let(x,inc(get(x)))

def decmem(x):
	return let(x,dec(get(x)))

def incn(x,n):
	for i in xrange(n):
		x = inc(x)
	return x

from Tkinter import Tk

r = Tk()
r.clipboard_clear()


def notx(x):
	return tern(x,dec(ret1()),ret1())

def getn(n):
	return get(retx(n))
s = (
	tikuzi(
		wnz(
			let(
				ret1(),
				inc(getc())
			),
			incmem(getn(1))
		), #input
		tikuzi(
			tikuzi(
				let(ret1(),ret1()),
				wnz(
					notx(get(inc(getn(1)))),
					incmem(ret1())
				)
			), #ここまでで、mem[1]が0x31になってるはず。
			wnz(
				get(incmem(ret1())), 
				wnz( #0になるまでoutput.
					get(getn(1)),
					tikuzi(
						putc(dec(getn(1))),
						decmem(getn(1))
					)
				)
			)
		)
	)
)
r.clipboard_append(s)

print s

exit(-1)

s = (
	#putc(let(dec(ret1()),dec(retx(0x65))))
	
	#wnz(inc(putc(getc())),ret1()) 
	#echo ただし 
	# runtime error: unichr() arg not in range(0x110000) (wide Python build)
	#で落ちる。

	tikuzi(
		wnz(
			let(
				ret1(),
				inc(getc())
			),
			incmem(get(ret1()))
		), #input
		tikuzi(
			let(ret1(),retx(0x30)),
			wnz(
				get(incmem(ret1())), 
				wnz( #0になるまでoutput.
					get(get(ret1())),
					tikuzi(
						putc(dec(get(ret1()))),
						decmem(get(ret1()))
					)
				)
			)
		)
	)
)
r.clipboard_append(s)

"""
s = (
	tikuzi(
		wnz(
			let(
				ret1(),
				inc(getc())
			),
			incmem(get(ret1()))
		), #input
		tikuzi(
			let(ret1(),retx(0x30)),
			wnz(
				get(incmem(ret1())), 
				putc(dec(get(ret1())))
			)
		)
	)
)
"""

"""
s = (
	tikuzi(
		let(ret1(),getc()),
		tikuzi(
			incmem(ret1()),
			putc(get(ret1()))
		)
	)
)
"""

#s = putc(getc())


#print s
