.text
main:
	li $v0, 5
	syscall
	move $t0, $v0
	li $a0, 11
	mult $t0, $a0
	mflo $t1
	add $a0, $t1, 0
	li $v0, 1
	syscall
	li $v0, 10
	syscall
