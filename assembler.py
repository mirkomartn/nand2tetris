import sys, os

class Assembler:
    '''Takes an .asm program written in HACK assembly and translates it to HACK machine code. For more see http://www.nand2tetris.org/.'''
    
    def __init__(self):
    
        self.comp_dict = {'0':'101010', '1':'111111', '-1':'111010', 'D':'001100', 'A':'110000', '!D':'001101', '!A':'110001', '-D':'001111', '-A':'110011',
                 'D+1':'011111', 'A+1':'110111', 'D-1':'001110', 'A-1':'110010', 'D+A':'000010', 'D-A':'010011', 'A-D':'000111', 'D&A':'000000',
                 'D|A':'010101'}

        self.jmp_dict = {'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}

        self.dest_dict = {'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'}
        
        self.sym_dict = {'SCREEN':'16384', 'KBD':'24576', 'SP':'0', 'LCL':'1', 'ARG':'2', 'THIS':'3', 'THAT':'4'}
        
        for x in range(16):
            self.sym_dict['R{}'.format(x)] = '{}'.format(x)
        
        
    def assemble(self, source):
    	'''The only intended interface to the Assembler class. takes a relative or absolute path to an *.asm program written in a HACK assembly and writes the 			   respective machine code to *.hack in the same directory as the *.asm file.'''
    	
    	with open(source, 'r') as f:
    		program = f.read()
    		instructions = self.translate((line.replace(' ', '') for line in program.split('\n') if line)) ## "if line" excludes empty lines
    		machine_code = '\n'.join(instructions)
    		
    		target = '{}.hack'.format(source.split('.')[0])
    		
    		print('\nMachine code successfully generated! Writing to {}.\n'.format(target))
    		
    		with open(target, 'w') as t:
    			t.write(machine_code)
    			
    def	translate(self, program):
    	'''A generator object yielding machine code assembled from the input assembly code one line at a time.'''
    
    	lines = [x for x in self.parse_lines(program)] #has to be a list, since it's get iterated over multiple times
    	
    	self.get_symbols(lines) # this needs to be done after parsing, to get the line numbers right
    	
    	for line in lines:
    	
    		#ignore the labeled lines
    		if line[0] == '(':
    			continue
    			
    		if line[0] == '@':
    			if not line[1:].isnumeric():
    				line = line.replace(line[1:], self.sym_dict[line[1:]])
    			temp = bin(int(line[1:]))[2:] # take the rest of the line, turn it into an integer, get the binary value and ignore the rest 
    			yield "000000000000000{}".format(temp)[-16:] # make sure the total number of bits == 16
    			continue # necessary because of a fallthrough to the second yield
    			
    		try:
    			dest, comp = line.split('=')
    			dest = self.dest_dict[dest]
    		except:
    			dest = '000'
    			
    		try:
    			comp, jump = line.split(';')
    			jump = self.jmp_dict[jump]
    		except:
    			jump = '000'
    			
    		a, comp = self.parse_comp(comp)
    		
    		yield "111{}{}{}{}".format(a, comp, dest, jump)
    		
    def parse_comp(self, comp):
    	'''Returns the values of the a bit and the c bits.'''
    	
    	a = 0
    	
    	# if 'M' is computed with, fix the a bit, then replace all the occurences of 'M' with 'A' to simplify the comp_dict query
    	if 'M' in comp:
    		a = 1
    		comp = comp.replace('M', 'A')
    		
    	c = self.comp_dict[comp]
    	
    	return a, c
    	
    
    def parse_lines(self, program):
    	'''Removes inline comments and replaces pure comment lines with an empty string. Works as a generator!'''
    	
    	for line in program:
    	
    		try:
    			line = line.split('//')[0]  # remove in-line comments, if line starts with '//', '' is returned
    		except:
    			pass
    			
    		# because self.parse_line returns an empty string for comment lines
    		if line:
    			yield line
    def get_symbols(self, program):
    	'''Goes through the code and gets the number appropriate number lines matched to the labels used in the assembly code.'''
    	
    	count = 0 # needs to count the number of labels, to compute the offset in the line number
    	reg_count = 16 # the general register counter
    	for num,line in enumerate(program):
    		if line[0] == '(':
    			new_key = line.split(')')[0].replace('(', '')
    			self.sym_dict[new_key] = str(num - count)
    			count += 1
    	
    	#the loops need to be separate because @LABEL might be referrenced before (LABEL) is declared!
    	for line in (program):
    		if line[0] == '@':
    			if line[1:] in self.sym_dict or line[1:].isnumeric(): #not all @ instructions include labels!
    				continue
    			self.sym_dict[line[1:]] = str(reg_count)
    			reg_count += 1
                

if __name__ == '__main__':

	ass = Assembler()

	targets = sys.argv[1:3]
	
	if not targets:
		ans = input("No targets given. Type 'y/Y' to assemble all .asm files in the directory: ")
		if ans in 'yY':
			targets = (x for x in os.listdir() if '.asm' in x)
				
	count = 0
	
	for target in targets:
		ass.assemble(target)
		count += 1
	
	print('Done! Total number of programs assembled: {}'.format(count))
