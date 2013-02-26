.text
main:
	li $a0, -1
	li $t0, 9
	mult $t0, $a0
	mflo $t0
	li $a0, -1
	mult $t0, $a0
	mflo $t0
	li $a0, -1
	mult $t0, $a0
	mflo $t0
	li $a0, -1
	mult $t0, $a0
	mflo $t0
	li $a0, 2
	mult $t0, $a0
	mflo $t4
	add $a0, $t4, 0
	li $v0, 1
	syscall
	li $v0, 10
	syscall
