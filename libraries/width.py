
code = "[(lambda x: globals().__setitem__('q',x) if 'T' in x else (exit(print(q+'\\n'+x.rstrip()+(len(q.rstrip())-len(x.rstrip()))*'*')) if 'K' in x else print(q)))(input()) for _ in range(100)]"



strs = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~\n\t"

code = list(map(lambda x: strs.index(x),code))

cs = "ifcaFAwQMW"


def strfy(s):
	res = "G"
	for v in s:
		res += cs[v//10] + cs[v%10]
	res += "G"
	return res

code = strfy(code)
print(code)

code += cs[6]+cs[6]+cs[5]+cs[6] #2212
print(code)

