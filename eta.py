#coding: utf-8
from Tkinter import Tk

def push(x):
	res = ""
	while x>0:
		res = ['H','T','A','O','I','N','S'][x%7] + res
		x /= 7
	return "NH"+res+"E"

"""
NOE
NHEH
NNET
NTENHET
NtoneO
NTES
NTENAET
"""

div = 'E'

def jnz(addr):
	return push(addr)+'T'

sub = 'S'

def tot(x): #to top(0 indexed)
	return push(x) + 'H'

def dup(x): #duplicate(0 indexed)
	return push(0)+push(x)+'S'+'H'

add = push(0)+tot(1)+sub+sub

def jmp(addr):
	return push(1) + jnz(addr)

r = Tk()
r.clipboard_clear()

ctp =  dup(0) + push(48) + add + 'O' + push(10) + 'O'

pop = dup(0) + sub + dup(0) + 'T'

k = 40
d = 100
s = (
	push(k+5) + '\n' + 
	push(0) + tot(1) + '\n' + 
	push(1) + sub + '\n' + 
	dup(0) + jnz(2) + '\n' + 
	
	push(d) + '\n' + 
	push(k) + 'I' + push(48) + sub + '\n' + 
	tot(k+2) + dup(0) + add + add + push(10) + div + '\n' + 
	tot(3) + tot(3) + tot(3) + '\n' + # ... d,k,q,r  -> r,d,k,q
	tot(1) + push(1) + sub + tot(1) + dup(1) + '\n' + 
	jnz(7) + '\n' + 
	pop + pop + '\n' + 
	push(1) + sub + '\n' + 
	dup(0) + jnz(6) + '\n' + 
	pop + '\n' + 

	push(k) + '\n' + 
	tot(1) + push(48) + add + 'O' + '\n' + 
	push(1) + sub + '\n' + 
	dup(0) + jnz(16) + '\n' + 
	jmp(0)
)
r.clipboard_append(s)

exit(-1)

"""
s = (
	push(4) + ctp + push(0) + '\n' + 
	dup(0) + add + ctp + '\n' + 
	'I' + push(48) + sub + add + '\n' +
	ctp + tot(0) + ctp + push(1) + sub + ctp  + tot(0)+ '\n' + 
	jmp(0)
)
r.clipboard_append(s)
exit(-1)
"""

s = (
	push(100) + push(0) + '\n' + 
	dup(0) + add + '\n' + 
	'I' + push(48) + sub + add + '\n' + 
	tot(1) + push(1) + sub + tot(1) + dup(1) + '\n' +
	jnz(2) + '\n' + 
	push(10) + div + push(48) + add + 'O' + '\n' + 
	dup(0) + jnz(6) + '\n' + 
	jmp(0)
)
r.clipboard_append(s)
