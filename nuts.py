import lambda_calculus
from lambda_calculus import str2lam,Var,Abs,App

def lam2nuts(lam,d=0):
	if isinstance(lam,Var):
		#print('v',d,lam.v)
		if lam.v == 'P':
			return ":" 
		elif lam.v == "G":
			return "::"
		elif lam.v == "N":	
			return "\""
		else:
			#print("\"" + lam.v + "\"")
			return '.'*(lam.idx+1)
	elif isinstance(lam,Abs):
		return "'"+lam2nuts(lam.p,d+1)
	elif isinstance(lam,App):
		return "," + lam2nuts(lam.p,d) + ' ' + lam2nuts(lam.q,d)

#prog = lam2nuts(str2lam("(d.e.(e (G d)) d) N P"))
#prog = lam2nuts(str2lam("(d.e.(e (G d)) d) N P"))
n = 50
# lambda_calculus.n50 = str2lam('s. z. ' + 's (' * n + ' z' + ')'*n)


# 					(($iszero ($sub c *32)) q $false)


s = 'N'
s = '($pair %s $false)' % s
for _ in range(75-33):
	s = '($pair %s N)' % s
s = '($pair %s $true)' % s
for _ in range(32-11):
	s = '($pair %s N)' % s
s = '($pair %s $true)' % s
for _ in range(10):
	s = '($pair %s N)' % s

s = '(n. $snd (n $fst %s))' % s

lambda_calculus.isle32 = str2lam(s)


s = 'N'
s = '($pair %s $false)' % s
for _ in range(84-33):
	s = '($pair %s N)' % s
s = '($pair %s $true)' % s
for _ in range(32):
	s = '($pair %s N)' % s

s = '(n. $snd (n $fst %s))' % s

lambda_calculus.isle32T = str2lam(s)




prog = str2lam('''
	($zcon (f. r. 
		(e. (f. g. e) (P *33 N) (G N))
		(*50 
			(q. (c. 
				(t. 
					(($isle32 c) q $false)
				) 
				(P (q c *33) N)
			) (G N))
			r
		)
		f (a. a) r
	))
	(($zcon (f. r.
		(c. 
			(x. 
				($isle32T c) (
					f 
				) (
					(i. i)
				) r
			) ((P c) N)
		) (G N) 
	)) $true)
''')




#prog = str2lam("P (G N) N ")
#prog = str2lam("(d.e.(e (G d)) d) N P")


'''
 ((
	 (Z (f. r. 
	 		(g. (x. I) g @ (i. .T g))
	 		(
		 		(x. x I ((D ( ( (f x)))))) 
		 		($n50 
		 			(q. K I q @ (i. 
			 			(p. p .X ((i ?U $iv2tf) .U .L) p) (
			 				(i ?K $iv2tf) $true q
			 			)
		 			)) 
		 			r
		 		)
		 	)
	 ))
	 (.T
		 (
			 (x. x $false)
			 (Z (f. r. 
				 	r @ (i.
				 		(i ?T $iv2tf) 
				 		I
				 		((D (f .A)))
				 	)
				) I I)
			)
		)
 ) I I)
'''

prog.init_debruijn()
prog = lam2nuts(prog)

#prog = ",,',',..',,.. .. .',..',,.. .. .'',..,,:,::. .\""
open('o','w').write(prog)
print(prog)

