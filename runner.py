import os, sys
import importlib
from pathlib import PurePath

def main():
	if len(sys.argv) <= 1:
		sys.stderr.write('Usage: python3 %s [filename]\n' % sys.argv[0])
		sys.stderr.write('Example: python3 %s code/language.py\n' % sys.argv[0])
		exit(-1)
	fn = sys.argv[1]
	fn = os.path.splitext(fn)[0]
	m = '.'.join(PurePath(fn).parts)
	importlib.import_module(m)

if __name__ == '__main__':
	main()

