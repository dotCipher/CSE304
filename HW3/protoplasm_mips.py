# -------------------------------------------------------- #
# Protoplasm 2 - MIPS code generator
# -------------------------------------------------------- #
import sys
import re

######################################################
# Globals
######################################################
# $t0-9 = Main assignment registers
# $s0-7 = Temp assignment registers
# $a0 = Function argument / Loading immediate
# $at = Assembler temporary for bit shift logical op
liveness = list()
reg_table = list()
temp_reg_table = list()
mips_code = list()

# Label sets
label_mapping = list()
lset_eq = ['EQ_EQ_0','EQ_NE_0','EQ_RET_0']
lset_ne = ['NE_NE_0','NE_EQ_0','NE_RET_0']
lset_gt = ['GT_GT_0','GT_LE_0','GT_RET_0']
lset_lt = ['LT_LT_0','LT_GE_0','LT_RET_0']
lset_ge = ['GE_GE_0','GE_LT_0','GE_RET_0']
lset_le = ['LE_LE_0','LE_GT_0','LE_RET_0']
lset_not = ['NOT_TRUE_0', 'NOT_FALSE_0', 'NOT_RET_0']
lset_if = ['IF_TRUE_0', 'IF_FALSE_0','IF_RET_0']
lset_while = ['WHILE_TRUE_0', 'WHILE_FALSE_0','WHILE_RET_0']
lset_goto = ['GOTO_0']

######################################################
# Main Function
######################################################
def make_asm_exec(fname, tlist):
	for tup in tlist:
		asm_pair = convert_tuple_to_asm(tup)
		mips_code.append(asm_pair)
	string = convert_mips_code_to_str()
	write_to_asm(fname, string)

######################################################
# Secondary Functions
######################################################
def write_to_asm(name, string):
	with open(name, "w") as asm_file:
		asm_file.write(string)

def convert_mips_code_to_str():
	full_asm = create_asm_header()
	for tup in mips_code:
		full_asm += tup[1]
	return full_asm

def create_asm_header():
	header = ".text\n"
	header += "main:\n"
	return header

def create_asm_exit():
	exit = "\tli $v0, 10\n"
	exit += "\tsyscall\n"
	return exit

def add_exit(tlist):
	last_tuple = tlist[-1]
	last_sn = last_tuple[0]
	exit_tuple = (last_sn+1, 'exit', None, None)
	tlist.append(exit_tuple)
	
######################################################
# Utility Functions
######################################################
# Returns boolean if tuple represents binary expression
def is_tuple_binop(t):
	op = t[1]
	if (op == '+') or (op == '*') or (op == '/'):
		return True
	elif (op == '%') or (op == '&&') or (op == '||'):
		return True
	elif (op == '==') or (op == '!='):
		return True
	elif (op == '<') or (op == '>') or (op == '>=') or (op == '<='):
		return True
	else:
		return False

def is_tuple_reserved(t):
	op = t[1]
	if (op == 'print') or (op == 'input'):
		return True
	elif (op == 'while') or (op == 'if') or (op == 'block'):
		return True
	else:
		return False

def remove_dups(l):
	seen = set()
	seen_add = seen.add
	return [ x for x in l if x not in seen and not seen_add(x)]

######################################################
# Liveness Analysis
######################################################
# After tuple list of intermediate code is made,
#  get_liveness is called to creat liveness tuple list
# Liveness is assigned based on statement number
# (SN, DEF, USE)
def get_liveness(tlist):
	for t in tlist:
		snum = t[0]
		op = t[1]
		arg1 = t[2]
		arg2 = t[3]
		if (op == '='):
			ulist = list()
			update_uselist_from_sn(tlist, ulist, snum)
			ulist = remove_dups(ulist)
			liveness.append((snum, arg1, ulist))
		elif (is_tuple_binop(t)) or (op == '!') or (op == '-') or (op == 'print'):
			ulist = list()
			update_uselist_from_sn(tlist, ulist, snum)
			ulist = remove_dups(ulist)
			liveness.append((snum, None, ulist))
		elif (op == 'input'):
			liveness.append((snum, arg1, []))
		elif (op == 'while') or (op == 'if'):
			ulist = list()
			update_uselist_from_sn(tlist, ulist, snum)
			ulist = remove_dups(ulist)
			liveness.append((snum, None, ulist))
		elif (op == 'goto') or (op == 'exit'):
			liveness.append((snum, None, []))
		else:
			print "Error with (%s, %s, %s, %s)" % (snum, op, arg1, arg2)			

# Mutates a list of all variables used at statement
#  using recursion
def update_uselist_from_sn(tlist, use_list, sn):
	for t in tlist:
		snum = t[0]
		if snum == sn:
			op = t[1]
			arg1 = t[2]
			arg2 = t[3]
			if op == '=':
				if isinstance(arg2, int):
					update_uselist_from_sn(tlist, use_list, arg2)
				else:
					if not(arg2.isdigit()):
						use_list.append(arg2)
			elif op == '-':
				if (not(arg1 is None)) and (arg2 is None):
					if isinstance(arg1, int):
						update_uselist_from_sn(tlist, use_list, arg1)
					else:
						if not(arg1.isdigit()):
							use_list.append(arg1)
				elif (arg1 is None) and (not(arg2 is None)):
					if isinstance(arg2, int):
						update_uselist_from_sn(tlist, use_list, arg2)
					else:
						if not(arg2.isdigit()):
							use_list.append(arg2)
				elif (not(arg1 is None)) and (not(arg2 is None)):
					 if isinstance(arg1, int):
						if isinstance(arg2, int):
							update_uselist_from_sn(tlist, use_list, arg1)
							update_uselist_from_sn(tlist, use_list, arg2)
						else:
							if not(arg2.isdigit()):
								use_list.append(arg2)
								update_uselist_from_sn(tlist, use_list, arg1)
							else:
								update_uselist_from_sn(tlist, use_list, arg1)
					 else:
					 	if isinstance(arg2, int):
					 		if not(arg1.isdigit()):
					 			use_list.append(arg1)
					 			update_uselist_from_sn(tlist, use_list, arg2)
					 		else:
					 			update_uselist_from_sn(tlist, use_list, arg2)
					 	else:
					 		if not(arg1.isdigit()):
								if not(arg2.isdigit()):
									use_list.append(arg1)
									use_list.append(arg2)
								else:
									use_list.append(arg1)
					 		else:
					 			if not(arg2.isdigit()):
					 				use_list.append(arg2)
				else:
					print "Syntax error for \'-\' operator"
			elif is_tuple_binop(t):
				if isinstance(arg1, int):
					if isinstance(arg2, int):
						update_uselist_from_sn(tlist, use_list, arg1)
						update_uselist_from_sn(tlist, use_list, arg2)
					else:
						if not(arg2.isdigit()):
							use_list.append(arg2)
							update_uselist_from_sn(tlist, use_list, arg1)
						else:
							update_uselist_from_sn(tlist, use_list, arg1)
				else:
					if isinstance(arg2, int):
						if not(arg1.isdigit()):
							use_list.append(arg1)
							update_uselist_from_sn(tlist, use_list, arg2)
						else:
							update_uselist_from_sn(tlist, use_list, arg2)
					else:
						if not(arg1.isdigit()):
							if not(arg2.isdigit()):
								use_list.append(arg1)
								use_list.append(arg2)
							else:
								use_list.append(arg1)
						else:
							if not(arg2.isdigit()):
								use_list.append(arg2)
			elif (op == '!'):
				if (arg1 is None) and (not(arg2 is None)):
					if isinstance(arg2, int):
						update_uselist_from_sn(tlist, use_list, arg2)
					else:
						if not(arg2.isdigit()):
							use_list.append(arg2)
				elif (arg2 is None) and (not(arg1 is None)):
					if isinstance(arg1, int):
						update_uselist_from_sn(tlist, use_list, arg1)
					else:
						if not(arg1.isdigit()):
							use_list.append(arg1)
				else:
					print "Syntax error with \'!\' operator"
			elif (op == 'print'):
				if (arg1 is None) and (not(arg2 is None)):
					if isinstance(arg2, int):
						update_uselist_from_sn(tlist, use_list, arg2)
					else:
						if not(arg2.isdigit()):
							use_list.append(arg2)
				elif (not(arg1 is None)) and (arg2 is None):
					if isinstance(arg1, int):
						update_uselist_from_sn(tlist, use_list, arg1)
					else:
						if not(arg1.isdigit()):
							use_list.append(arg1)
				else:
					print "Syntax error with \'print\' operator"
			elif (op == 'while') or (op == 'if'):
				if isinstance(arg1, int):
					update_uselist_from_sn(tlist, use_list, arg1)
				else:
					if not(arg1.isdigit()):
						use_list.append(arg1)

######################################################
# Register Allocation
######################################################
# Assumption that get_liveness is called first	
def get_register_from_var(isdef, linenum, var):
	for record in register_table:
		if record[0] == var:
			reg_list = record[1]
			for reg_assign in reg_list:
				if isdef:
					if reg_assign[1] == linenum:
						return reg_assign[0]
				else:
					r_min = reg_assign[1]+1
					r_max = reg_assign[2]
					if (linenum >= r_min) and (linenum <= r_max):
						return reg_assign[0]

def add_temp_reg(sn):
	if temp_reg_table:
		temp_reg_table.append((sn, 's0'))
	else:
		num = re.search('\d', temp_reg_table[-1][1])
		next_num = str(int(num.group(0))+1)
		if next_num > 7:
			print "Error assigning temporary variable on line %s" % (sn)
		else:
			new_reg = 's' + next_num
			temp_reg_table.append((sn, new_reg))
			return new_reg

def get_temp_reg(sn):
	reg = None
	for record in temp_reg_table:
		if record[0] == sn:
			reg = record[1]
			del temp_reg_table[-1]
			break
	return reg
	
######################################################
# MIPS Code Generation
######################################################
def get_label_set_eq():
	lset = lset_eq
	num = re.search('\d', lset_eq[0])
	next_num = str(int(num.group(0))+1)
	s1 = 'EQ_EQ_' + next_num
	s2 = 'EQ_NE_' + next_num
	s3 = 'EQ_RET_' + next_num
	lset_eq = [s1,s2,s3]
	return lset

def get_label_set_ne():
	lset = lset_ne
	num = re.search('\d', lset_ne[0])
	next_num = str(int(num.group(0))+1)
	s1 = 'NE_NE_' + next_num
	s2 = 'NE_EQ_' + next_num
	s3 = 'NE_RET_' + next_num
	lset_ne = [s1,s2,s3]
	return lset

def get_label_set_gt():
	lset = lset_gt
	num = re.search('\d', lset_gt[0])
	next_num = str(int(num.group(0))+1)
	s1 = 'GT_GT_' + next_num
	s2 = 'GT_LE_' + next_num
	s3 = 'GT_RET_' + next_num
	lset_gt = [s1,s2,s3]
	return lset

def get_label_set_lt():
	lset = lset_lt
	num = re.search('\d', lset_lt[0])
	next_num = str(int(num.group(0))+1)
	s1 = 'LT_LT_' + next_num
	s2 = 'LT_GE_' + next_num
	s3 = 'LT_RET_' + next_num
	lset_lt = [s1,s2,s3]
	return lset

def get_label_set_ge():
	lset = lset_ge
	num = re.search('\d', lset_ge[0])
	next_num = str(int(num.group(0))+1)
	s1 = 'GE_GE_' + next_num
	s2 = 'GE_LT_' + next_num
	s3 = 'GE_RET_' + next_num
	lset_ge = [s1,s2,s3]
	return lset

def get_label_set_le():
	lset = lset_le
	num = re.search('\d', lset_le[0])
	next_num = str(int(num.group(0))+1)
	s1 = 'LE_LE_' + next_num
	s2 = 'LE_GT_' + next_num
	s3 = 'LE_RET_' + next_num
	lset_le = [s1,s2,s3]
	return lset

def get_label_set_not():
	lset = lset_not
	num = re.search('\d', lset_not[0])
	next_num = str(int(num.group(0))+1)
	s1 = 'NOT_TRUE_' + next_num
	s2 = 'NOT_FALSE_' + next_num
	s3 = 'NOT_RET_' + next_num
	lset_not = [s1,s2,s3]
	return lset

def get_label_set_if():
	lset = lset_if
	num = re.search('\d', lset_if[0])
	next_num = str(int(num.group(0))+1)
	s1 = 'IF_TRUE_' + next_num
	s2 = 'IF_FALSE_' + next_num
	s3 = 'IF_RET_' + next_num
	lset_if = [s1,s2,s3]
	return lset

def get_label_set_while():
	lset = lset_while
	num = re.search('\d', lset_while[0])
	next_num = str(int(num.group(0))+1)
	s1 = 'WHILE_TRUE_' + next_num
	s2 = 'WHILE_FALSE_' + next_num
	s3 = 'WHILE_RET_' + next_num
	lset_while = [s1,s2,s3]
	return lset

def get_label_set_goto():
	lset = lset_goto
	num = re.search('\d', lset_goto[0])
	next_num = str(int(num.group(0))+1)
	s1 = 'GOTO_' + next_num
	lset_goto = [s1]
	return lset

def label_exists(sn):
	if label_mapping:
		for mapping in label_mapping:
			if mapping[0] == sn:
				return True
	else:
		return False

def map_label(sn, asm_str):
	for mapping in label_mapping:
		if mapping[0] == sn:
			# Parse out string
			after = asm_str
			before = mapping[1]
			asm_str = before + after

def prepend_label_to_block(sn, code):
	for block in mips_code:
		if block[0] == sn:
			after = block[1]
			new = code + after
			block[1] = new

def convert_tuple_to_asm(tup):
	asm_str = ""
	sn = t[0]
	op = t[1]
	arg1 = t[2]
	arg2 = t[3]

	if op == '=':
		if isinstance(arg2, int):
			# (#, '=', 'x', 5)
			treg2 = get_temp_reg(arg2)
			reg1 = get_register_from_var(1, sn, arg1)
			if treg1 is None:
				print "[%s] Error: Cannot find temp reg for %s" % (sn, arg2)
			else:
				asm_str = "\tadd %s, %s, 0\n" % (reg1, treg2)
		else:
			if arg2.isdigit():
				# (#, '=', 'x', '9')
				reg1 = get_register_from_var(1, sn, arg1)
				asm_str = "\tli %s, %s\n" % (reg1, str(arg2))
			else:
				# (#, '=', 'x', 'y')
				reg1 = get_register_from_var(1, sn, arg1)
				reg2 = get_register_from_var(0, sn, arg2)
				asm_str = "\tadd %s, %s, 0\n" % (reg1, reg2)
				
	elif op == '+':
		new_reg = add_temp_reg(sn)
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '+', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tadd %s, %s, %s\n" % (new_reg, treg1, treg2)
			else:
				if arg2.isdigit():
					# (#, '+', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\taddi %s, %s, %s\n" % (new_reg, treg1, str(arg2))
				else:
					# (#, '+', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tadd %s, %s, %s\n" % (new_reg, treg1, reg2)
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '+', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\taddi %s, %s, %s\n" % (new_reg, str(arg1), treg2)
				else:
					# (#, '+', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tadd %s, %s, %s\n" % (new_reg, reg1, treg2)
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '+', '9', '5')
						asm_str = "\tli $a0, %s\n" % (str(arg1))
						asm_str += "\taddi %s, %s, %s\n" % (new_reg, new_reg, str(arg2))
					else:
						# (#, '+', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tli $a0, %s\n" % (str(arg1))
						asm_str += "\tadd %s, %s, %s\n" % (new_reg, new_reg, reg2)
				else:
					if arg2.isdigit():
						# (#, '+', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tli $a0, %s\n" % (str(arg2))
						asm_str += "\tadd %s, %s, %s\n" % (new_reg, reg1, new_reg)
					else:
						# (#, '+', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str += "\tadd %s, %s, %s\n" % (new_reg, reg1, reg2)
						
	elif op == "-":
		new_reg = add_temp_reg(sn)
		if (arg1 is None) and (not(arg2 is None)):
			if isinstance(arg2, int):
				# (#, '-', None, 6)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tli $a0, -1\n"
				asm_str += "\tmult %s, $a0\n" % (treg2)
			else:
				if arg2.isdigit():
					# (#, '-', None, '5')
					asm_str = "\tli $a0, -1\n"
					asm_str += "\tli %s, %s\n" % (new_reg, arg2)
					asm_str += "\tmult %s, $a0\n" % (new_reg)
				else:
					# (#, '-', None, 'y')
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tli $a0, -1\n"
					asm_str += "\tmult %s, $a0\n" % (reg2)
			asm_str += "\tmflo %s\n" % (new_reg)
		elif (not(arg1 is None)) and (arg2 is None):
			if isinstance(arg1, int):
				# (#, '-', 2, None)
				treg1 = get_temp_reg(arg1)
				asm_str = "\tli $a0, -1\n"
				asm_str += "\tmult %s, $a0\n" % (treg1)
			else:
				if arg1.isdigit():
					# (#, '-', '9', None)
					asm_str = "\tli $a0, -1\n"
					asm_str += "\tli %s, %s\n" % (new_reg, arg1)
					asm_str += "\tmult %s, $a0\n" % (new_reg)
				else:
					# (#, '-', 'x', None)
					reg1 = get_register_from_var(0, sn, arg1)
					asm_str = "\tli $a0, -1\n"
					asm_str += "\tmult %s, $a0\n" % (reg1)
			asm_str += "\tmflo %s\n" % (new_reg)
		elif (not(arg1 is None)) and (not(arg2 is None)):
			if isinstance(arg1, int):
				if isinstance(arg2, int):
					# (#, '-', 2, 6)
					treg1 = get_temp_reg(arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tsub %s, %s, %s\n" % (new_reg, treg1, treg2)
				else:
					if arg2.isdigit():
						# (#, '-', 2, '5')
						treg1 = get_temp_reg(arg1)
						asm_str = "\tli $a0, %s\n" % (arg2)
						asm_str += "\tsub %s, %s, $a0\n" % (new_reg, treg1)
					else:
						# (#, '-', 2, 'y')
						treg1 = get_temp_reg(arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tsub %s, %s, %s\n" % (new_reg, treg1, reg2)
			else:
				if isinstance(arg2, int):
					if arg1.isdigit():
						# (#, '-', '9', 6)
						treg2 = get_temp_reg(arg2)
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tsub %s, $a0, %s\n" % (new_reg, treg2)
					else:
						# (#, '-', 'x', 6)
						reg1 = get_register_from_var(0, sn, arg1)
						treg2 = get_temp_reg(arg2)
						asm_str = "\tsub %s, %s, %s\n" % (new_reg, reg1, treg2)
				else:
					if arg1.isdigit():
						if arg2.isdigit():
							# (#, '-', '9', '5')
							asm_str = "\tli %s, %s\n" % (new_reg, arg1)
							asm_str += "\tli $a0, %s\n" % (arg2)
							asm_str += "\tsub %s, %s, $a0\n" % (new_reg, new_reg)
						else:
							# (#, '-', '9', 'y')
							reg2 = get_register_from_var(0, sn, arg2)
							asm_str = "\tli $a0, %s\n" % (arg1)
							asm_str += "\tsub %s, $a0, %s\n" % (new_reg, reg2)
					else:
						if arg2.isdigit():
							# (#, '-', 'x', '5')
							reg1 = get_register_from_var(0, sn, arg1)
							asm_str = "\tli $a0, %s\n" % (arg2)
							asm_str += "\tsub %s, %s, $a0\n" % (new_reg, reg1)
						else:
							# (#, '-', 'x', 'y')
							reg1 = get_register_from_var(0, sn, arg1)
							reg2 = get_register_from_var(0, sn, arg2)
							asm_str += "\tsub %s, %s, %s\n" % (new_reg, reg1, reg2)
							
	elif op == "/":
		new_reg = add_temp_reg(sn)
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '/', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tdiv %s, %s\n" % (treg1, treg2)
			else:
				if arg2.isdigit():
					# (#, '/', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tdiv %s, $a0\n" % (treg1)
				else:
					# (#, '/', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tdiv %s, %s\n" % (treg1, reg2)
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '/', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tdiv $a0, %s\n" % (treg2)
				else:
					# (#, '/', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tdiv %s, %s\n" % (reg1, treg2)
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '/', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tli %s, %s\n" % (new_reg, arg2)
						asm_str += "\tdiv $a0, %s\n" % (new_reg)
					else:
						# (#, '/', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tdiv $a0, %s\n" % (reg2)
				else:
					if arg2.isdigit():
						# (#, '/', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tli $a0, %s\n" % (arg2)
						asm_str += "\tdiv %s, $a0\n" % (reg1)
					else:
						# (#, '/', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str += "\tdiv %s, %s\n" % (reg1, reg2)
		asm_str += "\tmflo %s\n" % (new_reg)
						
	elif op == "%":
		new_reg = add_temp_reg(sn)
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '%', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tdiv %s, %s\n" % (treg1, treg2)
			else:
				if arg2.isdigit():
					# (#, '%', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tdiv %s, $a0\n" % (treg1)
				else:
					# (#, '%', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tdiv %s, %s\n" % (treg1, reg2)
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '%', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tdiv $a0, %s\n" % (treg2)
				else:
					# (#, '%', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tdiv %s, %s\n" % (reg1, treg2)
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '%', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tli %s, %s\n" % (new_reg, arg2)
						asm_str += "\tdiv $a0, %s\n" % (new_reg)
					else:
						# (#, '%', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tdiv $a0, %s\n" % (reg2)
				else:
					if arg2.isdigit():
						# (#, '%', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tli $a0, %s\n" % (arg2)
						asm_str += "\tdiv %s, $a0\n" % (reg1)
					else:
						# (#, '%', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tdiv %s, %s\n" % (reg1, reg2)
		asm_str += "\tmfhi %s\n" % (new_reg)
					
	elif op == "*":
		new_reg = add_temp_reg(sn)
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '*', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tmul %s, %s\n" % (treg1, treg2)
			else:
				if arg2.isdigit():
					# (#, '*', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tmul %s, $a0\n" % (treg1)
				else:
					# (#, '*', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tmul %s, %s\n" % (treg1, reg2)
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '*', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tmul $a0, %s\n" % (treg2)
				else:
					# (#, '*', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tmul %s, %s\n" % (reg1, treg2)
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '*', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tli %s, %s\n" % (new_reg, arg2)
						asm_str += "\tmul $a0, %s\n" % (new_reg)
					else:
						# (#, '*', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tmul $a0, %s\n" % (reg2)
				else:
					if arg2.isdigit():
						# (#, '*', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tli $a0, %s\n" % (arg2)
						asm_str += "\tmul %s, $a0\n" % (reg1)
					else:
						# (#, '*', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tmul %s, %s\n" % (reg1, reg2)
		asm_str += "\tmflo %s\n" % (new_reg)
					
	elif op == "&&":
		new_reg = add_temp_reg(sn)
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '&&', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tand %s, %s, %s\n" % (new_reg, treg1, treg2)
			else:
				if arg2.isdigit():
					# (#, '&&', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tandi %s, %s, %s\n" % (new_reg, treg1, arg2)
				else:
					# (#, '&&', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tand %s, %s, %s\n" % (new_reg, treg1, reg2)
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '&&', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tandi %s, %s, %s\n" % (new_reg, treg1, arg2)
				else:
					# (#, '&&', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tand %s, %s, %s\n" % (new_reg, reg1, treg2)
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '&&', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tandi %s, $a0, %s\n" % (new_reg, arg2)
					else:
						# (#, '&&', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tandi %s, %s, %s\n" % (new_reg, reg2, arg1)
				else:
					if arg2.isdigit():
						# (#, '&&', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tandi %s, %s, %s\n" % (new_reg, reg1, arg2)
					else:
						# (#, '&&', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tand %s, %s, %s\n" % (new_reg, reg1, reg2)
						
	elif op == "||":
		new_reg = add_temp_reg(sn)
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '||', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tor %s, %s, %s\n" % (new_reg, treg1, treg2)
			else:
				if arg2.isdigit():
					# (#, '||', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tori %s, %s, %s\n" % (new_reg, treg1, arg2)
				else:
					# (#, '||', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tor %s, %s, %s\n" % (new_reg, treg1, reg2)
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '||', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tori %s, %s, %s\n" % (new_reg, treg2, arg1)
				else:
					# (#, '||', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tor %s, %s, %s\n" % (new_reg, reg1, treg2)
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '||', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tori %s, $a0, %s\n" % (new_reg, arg2)
					else:
						# (#, '||', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tori %s, %s, %s\n" % (new_reg, reg2, arg1)
				else:
					if arg2.isdigit():
						# (#, '||', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tori %s, %s, %s\n" % (new_reg, reg1, arg2)
					else:
						# (#, '||', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tor %s, %s, %s\n" % (new_reg, reg1, reg2)
						
	elif op == "==":
		new_reg = add_temp_reg(sn)
		label_set = get_label_set_eq()
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '==', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tbeq %s, %s, %s\n" (treg1, treg2, label_set[0])
			else:
				if arg2.isdigit():
					# (#, '==', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tbeq %s, $a0, %s\n" (treg1, label_set[0])
				else:
					# (#, '==', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tbeq %s, %s, %s\n" (treg1, reg2, label_set[0])
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '==', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tbeq $a0, %s, %s\n" (treg2, label_set[0])
				else:
					# (#, '==', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tbeq %s, %s, %s\n" (reg1, treg2, label_set[0])
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '==', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tli %s, %s\n" % (new_reg, arg2)
						asm_str += "\tbeq $a0, %s, %s\n" (new_reg, label_set[0])
					else:
						# (#, '==', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tbeq $a0, %s, %s\n" (reg2, label_set[0])
				else:
					if arg2.isdigit():
						# (#, '==', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tli $a0, %s\n" % (arg2)
						asm_str += "\tbeq %s, $a0, %s\n" (reg1, label_set[0])
					else:
						# (#, '==', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tbeq %s, %s, %s\n" (reg1, reg2, label_set[0])
		asm_str += "\tj %s\n" (label_set[1])
		asm_str += "%s:\n" % (label_set[0])
		asm_str += "\tli %s, 1\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[1])
		asm_str += "\tli %s, 0\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[2])
		
	elif op == "!=":
		new_reg = add_temp_reg(sn)
		label_set = get_label_set_ne()
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '!=', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tbne %s, %s, %s\n" (treg1, treg2, label_set[0])
			else:
				if arg2.isdigit():
					# (#, '!=', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tbne %s, $a0, %s\n" (treg1, label_set[0])
				else:
					# (#, '!=', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tbne %s, %s, %s\n" (treg1, reg2, label_set[0])
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '!=', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tbne $a0, %s, %s\n" (treg2, label_set[0])
				else:
					# (#, '!=', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tbne %s, %s, %s\n" (reg1, treg2, label_set[0])
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '!=', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tli %s, %s\n" % (new_reg, arg2)
						asm_str += "\tbne $a0, %s, %s\n" (new_reg, label_set[0])
					else:
						# (#, '!=', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tbne $a0, %s, %s\n" (reg2, label_set[0])
				else:
					if arg2.isdigit():
						# (#, '!=', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tli $a0, %s\n" % (arg2)
						asm_str += "\tbne %s, $a0, %s\n" (reg2, label_set[0])
					else:
						# (#, '!=', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tbne %s, %s, %s\n" (reg1, reg2, label_set[0])
		asm_str += "\tj %s\n" (label_set[1])
		asm_str += "%s:\n" % (label_set[0])
		asm_str += "\tli %s, 1\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[1])
		asm_str += "\tli %s, 0\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[2])
			
	elif op == "<":
		new_reg = add_temp_reg(sn)
		label_set = get_label_set_lt()
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '<', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tslt $at, %s, %s\n" % (treg1, treg2)
			else:
				if arg2.isdigit():
					# (#, '<', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tslt $at, %s, $a0\n" % (treg1)
				else:
					# (#, '<', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tslt $at, %s, %s\n" % (treg1, reg2)
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '<', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tslt $at, $a0, %s\n" % (treg2)
				else:
					# (#, '<', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tslt $at, %s, %s\n" % (reg1, treg2)
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '<', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tli %s, %s\n" % (new_reg, arg2)
						asm_str += "\tslt $at, $a0, %s\n" % (new_reg)
					else:
						# (#, '<', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tslt $at, $a0, %s\n" % (reg2)
				else:
					if arg2.isdigit():
						# (#, '<', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tli $a0, %s\n" % (arg2)
						asm_str += "\tslt $at, %s, $a0\n" % (reg1)

					else:
						# (#, '<', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tslt $at, %s, %s\n" % (reg1, reg2)
		asm_str += "\tbne $at, $zero, %s\n" % (label_set[0])
		asm_str += "\tj %s\n" (label_set[1])
		asm_str += "%s:\n" % (label_set[0])
		asm_str += "\tli %s, 1\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[1])
		asm_str += "\tli %s, 0\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[2])
		
	elif op == ">":
		new_reg = add_temp_reg(sn)
		label_set = get_label_set_gt()
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '>', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tslt $at, %s, %s\n" % (treg2, treg1)
			else:
				if arg2.isdigit():
					# (#, '>', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tslt $at, $a0, %s\n" % (treg1)
				else:
					# (#, '>', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tslt $at, %s, %s\n" % (treg2, reg1)
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '>', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tslt $at, %s, $a0\n" % (treg2)
				else:
					# (#, '>', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tslt $at, %s, %s\n" % (treg2, reg1)
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '>', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tli %s, %s\n" % (new_reg, arg2)
						asm_str += "\tslt $at, %s, $a0\n" % (new_reg)
					else:
						# (#, '>', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tslt $at, %s, $a0\n" % (reg2)
				else:
					if arg2.isdigit():
						# (#, '>', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tli $a0, %s\n" % (arg2)
						asm_str += "\tslt $at, $a0, %s\n" % (reg1)
					else:
						# (#, '>', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tslt $at, %s, %s\n" % (reg2, reg1)
		asm_str += "\tbne $at, $zero, %s\n" % (label_set[0])
		asm_str += "\tj %s\n" (label_set[1])
		asm_str += "%s:\n" % (label_set[0])
		asm_str += "\tli %s, 1\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[1])
		asm_str += "\tli %s, 0\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[2])
		
	elif op == "<=":
		new_reg = add_temp_reg(sn)
		label_set = get_label_set_le()
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '<=', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tslt $at, %s, %s\n" % (treg2, treg1)
			else:
				if arg2.isdigit():
					# (#, '<=', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tslt $at, $a0, %s\n" % (treg1)
				else:
					# (#, '<=', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tslt $at, %s, %s\n" % (reg2, treg1)
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '<=', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tslt $at, %s, $a0\n" % (treg2)
				else:
					# (#, '<=', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tslt $at, %s, %s\n" % (treg2, reg1)
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '<=', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tli %s, %s\n" % (new_reg, arg2)
						asm_str += "\tslt $at, %s, $a0\n" % (new_reg)
					else:
						# (#, '<=', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tslt $at, %s, $a0\n" % (reg2)
				else:
					if arg2.isdigit():
						# (#, '<=', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tli $a0, %s\n" % (arg2)
						asm_str += "\tslt $at, $a0, %s\n" % (reg1)
					else:
						# (#, '<=', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tslt $at, %s, %s\n" % (reg2, reg1)
		asm_str += "\tbeq $at, $zero, %s\n" % (label_set[0])
		asm_str += "\tj %s\n" (label_set[1])
		asm_str += "%s:\n" % (label_set[0])
		asm_str += "\tli %s, 1\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[1])
		asm_str += "\tli %s, 0\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[2])
		
	elif op == ">=":
		new_reg = add_temp_reg(sn)
		label_set = get_label_set_ge()
		if isinstance(arg1, int):
			if isinstance(arg2, int):
				# (#, '>=', 2, 6)
				treg1 = get_temp_reg(arg1)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tslt $at, %s, %s\n" % (treg1, treg2)
			else:
				if arg2.isdigit():
					# (#, '>=', 2, '5')
					treg1 = get_temp_reg(arg1)
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tslt $at, %s, $a0\n" % (treg1)
					
				else:
					# (#, '>=', 2, 'y')
					treg1 = get_temp_reg(arg1)
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tslt $at, %s, %s\n" % (treg1, reg2)
		else:
			if isinstance(arg2, int):
				if arg1.isdigit():
					# (#, '>=', '9', 6)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tslt $at, $a0, %s\n" % (treg2)
				else:
					# (#, '>=', 'x', 6)
					reg1 = get_register_from_var(0, sn, arg1)
					treg2 = get_temp_reg(arg2)
					asm_str = "\tslt $at, %s, %s\n" % (reg1, treg2)
			else:
				if arg1.isdigit():
					if arg2.isdigit():
						# (#, '>=', '9', '5')
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tli %s, %s\n" % (new_reg, arg2)
						asm_str += "\tslt $at, $a0, %s\n" % (new_reg)
					else:
						# (#, '>=', '9', 'y')
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tli $a0, %s\n" % (arg1)
						asm_str += "\tslt $at, $a0, %s\n" % (reg2)
				else:
					if arg2.isdigit():
						# (#, '>=', 'x', '5')
						reg1 = get_register_from_var(0, sn, arg1)
						asm_str = "\tli $a0, %s\n" % (arg2)
						asm_str += "\tslt $at, %s, $a0\n" % (reg1)
					else:
						# (#, '>=', 'x', 'y')
						reg1 = get_register_from_var(0, sn, arg1)
						reg2 = get_register_from_var(0, sn, arg2)
						asm_str = "\tslt $at, %s, %s\n" % (reg1, reg2)
		asm_str += "\tbeq $at, $zero, %s\n" % (label_set[0])
		asm_str += "\tj %s\n" (label_set[1])
		asm_str += "%s:\n" % (label_set[0])
		asm_str += "\tli %s, 1\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[1])
		asm_str += "\tli %s, 0\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[2])
		
	elif op == "!":
		new_reg = add_temp_reg(sn)
		label_set = get_label_set_not()
		if (not(arg1 is None)) and (arg2 is None):
			if isinstance(arg1, int):
				# (#, '!', None, 6)
				treg2 = get_temp_reg(arg2)
				asm_str = "\tbeq %s, $zero, %s\n" % (treg2, label_set[0])
			else:
				if arg1.isdigit():
					# (#, '!', None, '5')
					asm_str = "\tli $a0, %s\n" % (arg2)
					asm_str += "\tbeq $a0, $zero, %s\n" % (label_set[0])
				else:
					# (#, '!', None, 'y')
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\tbeq %s, $zero, %s\n" % (reg2, label_set[0])
		elif (arg1 is None) and (not(arg2 is None)):
			if isinstance(arg2, int):
				# (#, '!', 2, None)
				treg1 = get_temp_reg(arg1)
				asm_str = "\tbeq %s, $zero, %s\n" % (treg1, label_set[0])
			else:
				if arg2.isdigit():
					# (#, '!', '9', None)
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tbeq $a0, $zero, %s\n" % (label_set[0])
				else:
					# (#, '!', 'x', None)
					reg1 = get_register_from_var(0, sn, arg1)
					asm_str = "\tbeq %s, $zero, %s\n" % (reg1, label_set[0])
		asm_str += "\tj %s\n" (label_set[1])
		asm_str += "%s:\n" % (label_set[0])
		asm_str += "\tli %s, 1\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[1])
		asm_str += "\tli %s, 0\n" % (new_reg)
		asm_str += "\tj %s\n" (label_set[2])
		asm_str += "%s:\n" % (label_set[2])
		
	elif op == "input":
		new_reg = add_temp_reg(sn)
		if (arg1 is None) and (arg2 is None):
			asm_str = "\tli $v0, 5\n"
			asm_str += "\tsyscall\n"
			asm_str += "\taddi %s, $v0, $zero\n" % (new_reg)
			
	elif op == "print":
		if (not(arg1 is None)) and (arg2 is None):
			if isinstance(arg1, int):
				# (#, 'print', 2, None)
				treg1 = get_temp_reg(arg1)
				asm_str = "\taddi $a0, %s, $zero\n" % (treg1)
				asm_str += "\tli $v0, 1\n"
				asm_str += "\tsyscall\n"
			else:
				if arg1.isdigit():
					# (#, 'print', '9', None)
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tli $v0, 1\n"
					asm_str += "\tsyscall\n"
				else:
					# (#, 'print', 'x', None)
					reg1 = get_register_from_var(0, sn, arg1)
					asm_str = "\taddi $a0, %s, $zero\n" % (reg1)
					asm_str += "\tli $v0, 1\n"
					asm_str += "\tsyscall\n"
		elif (arg1 is None) and (not(arg2 is None)):
			if isinstance(arg2, int):
				# (#, 'print', None, 6)
				treg2 = get_temp_reg(arg2)
				asm_str = "\taddi $a0, %s, $zero\n" % (treg2)
				asm_str += "\tli $v0, 1\n"
				asm_str += "\tsyscall\n"
			else:
				if arg2.isdigit():
					# (#, 'print', None, '5')
					asm_str = "\tli $a0, %s\n" % (arg1)
					asm_str += "\tli $v0, 1\n"
					asm_str += "\tsyscall\n"
				else:
					# (#, 'print', None, 'y')
					reg2 = get_register_from_var(0, sn, arg2)
					asm_str = "\taddi $a0, %s, $zero\n" % (reg2)
					asm_str += "\tli $v0, 1\n"
					asm_str += "\tsyscall\n"
					
	elif (op == "while") or (op == "if"):
		if op == "while":
			label_set = get_label_set_while()
		else:
			label_set = get_label_set_if()
		label_to_map = label_set[1] + ':\n'
		if (not(arg1 is None)) and (not(arg2 is None)):
			cond_reg = get_temp_reg(arg1)
			asm_str = "\tli $a0, 1\n"
			asm_str += "\tbne %s, $a0, %s\n" % (cond_reg, label_set[1])
			label_mapping.append((arg2, label_to_map))

	elif op == "goto":
		label_set = get_label_set_goto()
		label_to_preprend = label_set[0] + ':\n'
		if (not(arg1 is None)) and (arg2 is None):
			prepend_label_to_block(arg1, label_to_prepend)
		elif (arg1 is None) and (not(arg2 is None)):
			prepend_label_to_block(arg2, label_to_prepend)
		asm_str = "\tj %s\n" % (label_set[0])
		
	elif op == "exit":
		asm_str = create_asm_exit()
		
	else:
		print "Syntax Error: Invalid Operator \'%s\' on %s" % (op, sn)

	if(label_exists(sn)):
		map_label(sn, asm_str)
		
	return [sn, asm_str]

