.text
main:
	li $v0, 5
	syscall
	move $t0, $v0
	li $v0, 5
	syscall
	move $t1, $v0
	div $t0, $t1
	mfhi $t2
	add $a0, $t2, 0
	li $v0, 1
	syscall
	li $v0, 10
	syscall
