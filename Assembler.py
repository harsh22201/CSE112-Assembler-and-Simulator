ISA = {'add' : '0000000', 'sub' : '0000100', 'mov' : ['000100','0001100000'], 'ld' :'001000' , 'st' : '001010', 'mul' : '0011000', 'div' : '0011100000', 'ls' : '010010', 'rs' : '010000', 'or' : '0101100', 'xor' : '0101000', 'and' : '0110000', 'not' : '0110100000', 'cmp' : '0111000000', 'jmp' : '011110000', 'jgt' : '111010000', 'jlt' : '111000000', 'je' : '111110000','hlt':'1101000000000000'}#,'addf':'1000000','subf':'1000100','movf':'10010'}
registers  = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}
variables = {}
labels = {} 

def dec2bin(number):
    bnum = str(bin(number))[2:]
    s = 7 - len(bnum)
    return '0'*s + bnum

def binaryOfFraction(fraction):
	binary = str()
	for i in range(5):
		fraction *= 2
		if (fraction >= 1):
			int_part = 1
			fraction -= 1
		else:
			int_part = 0
		binary += str(int_part)
	return binary

def float2bin(real_no):
    if (0<real_no and real_no<32):
        int_str = bin(int(real_no))[2 : ]
        fraction_str = binaryOfFraction(real_no - int(real_no))
        ind = int_str.index('1')
        exp_str = bin((len(int_str) - ind - 1) + 127)[2 : ]
        mant_str = int_str[ind + 1 : ] + fraction_str
        mant_str = mant_str + ('0' * (23 - len(mant_str)))
        return  exp_str, mant_str
    else:
        return False

def scan_input():  # Take input from file
    f = open("stdin.txt",'r')
    lines = f.readlines()
    line_no = 0
    raw_assembly = []   # removed empty lines 
    for line in lines:
        line_no += 1
        if line.isspace():
            continue
        raw_assembly.append([line_no, line])
        if not line:
            break
    f.close()
    return raw_assembly

def update_var_label(raw_assembly):
    var_ntbegin = False
    assembly = []  # removed variables and labels
    i = 0
    label_line = -1
    for line_no, line in raw_assembly:
        label_line+=1
        line_list = line.split()
        if(line_list[0] == 'var'):
            if( 2 != len(line_list)):
                raise Exception(f'Error: General Syntax Error, line {line_no}')
            if var_ntbegin:
                raise Exception(f'Error: Variables not declared at beginning, line {line_no}')
            else:
                variables[line_list[1]]=i
                i+=1
            continue
        elif(line_list[0][-1] == ':'):
            label = line_list[0]
            if(len(line_list) <2 or label==':'):
                raise Exception(f'Error: General Syntax Error, line {line_no}')
            else:
                labels[label[:-1]] = label_line
                assembly.append([line_no, line_list[1:]])
            var_ntbegin = True
            continue
        var_ntbegin = True
        assembly.append([line_no, line_list])
    return assembly

def verify_regregreg(syntax,line_no):
    if (len(syntax)!= 3):
        raise Exception(f'Error: General Syntax Error, line {line_no}')
    for register in syntax:
        if register == 'FLAGS':
            raise Exception(f'Error: Illegal use of FLAGS register, line {line_no}')
        if register not in registers:
            raise Exception(f'Error: Invalid Register name, line {line_no}')
    return None

def verify_regreg(syntax,line_no):
    if (len(syntax)!= 2):
        raise Exception(f'Error: General Syntax Error, line {line_no}')
    for register in syntax:
        if register == 'FLAGS':
            raise Exception(f'Error: Illegal use of FLAGS register, line {line_no}')
        if register not in registers:
            raise Exception(f'Error: Invalid Register name, line {line_no}')
    return None

def verify_jump(syntax,line_no):
    if (len(syntax)!=1):
        raise Exception(f'Error: General Syntax Error, line {line_no}')
    label = syntax[0]
    if ((label in variables )and(label not in labels )):
        raise Exception(f'Error: Misuse of variables as labels, line {line_no}')
    if ((label not in labels )):
        raise Exception(f'Error: Use of undefined labels, line {line_no}')
    return None

def verify_regvar(syntax,line_no):
    if len(syntax)!=2:
        raise Exception(f'Error: General Syntax Error, line {line_no}')
    register = syntax[0]
    variable = syntax[1]
    if register == 'FLAGS':
        raise Exception(f'Error: Illegal use of FLAGS register, line {line_no}')
    if register not in registers:
        raise Exception(f'Error: Invalid Register name, line {line_no}')
    if ((variable not in variables )and( variable  in labels )):
        raise Exception(f'Error: Misuse of labels as variables, line {line_no}')
    if ((variable not in variables )):
        raise Exception(f'Error: Use of undefined variables, line {line_no}')
    return None

def verify_regimm(syntax,line_no):
    if len(syntax)!=2:
        raise Exception(f'Error: General Syntax Error, line {line_no}')
    register = syntax[0]
    imm = syntax[1]
    if register == 'FLAGS':
        raise Exception(f'Error: Illegal use of FLAGS register, line {line_no}')
    if register not in registers:
        raise Exception(f'Error: Invalid Register name, line {line_no}')
    if imm[0]!= '$' or len(imm) == 1:
        raise Exception(f'Error: General Syntax Error, line {line_no}')
    for x in range(1, len(imm)):
        if not imm[x].isdigit():
            raise Exception(f'Error: Illegal Immediate values, line {line_no}')
    if int(imm[1:])>127:
        raise Exception(f'Error: Illegal Immediate values, line {line_no}')

def verify_mov(syntax,line_no):
    if len(syntax)!=2:
        raise Exception(f'Error: General Syntax Error, line {line_no}')
    register1 = syntax[0]
    arg2 = syntax[1]
    if register1 == 'FLAGS':
        raise Exception(f'Error: Illegal use of FLAGS register, line {line_no}')
    if register1 not in registers:
        raise Exception(f'Error: Invalid Register name, line {line_no}')
    if arg2[0]== '$':
        for x in range(1, len(arg2)):
            if not arg2[x].isdigit():
                raise Exception(f'Error: General Syntax Error, line {line_no}')
        if int(arg2[1:])>127:
            raise Exception(f'Error: Illegal Immediate values, line {line_no}')
    else :
        if arg2 not in registers:
            raise Exception(f'Error: Invalid Register name, line {line_no}')

def verify_movf(syntax,line_no):
    if len(syntax)!=2:
        raise Exception(f'Error: General Syntax Error, line {line_no}')
    register1 = syntax[0]
    imm = syntax[1]
    if register1 == 'FLAGS':
        raise Exception(f'Error: Illegal use of FLAGS register, line {line_no}')
    if register1 not in registers:
        raise Exception(f'Error: Invalid Register name, line {line_no}')
    if imm[0]!= '$' or len(imm)==1:
        raise Exception(f'Error: General Syntax Error, line {line_no}')
    imm = imm[1:]
    try :
        imm = float(imm) 
    except ValueError : 
        raise Exception(f'Error: General Syntax Error, line {line_no}')

def inspect_syntax(assembly):
    for line_no,line in assembly : 
        instruction = line[0]
        if(instruction not in ISA):
            raise Exception(f'Error: Invalid Instruction, line {line_no}')
        syntax = line[1:]
        if ( instruction in ["add", "sub", "mul", "xor","or", "and"]):
            verify_regregreg(syntax,line_no)
        elif (instruction in ["jmp","jlt","je","jgt"]):
            verify_jump(syntax,line_no)
        elif (instruction in ['ld','st']):
            verify_regvar(syntax,line_no)
        elif (instruction in ['ls','rs']):
            verify_regimm(syntax,line_no)
        elif (instruction in ['div','not','cmp']):
            verify_regreg(syntax,line_no)
        elif (instruction == 'mov'):
            verify_mov(syntax,line_no)
        elif instruction is not  assembly[-1][1][0]:
            raise Exception(f'Error: Can\'t execute lines after hlt, line {line_no}')
        else : 
            pass
    if assembly[-1][1] != ['hlt']:
        line_no = assembly[-1][0]
        raise Exception(f'Error: Missing Halt instruction at the end')
    return None

def generate_binary(assembly): 
    binary=""
    for _,line in assembly : 
        instruction = line[0]
        syntax = line[1:]
        if (instruction == 'mov'):
            if syntax[1][0] == '$':
                binary+='000100'
                register  = syntax[0]
                imm = int(syntax[1][1:])
                binary+= registers[register]
                binary += dec2bin(imm)
            else :
                binary+= '0001100000'
                for register in syntax:
                    binary+=registers[register]
            binary+='\n'
            continue
        binary+= ISA[instruction]
        if ( instruction in ["add", "sub", "mul", "xor","or", "and",'div','not','cmp']):
            for register in syntax:
                binary+=registers[register]
        elif (instruction in ["jmp","jlt","je","jgt"]):
            label = syntax[0]
            binary+=labels[label]
        elif (instruction in ['ld','st']):
            register  = syntax[0]
            variable = syntax[1]
            binary+= registers[register]
            binary += variables[variable]
        elif (instruction in ['ls','rs']):
            register  = syntax[0]
            imm = int(syntax[1][1:])
            binary+= registers[register]
            binary += dec2bin(imm)
        elif(instruction  == 'movf'):
            register  = syntax[0]
            imm = int(syntax[1][1:])
            binary+= registers[register]
            binary += float2bin(imm)
        else :
            break
        binary += '\n'  
    return binary

def main():
    raw_assembly = scan_input()
    if (len(raw_assembly)>128):
        raise Exception(f'Error: Assembler can write upto 128 lines')
    assembly = update_var_label(raw_assembly)
    for label in labels :
        labels[label]  = dec2bin(labels[label]-len(variables))
    for variable in variables :
        variables[variable]  = dec2bin(variables[variable]+len(assembly))
    inspect_syntax(assembly)
    binary = generate_binary(assembly)
    f = open("stdout.txt",'w')
    f.write(binary)
    f.close()

try :
    main()
except Exception as error:
    f = open("stdout.txt",'w')
    f.write(str(error))
    f.close()
