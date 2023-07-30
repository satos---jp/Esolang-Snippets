#coding: utf-8

from Tkinter import Tk

r = Tk()
r.clipboard_clear()


s = (
	'zy' +
	'a' + 'cy' * 10 + 'i' + # 0 , 1 , .... 1
	#wheeel位置を修正せよ!!
	'oo' + 
	'a' * 99 + 'k' + #inputnumをPenalに。
	'm' + 
		'x' + 
		
		'r' + 'u' * 47 + 
		'j' + 
			'i' + 
			'u' + 'sb' + #dec -> non0でloop
		
		#対応するWheelをinc.
		'pay' + 
		
		'j' + #*wheelが0になるまでloop
			'i' + 'p' + 'sb'
		
		#decrement -> 0でないならloop.
		'x' + 'guk' + 
		'sb' + 
	
	#ここまででinput
	
	#テスト出力。
	#('i' + 'p' + 'a' * ord('A') + 'w') * 10 + 'i' + 
	
	'i' + 
	'z' + 'a' * 0x30 + 'k' + 
	'm' + 
		'x' + 
		'puy' + #dec.
		#今のwheelが0になるまでputc.
		'j' + 
			'gw' + 
			#dec->check
			'puy' + 'sb' + 
		#penalのinc.
		'gak' + 
		
		#nextwheel -> 0でないならloop.
		'x' + 
		'ip' + 'sb' + 
	''
)
r.clipboard_append(s)
