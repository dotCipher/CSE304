# ---------------------------------------------------- #
# CSE 304/504
# HW 1
# Cody Moore
# Part C: MIPS
# ---------------------------------------------------- #
# The text segment
# ---------------------------------------------------- #
.text
main:
	# Prints Ask_Input to console
	la $a0, get_input				# Loads get_input to $a0
	li $v0, 4 					# Load syscall opcode for print-string to $v0
	syscall						# System call - $v0 = 4 , $a0 = get_input
	# Gets input from user, stores in $t0
	li $v0, 5					# Load syscall opcode for read-int to $v0
	syscall						# System call - $v0 = 5
	move $t0, $v0					# Move value from $v0 to $t0
	# Check if $t0 <= 0
	ble $t0, $zero, exit
	# Call factorial function on input
	move $a0, $t0					# Move value from $t0 to $a0
	addi $sp, $sp, -12				# Move stackpointer up 3 words
	sw $t0, 0($sp)					# Store input on top of stack
	sw $ra, 8($sp)					# Store counter at bottom of stack
	jal factorial					# Call factorial function
	# With final return value from factorial in 4($sp):
	lw $s0, 4($sp)					# Load word from return value in 4($sp) to $s0
	
	# Print output with original input value
	la $a0, output1					# Load output1 to $a0
	li $v0, 4					# Load syscall opcode for print-string to $v0
	syscall						# System call - $v0 = 4 , $a0 = output1
	lw $a0, 0($sp)					# Load input value from stack to $t0
	li $v0, 1					# Load syscall opcode for print-int to $v0
	syscall						# System call - $v0 = 1 , $a0 = original input
	la $a0, output2					# Load output2 to $a0
	li $v0, 4					# Load syscall opcode for print-string to $v0
	syscall						# System call - $v0 = 4 , $a0 = output2
	move $a0, $s0					# Move return value from $s0 to $a0
	li $v0, 1					# Load syscall opcode for print-int to $v0
	syscall						# System call - $v0 = 1 , $a0 = return value
	addi $sp, $sp, 12				# Move stack pointer to original state
	
	# Start power function
	li $s1, 1					# Load one (1) to $a0 (Start with total of 1)
	li $s2, -1					# Load -1 to $a1 (Start checking 2^0 after first add)
	# Set up recursive call
loop:
	addi $s2, $s2, 1				# Add one to $s2 register
	addi $sp, $sp, -4				# Move stack pointer up 3 words
	#sw $s0, 0($sp)					# Store $s0 on the top of stack
	sw $ra, 0($sp)					# Store counter on bottom of stack
	move $a0, $s1					# Set up param total for function call
	#move $a1, $s2					# Set up param counter for function call
	move $s4, $s1					# Save previous 2^k value
	jal two_power					# Call power function
	move $s1, $v0					# Get return value of call
	# Set up proper saved values
	# Value of n! already set to $s0
	# Value of 2^k = $s1
	# Value of k = $s2
	# Check divisible of n!=($a0) / 2^k=($a1)
	# Output k
	move $a0, $s0					# Set $a0 to $s0 ( n! = $a0 )
	move $a1, $s1					# Set $a1 to $s1 ( 2^k = $a1 )
	addi $sp, $sp, -4				# Move stack pointer up 2 words
	sw $ra, 0($sp)					# Store counter on top of stack
	jal chk_div					# Function call
	# Check return value
	beq $v0, 1, loop				# Repeat loop to check next iteration
	beq $v0, 0, found				# Last iteration found at k-1
	
found:	
	#addi $s2, $s2, -1				# Subtract one from $s2 register
	# Print output
	la $a0, power1					# Load power1 to $a0
	li $v0, 4					# Load syscall opcode for print-string to $v0
	syscall						# System call - $v0 = 4 , $a0 = power1
	move $a0, $s2					# Load output value of $s1 into $a0
	li $v0, 1					# Load syscall opcode for print-int to $v0
	syscall						# System call - $v0 = 1 , $a0 = k
	la $a0, power2					# Load power2 to $a0
	li $v0, 4					# Load syscall opcode for print-string to $v0
	syscall						# System call - $v0 = 4 , $a0 = power2
	move $a0, $s4					# Load output value of $s1 into $a0
	li $v0, 1					# Load syscall opcode for print-int to $v0
	syscall						# System call - $v0 = 1 , $a0 = 2^k
	
	# Exit program
	j exit						# Jump to exit program

###	Subroutine	###
# Two Power function (two_power)
# input: $a0 = total				, $a1 = counter
# output: $v0 = Total after exponential calc
two_power:
	# Base Case
	#beq $a1, $0, two_power_ret			# Return if input = 0 (2^0 = 1)
	# Recursive case
	mul $a0, $a0, 2					# One iteration of a multply, and store in $a0
	move $v0, $a0
	#addi $a1, $a1, -1				# Subtract 1 from $a0 if $a0 != 0
	jr $ra						# Jump to caller
two_power_ret:
	#sw $a0, 4($sp)					# Store $a0 to caller's return value
	#jr $ra						# Jump to caller
###	End subroutine	###

###	Subroutine	###
# Check if divisible (devisible)
# input: $a0 = divisor1, $a1 = divisor2
# output: $v0 = 0 for false, 1 for true
chk_div:
	divu $a0, $a1
	mfhi $v0
	beqz $v0, chk_divt
	bnez $v0, chk_divf
chk_divf:
	li $v0, 0
	jr $ra
chk_divt:
	li $v0, 1
	jr $ra
###	End subroutine	###

###	Subroutine	###
# Factorial (factorial)
# input: 0($sp) = n
# output: 16($sp) = n!
factorial:
	# Base Case
	lw $t0, 0($sp)					# Load input from top of stack into $t0
	beq $t0, $0, ret_one				# If $t0 is equal to 0, branch to ret_one
	addi $t0, $t0, -1				# Subtract 1 from $t0 if $t0 != 0
	# Recursive case
	addi $sp, $sp, -12				# Move stack pointer up 3 words
	sw $t0, 0($sp)					# Store current working number on top of stack
	sw $ra, 8($sp)					# Store counter at bottom of stack
	jal factorial					# Recursive call
	# Check return value
	lw $ra, 8($sp)					# Load $ra from stack
	lw $t1, 4($sp)					# Load return value $t1 from stack
	lw $t2, 12($sp)					# Load caller's start value into $t2
	mul $t3, $t1, $t2				# Multiply return value by caller's working value, store in $t3
	sw $t3, 16($sp)					# Store result from $t3 to caller's return value
	addi $sp, $sp, 12				# Move stackpointer back for caller
	jr $ra						# Jump to caller
###	End subroutine	###

ret_one:
	li $t0, 1					# Load one (1) to $t0
	sw $t0, 4($sp)					# Store 1 to caller's return value
	jr $ra						# Jump to caller
	
exit:	
	la $a0, exstr					# loads the contents of exstr to $a0
	li $v0, 4					# loads syscall for print string
	syscall						# prints the exit message
	li $v0, 10					# load syscall code for exiting
	syscall						# terminates execution of program

# ---------------------------------------------------- #
# The data segment
# ---------------------------------------------------- #
.data

title:		.asciiz "This will calculate the largest k such that 2^k divides n!\n"
get_input:	.asciiz "Enter value for n: "
output1:	.asciiz "The value of factorial("
output2:	.asciiz ") is: "
power1:		.asciiz "\nFound divisible number at 2^"
power2:		.asciiz " = "
exstr:		.asciiz "\nGoodbye!"
