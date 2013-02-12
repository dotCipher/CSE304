# ---------------------------------------------------- #
# CSE 304/504
# HW 1
# Cody Moore
# Part A: Python Lists
# ---------------------------------------------------- #
# Imports and globals
import re
lastNumber = re.compile(r'(?:[^\d]*(\d+)[^\d]*)+')
# ---------------------------------------------------- #
# HELPER: Find sequence of numbers in string 
#	and increment

def increment_string(inStr):
    mutableString = lastNumber.search(inStr)
    if mutableString:
        next = str(int(mutableString.group(1))+1)
        start, end = mutableString.span(1)
        inStr = inStr[:max(end-len(next), start)] + next + inStr[end:]
    return inStr
# ---------------------------------------------------- #
# HELPER: Get Defined and Used Element Lists

def get_def_and_use(list_of_assignments):
	i = 0
	definedElements = list()
	usedElements = list()
	while i < len(list_of_assignments):
		assignment = list_of_assignments[i]
		definedElements.append((i+1, assignment[0]))
		j = 0
		while j < len(assignment[1]):
			usedElements.append((i+1, assignment[1][j]))
			j += 1
		i += 1
	definedElements.sort()
	usedElements.sort()
	return definedElements, usedElements
# ---------------------------------------------------- #
# HELPER: Get Defined and Used Element Lists

def create_list_of_assignments(def_elements, used_elements):
	list_of_assignments = list()
	defLen = len(def_elements)
	totalNumLines = def_elements[defLen-1][0]
	i = 0
	# Iterate all lines and check both
	#  lists to build assignment list
	while i < totalNumLines:
		used_array = list()
		var = def_elements[i][1]
		lineDefined = def_elements[i][0]
		# Find all used vars in line i
		j = 0
		while j < len(used_elements):
			if used_elements[j][0] == lineDefined:
				used_array.append(used_elements[j][1])
			j += 1
		assignment = [var, used_array]
		list_of_assignments.append(assignment)
		i += 1
	return list_of_assignments
# ---------------------------------------------------- #
# HELPER: Get Unique Variables

def get_unique_vars(used_elements):
	uniqueVars = set()
	i = 0
	while i < len(used_elements):
		uniqueVars.add(used_elements[i][1])
		i += 1
	return uniqueVars
# ---------------------------------------------------- #
# HELPER: Find line first seen

def find_line_first_seen(variable, def_or_use_elements):
	i = 0
	lineFirstSeen = -1
	# Find line first seen
	while i < len(def_or_use_elements):
		assignment = def_or_use_elements[i]
		if (variable == assignment[1]) and (lineFirstSeen == -1):
			lineFirstSeen = assignment[0]
		i += 1
	return lineFirstSeen
# ---------------------------------------------------- #
# HELPER: Find line second seen

def find_line_second_seen(variable, def_or_use_elements):
	i = 0
	lineFirstSeen = -1
	lineSecondSeen = -1
	# Find line second seen
	while i < len(def_or_use_elements):
		assignment = def_or_use_elements[i]
		if (variable == assignment[1]) and (lineFirstSeen != -1):
			lineSecondSeen = assignment[0]
			break
		if (variable == assignment[1]) and (lineFirstSeen == -1):
			lineFirstSeen = assignment[0]
		i += 1
	return lineSecondSeen
# ---------------------------------------------------- #
# HELPER: Replace elements after first

def replace_after_first(variable, def_or_use_elements):
	i = 0
	lineFirstSeen = find_line_first_seen(variable, def_or_use_elements)
	# Replace all elements after lineFirstSeen
	while i < len(def_or_use_elements):
		assignment = def_or_use_elements[i]
		# Modify assignment only by replacing
		#	after line first seen
		if assignment[1] == variable:
			if assignment[0] > lineFirstSeen:
				hasNum = bool(re.search('[0-9]', assignment[1], re.IGNORECASE))
				# If var has num, increment, else append num
				if hasNum:
					newVar = increment_string(assignmen[1])
					line = assignment[0]
					newTuple = (line, newVar)
					def_or_use_elements[i] = newTuple
				else:
					newVar = assignment[1] + '1'
					line = assignment[0]
					newTuple = (line, newVar)
					def_or_use_elements[i] = newTuple
		i += 1
	return def_or_use_elements
# ---------------------------------------------------- #
# HELPER: Replace elements after second

def replace_after_second(variable, def_or_use_elements):
	i = 0
	lineSecondSeen = find_line_second_seen(variable, def_or_use_elements)
	# Replace all elements after lineSecondSeen
	while i < len(def_or_use_elements):
		assignment = def_or_use_elements[i]
		# Modify assignment only by replacing
		#	after line first seen
		if assignment[1] == variable:
			if assignment[0] > lineSecondSeen:
				hasNum = bool(re.search('[0-9]', assignment[1], re.IGNORECASE))
				# If var has num, increment, else append num
				if hasNum:
					newVar = increment_string(assignmen[1])
					line = assignment[0]
					newTuple = (line, newVar)
					def_or_use_elements[i] = newTuple
				else:
					newVar = assignment[1] + '1'
					line = assignment[0]
					newTuple = (line, newVar)
					def_or_use_elements[i] = newTuple
		i += 1
	return def_or_use_elements
# ---------------------------------------------------- #
# 1. Duplicates
# 	Algorithm:
# 	1- Sort the list
# 	2- Do single pass of list
#	3- Add all elements found
# 	3- Return boolean if duplicate found

def dup(list):
	list.sort()
	seenElements = set()
	for i in list:
		if i in seenElements:
			return True
		seenElements.add(i)
	return False
# ---------------------------------------------------- #
# 2. Defined_use
#	Algorithm
#	1- Get lists of defined and used elements
#	2- Do single pass of list_of_assignments
#	3- For each assignment, select definitions and
#		append to defined list
#	4- For each assignment, select used elements and
#		append to used list
#	5- Do check of used list and compare indices to 
#		defined list for differences
#	6- Return new list of elements used before defined

def def_use(list_of_assignments):
	# Initialize counters
	x = 0
	i = 0
	j = 0
	# Populate lists of defined and used elements
	definedElements = list()
	usedElements = list()
	definedElements, usedElements = get_def_and_use(list_of_assignments)
	# Get array of unique variables
	uniqueVars = get_unique_vars(usedElements)
	# Iterate through all unique variables,
	#  compare differences of indexed elements
	#  add all elements that have used >= defined
	tmpVars = uniqueVars.copy()
	usedBeforeDefElements = list()
	while x < len(tmpVars):
		checkVar = uniqueVars.pop()
		firstDefined = -1
		firstUsed = -1
		i = 0
		j = 0
		while i < len(usedElements):
			if checkVar == usedElements[i][1]:
				firstUsed = usedElements[i][0]
				break
			i += 1
		while j < len(definedElements):
			if checkVar == definedElements[j][1]:
				firstDefined = definedElements[j][0]
				break
			j += 1
		if firstUsed <= firstDefined:
			usedBeforeDefElements.append(checkVar)
		elif firstDefined == -1:
			usedBeforeDefElements.append(checkVar)
		x += 1
	
	return usedBeforeDefElements
# ---------------------------------------------------- #
# 3. SSA
#	Assumption:
#		All variables are defined before usage
#	Algorithm
#	1- Get unique list of elements used
#	2- Get lists of defined and used elements
#	3- 
def ssa(list_of_assignments):
	# Initialize counters
	i = 0
	j = 0
	# Populate lists of defined and used elements
	definedElements = list()
	usedElements = list()
	definedElements, usedElements = get_def_and_use(list_of_assignments)
	# Get array of unique variables
	uniqueVars = get_unique_vars(definedElements)
	# Iterate through defined elements
	# Make sure to repeat this loop until no duplicates
	#  are found in the definitions
	seenElements = set()
	SSAForm = False
	while SSAForm != True:
		while i < len(definedElements):
			definedElement = definedElements[i]
			if definedElement[1] in seenElements:
				definedElements = replace_after_first(definedElement[1], definedElements)
				usedElements = replace_after_second(definedElement[1], usedElements)
				# If element is seen, replace all instances
				#   in definedElements and usedElements 
				#	after first instance of definition
			else:
				seenElements.add(definedElement[1])
			i += 1
		# Check if in SSA Form
		uniqueVars = get_unique_vars(definedElements)
		if len(uniqueVars) == len(definedElements):
			SSAForm = True
			break
		else:
			SSAForm = False
	# Recreate list of assignments from changed lists
	list_of_assignments = create_list_of_assignments(definedElements, usedElements)
	return list_of_assignments
	
# ---------------------------------------------------- #
