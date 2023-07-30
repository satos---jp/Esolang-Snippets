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

def let(x,y): #x .. number(expression) , let x := y  number‚Í0ˆÈã‚Æ‚·‚éB
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
	for i in range(n):
		x = inc(x)
	return x


def decn(x,n):
	for i in range(n):
		x = dec(x)
	return x

def notx(x):
	return tern(x,dec(ret1()),ret1())

def getn(n):
	return get(retx(n))

def tikus(v):
  res = v[0]
  v = v[1:]
  while len(v)>0:
    res = tikuzi(res,v[0])
    v = v[1:]
  return res

def letn(n,x):
  return let(retx(n),x)

s = (
	tikus([
		wnz(decn(putc(getc()),84),retx(1)),
		letn(1,retx(0)),
		wnz(dec(getn(1)),tikus([
			letn(2,retx(50)),
			wnz(getn(2),tikus([
				tern(
					tern(
						decn(letn(3,getc()),75),
						getn(1),
						letn(1,retx(1)),
					),
					putc(inc(getn(3))),
					putc(getn(3)),
				),
				letn(2,dec(getn(2))),
			])),
			putc(inc(getc())),
		])),
	])
)
"""
    letn(6,retx(5)),
    letn(7,retx(42)),
    wnz(getn(6),tikus([
      let(getn(6),decn(getc(),48)),
      letn(6,dec(getn(6))),
    ])),
    #putc(incn(getn(2),48)),
    #putc(incn(getn(2),48)),
    wnz(getn(2),tikus([
      letn(1,incn(getn(1),10)),
      letn(2,dec(getn(2))),
    ])),
    wnz(getn(5),tikus([
      letn(4,incn(getn(4),10)),
      letn(5,dec(getn(5))),
    ])),
    #inputted 3 :: h, 1 :: w
    
    #putc(retx(65)),
    wnz(getn(1),tikus([
      putc(getn(7)),
      letn(2,inc(getn(2))),
      letn(1,dec(getn(1))),
    ])),
    putc(retx(10)),
    letn(2,decn(getn(2),2)),
    letn(4,decn(getn(4),2)),
    wnz(getn(4),tikus([
      putc(getn(7)),
      wnz(getn(2),tikus([
        putc(retx(32)),
        letn(2,dec(getn(2))),
        letn(1,inc(getn(1))),
      ])),
      wnz(getn(1),tikus([
        letn(2,inc(getn(2))),
        letn(1,dec(getn(1))),
      ])),
      putc(getn(7)),
      putc(retx(10)),
      letn(4,dec(getn(4))),
    ])),
    letn(2,incn(getn(2),2)),
    
    wnz(getn(2),tikus([
      putc(getn(7)),
      letn(2,dec(getn(2))),
    ])),
  ])
)
"""
open('o','w').write(s)
#print(s)

