.text
main:
	li $t0, 1
	add $t1, $t0, 0
	add $t1, $t1, 0
	add $a0, $t1, 0
	li $v0, 1
	syscall
	li $v0, 10
	syscall
