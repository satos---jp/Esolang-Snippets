import emoji_table


table = list(map(lambda x: x.split(b':')[0],filter(lambda x: x != b'',open('emoji_table.txt','rb').read().split(b'\n'))))
#print(table)

strtable = emoji_table.emoji_mean

def comp(s):
	s = s.split(b';')
	res = b""
	for d in s:
		ds = d.decode('utf-8')
		if d == b"":
			continue
		elif ds in strtable:
			res += table[strtable.index(ds)]
		elif b"(" in d:
			res += comp(eval(d))
		else:
			print("constr",d)
			res += d
	return res

def pushn(x):
	if x == 0:
		return b"nil;len;"
	elif x > 0:
		return b"[;" + (b"a"*x) + b";];len;"
	else:
		return pushn(0) + pushn(-x) + b"sub;"

# input string is on the top of the stack.
#prog = b'pushn(0);swap;[;q;];add;[;dup;[;];=;not;];[;dup;pushn(-6);pushn(-1);substr;[;sushi;];=;if;swap;pushn(1);add;swap;fi;pushn(0);pushn(-1);substr;];while;swap;print'

prog = (
	#b'[;a;];swap;set;' + 
	#b'[;f;];[;dup;pushn(1);add;[;a;];load;substr;];' + 
	b'dup;dup;pushn(0);pushn(50);substr;swap;len;pushn(51);div;pushn(1);sub;[;dup;pushn(0);>;];[;swap;dup;print;swap;pushn(1);sub;];while;ceil;' + 
	# all, "     T    ", 0
	b'swap;[;a;];set;' + 
	# all, 0
	b'swap;dup;len;dup;pushn(51);sub;swap;substr;' +
	# 0,"     K    "
	b'[;b;];set;pushn(0);[;c;];set;[;];[;r;];set;' + 
	# q,0
	b'[;dup;pushn(1);add;swap;[;a;];load;swap;dup;pushn(1);add;substr;ord;pushn(33);<;];[;dup;[;b;];load;swap;dup;pushn(1);add;substr;ord;dup;[;c;];load;add;chr;[;r;];load;swap;add;[;r;];set;pushn(75);=;[;c;];load;add;[;c;];set;];while;[;r;];load;[;x;];add;print;' +
b'')
open('o','wb').write(comp(prog))



