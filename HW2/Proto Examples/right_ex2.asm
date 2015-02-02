.text
main:
	li $v0, 5
	syscall
	move $t0, $v0
	add $a0, $t0, 0
	li $v0, 1
	syscall
	li $v0, 10
	syscall
