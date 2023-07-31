import re
def compile(prog):
	prog = re.split('(\d*.)',prog)
	prog = list(filter(lambda x: x!='',prog))
	#print(prog)
	def f(x):
		if len(x)>1:
			x = x[-1] * int(x[:-1])
		return x
	return ''.join(map(f,prog))


assert compile('12+.3>')==12*"+" + "." + 3*">"
