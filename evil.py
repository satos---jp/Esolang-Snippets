#coding: utf-8

from Tkinter import Tk

r = Tk()
r.clipboard_clear()


s = (
	'zy' +
	'a' + 'cy' * 10 + 'i' + # 0 , 1 , .... 1
	#wheeel�ʒu���C������!!
	'oo' + 
	'a' * 99 + 'k' + #inputnum��Penal�ɁB
	'm' + 
		'x' + 
		
		'r' + 'u' * 47 + 
		'j' + 
			'i' + 
			'u' + 'sb' + #dec -> non0��loop
		
		#�Ή�����Wheel��inc.
		'pay' + 
		
		'j' + #*wheel��0�ɂȂ�܂�loop
			'i' + 'p' + 'sb'
		
		#decrement -> 0�łȂ��Ȃ�loop.
		'x' + 'guk' + 
		'sb' + 
	
	#�����܂ł�input
	
	#�e�X�g�o�́B
	#('i' + 'p' + 'a' * ord('A') + 'w') * 10 + 'i' + 
	
	'i' + 
	'z' + 'a' * 0x30 + 'k' + 
	'm' + 
		'x' + 
		'puy' + #dec.
		#����wheel��0�ɂȂ�܂�putc.
		'j' + 
			'gw' + 
			#dec->check
			'puy' + 'sb' + 
		#penal��inc.
		'gak' + 
		
		#nextwheel -> 0�łȂ��Ȃ�loop.
		'x' + 
		'ip' + 'sb' + 
	''
)
r.clipboard_append(s)
