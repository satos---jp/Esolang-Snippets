def push(x):
	assert x>=0
	return (x+5)*' '+'+'

dup = " +"
swap = "  +"
rot = "   +"
drop = "    +"
add = "*"
sub = " *"
mult = "  *"
div = "   *"
mod = "    *"
putc = " ."
putn = "."
getc = " ,"

def label(x):
	return ' '*x + '`'
def jnz(x):
	return ' '*x + '\''



prog = (
	label(0) + 
		getc + dup + putc +  
		push(3) + 
		mod + dup + 
	jnz(0) +
	label(1) + 
		push(7) + dup + mult + dup + # flag,cnt,cnt
		label(2) + # flag,chr,cnt
			swap + putc + swap + dup + # cnt,flag,flag
			getc + add + dup + rot + # cnt,flag+getc,flag,flag+getc
			push(2) + mod + 
			add + # cnt,flag+getc,flag'
			rot + swap + # flag',flag+getc,cnt,
			dup + push(1) + sub + swap + # flag,cnt',cnt
		jnz(2) + # flag,cnt'
		#add + dup + push(2) + dup + getc + add + putc + sub + 
		drop + dup + push(2) + sub + 
	jnz(1) + 	
"")


prog = (
	label(0) + 
		getc + dup + putc +  
		push(3) + 
		mod + dup + 
	jnz(0) +
	label(1) + 
		push(7) + dup + mult + # flag,cnt
		label(2) + 
			swap + 
			dup + getc + add + dup + putc + # cnt,flag,flag+getc
			push(2) +
			mod + add + 
			swap + # flag',cnt
			dup + push(1) + sub + swap + # flag,cnt',cnt
		jnz(2) + # flag,cnt'
		#add + dup + push(2) + dup + getc + add + putc + sub + 
		getc + swap + sub + putc + 
		dup + push(2) + sub + 
	jnz(1) + 	
"")


#110byte
prog = (
	label(0) + 
		getc + dup + putc +  
		push(3) + 
		mod + dup + 
	jnz(0) +
	label(1) + 
		dup + sub + 
		push(7) + dup + mult + # flag,cnt
		label(2) + 
			swap + 
			dup + getc + add + dup + putc + # cnt,flag,flag+getc
			push(2) +
			mod + add + 
			swap + # flag',cnt
			dup + push(1) + sub + swap + # flag,cnt',cnt
		jnz(2) + # flag,cnt'
		getc + swap + sub + dup + putc + 
	jnz(1) + 	
"")

# 109byte
prog = (
	label(0) + 
		getc + dup + putc +  
		push(3) + 
		mod + dup + 
	jnz(0) +
	label(1) + 
		dup + #0,0,cnt
		push(7) + dup + mult + # flag,cnt
		label(2) + 
			swap + 
			dup + getc + add + dup + putc + # cnt,flag,flag+getc
			push(2) +
			mod + add + 
			swap + # flag',cnt
			dup + push(1) + sub + swap + # flag,cnt',cnt
		jnz(2) + # flag,cnt'
		# flag,-1
		getc + swap + sub + #,flag,getc+1
		add + dup + putc + 
	jnz(1) + 	
"")


# 
prog = (
	label(0) + 
		getc + dup + putc +  
		push(3) + 
		mod + dup + 
	jnz(0) +
	getc + 
	label(1) + 
		push(0) + #0,cnt
		push(7) + dup + mult + # flag,cnt
		label(2) + 
			swap + 
			dup + getc + add + dup + putc + # cnt,flag,flag+getc
			push(2) +
			mod + add + 
			swap + # flag',cnt
			dup + push(1) + sub + swap + # flag,cnt',cnt
		jnz(2) + # flag,cnt'
		# flag,-1
		push(42) + putc + 
	jnz(1) + 	
"")



open('o','w').write(prog)

