.text
main:
	li $v0, 5
	syscall
	move $t0, $v0
	li $a0, 2
	sub $t1, $t0, $a0
	add $a0, $t1, 0
	li $v0, 1
	syscall
	li $v0, 10
	syscall
