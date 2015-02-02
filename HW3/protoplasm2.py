# -------------------------------------------------------- #
# Protoplasm 2 - Main Caller
# -------------------------------------------------------- #
#
# -------------------------------------------------------- #
# Imports and globals
# -------------------------------------------------------- #
import sys
import ply.lex as lex
import ply.yacc as yacc
import protoplasm_parse
import protoplasm_lex
import protoplasm_interp
import protoplasm_mips

# -------------------------------------------------------- #
# Main Code Block
# -------------------------------------------------------- #
def main():
	s = ''
	if len(sys.argv) > 1:
		f = open(sys.argv[1],'r')
		for line in f:
			s += line
	else:
		print 'Please run protoplasm with this format: protoplasm2.py arg1'
		print 'arg1 being a .proto file'
	if len(sys.argv) > 1:
		for line in f:
			s += line + ' '
		
		program = protoplasm_parse.parse(s)
		# Global of triples set up in protoplasm_interp
		intermediate_code = protoplasm_interp.gencode(program, 0)
		protoplasm_mips.add_exit(intermediate_code)
		protoplasm_mips.get_liveness(intermediate_code)
		#protoplasm_interp.optimize()
		print ""
		print ""
		print program
		print ""
		print ""
		print ""
		print ""
		print intermediate_code
		print ""
		print ""
		print ""
		print ""
		print protoplasm_mips.liveness
		print ""
		print ""
		
		# Get file name to write too
		#i = sys.argv[1].rindex('.')
		#substr = sys.argv[1][:i]
		#filename = substr + ".asm"
		
		# Generate MIPS from intermediate code
		#protoplasm_mips.make_asm_exec(filename, protoplasm_interp.triples)
		#print "Written out to file: %s" % filename

if __name__ == "__main__":
	main()
