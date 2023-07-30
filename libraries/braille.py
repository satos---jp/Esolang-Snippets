import brainf_ck

def compile(prog):
	pass


prog = "+[,.>12+[<7->-]<]+[>>[-]+++++[<++++++++++>-]<[>,+<<[>>->+<<<-]>>.<<+++++[>>---------------<<-]>>[>[<<<+>>>-]<[+]]>[-]<<-]>,+.<<]"

import sys
sys.stdout.write('\x28\xff')

bits = ["⠀","⠈","⠐","⠠","⢀","⠁","⠂","⠄","⡀"]

bits = list(map(lambda x: x.encode('utf-8'),bits))


prog = brainf_ck.compile(prog)
prog = compile(prog)
#print(len(prog))
#open('o','w').write(prog)

