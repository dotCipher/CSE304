# -------------------------------------------------------- #
# Protoplasm 1 - MIPS code generator
# -------------------------------------------------------- #
import sys

# $t0-9
assignments = list()

def write_to_asm(name, string):
	with open(name, "w") as asm_file:
		asm_file.write(string)

def create_asm_header():
	header = ".text\n"
	header += "main:\n"
	return header

def create_asm_exit():
	exit = "\tli $v0, 10\n"
	exit += "\tsyscall\n"
	return exit

def get_val_from_ctr(ctr):
	for asgn in assignments:
		if asgn[0] == ctr:
			return asgn[3]
	return -1

#def get_val_from_ctr_and_rem(ctr):
#	for asgn in assignments:
#		if asgn[0] == ctr:
#			tmp = asgn[3]
#			assignments.remove(asgn)
#			return tmp

def get_val_from_var(var):
	for asgn in assignments:
		if asgn[2] == var:
			return asgn[3]
	return -1

def get_reg_num_from_ctr(ctr):
	for asgn in assignments:
		if asgn[1] == ctr:
			return asgn[0]
	return -1


def get_reg_num_from_var(var):
	for asgn in assignments:
		if asgn[2] == var:
			return asgn[0]
	return -1

def optimize_assignments():
	for asgn in assignments:
		if isinstance(asgn[3], int):
			print "Found instance at"
			print asgn
			print ""
			reg_num = asgn[0]
			ctr = asgn[1]
			arg1 = asgn[2]
			arg2 = get_val_from_ctr(asgn[3])
			assignments.remove(asgn)
			assignments.append([reg_num, ctr, arg1, arg2])
			
def convert_tuple_to_asm(t, reg_num):
	#optimize_assignments()
	asm_str = ""
	ctr = t[0]
	op = t[1]
	arg1 = t[2]
	arg2 = t[3]
	new_num = reg_num

	if op == '=':
		reg = "$t%r" % (new_num)
		if arg2 == None:
			if arg1.isdigit():
				assignments.append([reg_num, ctr, "temp", arg1])
				asm_str = "\tli %s, %s\n" % (reg, str(arg1))
				new_num += 1
			else:
				reg2 = "$t%r" % get_reg_num_from_var(arg1)
				#assignments.append([reg_num, ctr, arg1, None]
				assignments.append([reg_num, ctr, arg1, '0'])
				asm_str = "\tadd %s, %s, 0\n" % (reg, reg2)
				#asm_str = "\tli %s, 0\n" % (reg)
				new_num += 1
		else:
			num = get_reg_num_from_ctr(arg2)
			reg2 = "$t%r" % (num)
			assignments.append([reg_num, ctr, arg1, arg2])
			asm_str = "\tadd %s, %s, 0\n" % (reg, reg2)
			new_num += 1
			
	elif op == '+':
		add = "$t%r" % (new_num)
		if (not isinstance(arg1, int)) and isinstance(arg2, int):
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg2))
			if arg1.isdigit():
				# (4, '+', '2', 0)
				asm_str = "\tli $a0, %s\n" % (arg1)
				asm_str += "\tadd %s, %s, $a0\n" % (add, reg2)
				v = int(arg1)
				assignments.append([reg_num, ctr, 'add', v])
			else:
				# (4, '+', 'var', 0)
				reg1 = "$t%r" % (get_reg_num_from_var(arg1))
				asm_str = "\tadd %s, %s, %s\n" % (add, reg1, reg2)
				v = int(arg1)
				assignments.append([reg_num, ctr, 'add', v])
		elif isinstance(arg1, int) and (not isinstance(arg2, int)):
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg1))
			if arg2.isdigit():
				# (4, '+', 0, '2')
				asm_str = "\tli $a0, %s\n" % str(arg2)
				asm_str += "\tadd %s, %s, $a0\n" % (add, reg2)
				v = int(arg2)
				assignments.append([reg_num, ctr, 'add', v])
			else:
				# (4, '+', 0, 'var')
				reg1 = "$t%r" % (get_reg_num_from_var(arg2))
				asm_str = "\tadd %s, %s, %s\n" % (add, reg1, reg2)
				v = int(arg2)
				assignments.append([reg_num, ctr, 'add', v])
		else:
			reg1 = "$t%r" % (get_reg_num_from_ctr(arg1))
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg2))
			asm_str = "\tadd %s, %s, %s\n" % (add, reg1, reg2)
			v = int(new_num)
			assignments.append([reg_num, ctr, 'add', v])
		new_num += 1
		
	elif op == '-':
		sub = "$t%r" % (new_num)
		if (not isinstance(arg1, int)) and isinstance(arg2, int):
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg2))
			if arg1.isdigit():
				# (4, '-', '2', 0)
				asm_str = "\tli $a0, %s\n" % (arg1)
				asm_str += "\tsub %s, %s, $a0\n" % (sub, reg2)
				v = int(arg1)
				assignments.append([reg_num, ctr, 'sun', v])
			else:
				# (4, '-', 'var', 0)
				reg1 = "$t%r" % (get_reg_num_from_var(arg1))
				asm_str = "\tsub %s, %s, %s\n" % (sub, reg1, reg2)
				v = int(arg1)
				assignments.append([reg_num, ctr, 'sub', v])
		elif isinstance(arg1, int) and (not isinstance(arg2, int)):
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg1))
			if arg2.isdigit():
				# (4, '-', 0, '2')
				asm_str = "\tli $a0, %s\n" % str(arg2)
				asm_str += "\tsub %s, %s, $a0\n" % (sub, reg2)
				v = int(arg2)
				assignments.append([reg_num, ctr, 'sub', v])
			else:
				# (4, '-', 0, 'var')
				reg1 = "$t%r" % (get_reg_num_from_var(arg2))
				asm_str = "\tsub %s, %s, %s\n" % (sub, reg2, reg1)
				v = int(arg2)
				assignments.append([reg_num, ctr, 'sub', v])
		else:
			reg1 = "$t%r" % (get_reg_num_from_ctr(arg1))
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg2))
			asm_str = "\tsub %s, %s, %s\n" % (sub, reg1, reg2)
			v = int(new_num)
			assignments.append([reg_num, ctr, 'sub', v])
		new_num += 1

	elif op == '*':
		if (not isinstance(arg1, int)) and isinstance(arg2, int):
			mflo = "$t%r" % (new_num)
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg2))
			if arg1.isdigit():
				asm_str = "\tli $a0, %s\n" % (arg1)
				asm_str += "\tmult %s, $a0\n" % (reg2)
				asm_str += "\tmflo %s\n" % (mflo)
				v = int(arg1) * int(get_val_from_ctr(arg2))
				assignments.append([reg_num, ctr, 'mul', v])
			else:
				reg1 = "$t%r" % (get_reg_num_from_var(arg1))
				asm_str = "\tmult %s, %s\n" % (reg1, reg2)
				asm_str += "\tmflo %s\n" % (mflo)
				v = get_val_from_var(arg1) * get_val_from_ctr(arg2)
				assignments.append([reg_num, ctr, 'mul', v])
		elif isinstance(arg1, int) and (not isinstance(arg2, int)):
			num = get_reg_num_from_ctr(arg1)
			mflo = "$t%r" % (new_num)
			reg1 = "$t%r" % (num)
			# Load immediate then mult
			# else get value of var assignment
			if arg2.isdigit():
				print num
				print arg2
				asm_str = "\tli $a0, %s\n" % (arg2)
				asm_str += "\tmult %s, $a0\n" % (reg1)
				asm_str += "\tmflo %s\n" % (mflo)
				v = int(get_val_from_ctr(arg1)) * int(arg2)
				assignments.append([reg_num, ctr, 'mul', v])
			else:
				reg2 = get_val_from_var(arg2)
				asm_str = "\tli $a0, %s\n" % (reg2)
				asm_str += "\tmult %s, %s\n" % (reg1, reg2)
				asm_str += "\tmflo %s\n" % (mflo)
				v = int(get_val_from_ctr(arg1)) * int(reg2)
				assignments.append([reg_num, ctr, 'mul', reg2])
		else:
			reg1 = "$t%r" % (get_reg_num_from_ctr(arg1))
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg2))
			asm_str = "\tmult %s, %s\n" % (reg1, reg2)
			asm_str += "\tmflo %s\n" % (mflo)
			v = int(new_num)
			assignments.append([reg_num, ctr, 'mul', v])
		new_num += 1
			
	elif op == '/':
		div = "$t%r" % (new_num)
		if (not isinstance(arg1, int)) and isinstance(arg2, int):
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg2))
			if arg1.isdigit():
				# (4, '/', '2', 0)
				asm_str = "\tli $a0, %s\n" % (arg1)
				asm_str += "\tdiv $a0, %s\n" % (reg2)
				asm_str += "\tmflo %s\n" % (div)
				v = int(arg1)
				assignments.append([reg_num, ctr, 'div', v])
			else:
				# (4, '/', 'var', 0)
				reg1 = "$t%r" % (get_reg_num_from_var(arg1))
				asm_str = "\tdiv %s, %s\n" % (reg1, reg2)
				asm_str += "\tmflo %s\n" % (div)
				v = int(arg1)
				assignments.append([reg_num, ctr, 'div', v])
		elif isinstance(arg1, int) and (not isinstance(arg2, int)):
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg1))
			if arg2.isdigit():
				# (4, '/', 0, '2')
				asm_str = "\tli $a0, %s\n" % str(arg2)
				asm_str += "\tdiv %s, $a0\n" % (reg2)
				asm_str += "\tmflo %s\n" % (div)
				v = int(arg2)
				assignments.append([reg_num, ctr, 'div', v])
			else:
				# (4, '/', 0, 'var')
				reg1 = "$t%r" % (get_reg_num_from_var(arg2))
				asm_str = "\tdiv %s, %s\n" % (reg2, reg1)
				asm_str += "\tmflo %s\n" % (div)
				v = int(arg2)
				assignments.append([reg_num, ctr, 'div', v])
		else:
			reg1 = "$t%r" % (get_reg_num_from_ctr(arg1))
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg2))
			asm_str = "\tdiv %s, %s\n" % (reg1, reg2)
			asm_str += "\tmflo %s\n" % (div)
			v = int(new_num)
			assignments.append([reg_num, ctr, 'div', v])
		new_num += 1
		
	elif op == '%':
		div = "$t%r" % (new_num)
		if (not isinstance(arg1, int)) and isinstance(arg2, int):
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg2))
			if arg1.isdigit():
				# (4, '/', '2', 0)
				asm_str = "\tli $a0, %s\n" % (arg1)
				asm_str += "\tdiv $a0, %s\n" % (reg2)
				asm_str += "\tmfhi %s\n" % (div)
				v = int(arg1)
				assignments.append([reg_num, ctr, 'mod', v])
			else:
				# (4, '/', 'var', 0)
				reg1 = "$t%r" % (get_reg_num_from_var(arg1))
				asm_str = "\tdiv %s, %s\n" % (reg1, reg2)
				asm_str += "\tmfhi %s\n" % (div)
				v = int(arg1)
				assignments.append([reg_num, ctr, 'mod', v])
		elif isinstance(arg1, int) and (not isinstance(arg2, int)):
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg1))
			if arg2.isdigit():
				# (4, '/', 0, '2')
				asm_str = "\tli $a0, %s\n" % str(arg2)
				asm_str += "\tdiv %s, $a0\n" % (reg2)
				asm_str += "\tmfhi %s\n" % (div)
				v = int(arg2)
				assignments.append([reg_num, ctr, 'mod', v])
			else:
				# (4, '/', 0, 'var')
				reg1 = "$t%r" % (get_reg_num_from_var(arg2))
				asm_str = "\tdiv %s, %s\n" % (reg2, reg1)
				asm_str += "\tmfhi %s\n" % (div)
				v = int(arg2)
				assignments.append([reg_num, ctr, 'mod', v])
		else:
			reg1 = "$t%r" % (get_reg_num_from_ctr(arg1))
			reg2 = "$t%r" % (get_reg_num_from_ctr(arg2))
			asm_str = "\tdiv %s, %s\n" % (reg1, reg2)
			asm_str += "\tmfhi %s\n" % (div)
			v = int(new_num)
			assignments.append([reg_num, ctr, 'mod', v])
		new_num += 1
		
	elif op == 'minus':
		if arg1 == None:
			if isinstance(arg2, int):
				num = get_reg_num_from_ctr(arg2)
				print num
				if num != -1:
					reg = "$t%r" % (num)
					asm_str = "\tli $a0, -1\n"
					asm_str += "\tmult %s, $a0\n" % (reg)
					asm_str += "\tmflo %s\n" % (reg)
					assignments.append([num, ctr, 'minus', arg2])
					new_num += 1
			else:
				reg = "$t%r" % (new_num)
				asm_str = "\tli $a0, -1\n"
				asm_str += "\tli %s, %s\n" % (reg, arg2)
				asm_str += "\tmult %s, $a0\n" % (reg)
				asm_str += "\tmflo %s\n" % (reg)
				assignments.append([reg_num, ctr, 'minus', arg2])
				new_num += 1
				
	elif op == 'print':
		if isinstance(arg2, int):
			num = get_reg_num_from_ctr(arg2)
			if num != -1:
				reg = "$t%r" % (num)
				asm_str = "\tadd $a0, %s, 0\n" % (reg)
				asm_str += "\tli $v0, 1\n"
				asm_str += "\tsyscall\n"
			#else:
			#	num = follow_assigns_to_print(arg2)
		else:
			asm_str = "\tli $a0, %s\n" % (arg2)
			asm_str += "\tli $v0, 1\n"
			asm_str += "\tsyscall\n"
			
	elif op == 'input':
		reg = "$t%r" % (new_num)
		if arg2 == None:
			assignments.append([reg_num, ctr, 'temp', 'input'])
			asm_str = "\tli $v0, 5\n"
			asm_str += "\tsyscall\n"
			asm_str += "\tmove %s, $v0\n" % (reg)
			new_num += 1
	else:
		pass
	return (new_num, asm_str)

def make_asm_exec(fname, tlist):
	reg_num = 0
	string = create_asm_header()
	exit = create_asm_exit()
	for tup in tlist:
		ret = convert_tuple_to_asm(tup, reg_num)
		reg_num = ret[0]
		string += ret[1]
	string += exit
	#print assignments
	#print ""
	#print string
	if reg_num >= 10:
		print "Error: Register spilling detected. Aborting compile"
	else:
		write_to_asm(fname, string)

