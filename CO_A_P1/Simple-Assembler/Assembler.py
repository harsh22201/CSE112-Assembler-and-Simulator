import inspect

ISA = {
    "add":  "0000000",
    "sub":  "0000100",
    "mov": ["000100", "0001100000"],
    "ld":   "001000",
    "st":   "001010",
    "mul":  "0011000",
    "div":  "0011100000",
    "ls":   "010010",
    "rs":   "010000",
    "or":   "0101100",
    "xor":  "0101000",
    "and":  "0110000",
    "not":  "0110100000",
    "cmp":  "0111000000",
    "jmp":  "011110000",
    "jgt":  "111010000",
    "jlt":  "111000000",
    "je":   "111110000",
    "hlt": "1101000000000000",
    "addf": "1000000",
    "subf": "1000100",
    "movf": "10010",
    "set":  "100110",
    "clr":  "101000",
    "tgl":  "101010",
    "rol":  "101100",
    "ror":  "101110",
}
registers = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111",
}
variables = {}
labels = {}


def dec2bin(number):
    bnum = str(bin(number))[2:]
    s = 7 - len(bnum)
    return "0" * s + bnum


def binaryOfFraction(fraction):
    binary = str()
    for i in range(5):
        fraction *= 2
        if fraction >= 1:
            int_part = 1
            fraction -= 1
        else:
            int_part = 0
        binary += str(int_part)
    return binary


def float2binOrig(real_no):
    if 0 < real_no and real_no < 32:
        int_str = bin(int(real_no))[2:]
        fraction_str = binaryOfFraction(real_no - int(real_no))
        ind = int_str.index("1")
        exp_str = bin((len(int_str) - ind - 1) + 127)[2:]
        mant_str = int_str[ind + 1:] + fraction_str
        mant_str = mant_str + ("0" * (23 - len(mant_str)))
        return exp_str, mant_str
    else:
        return False


def float2bin(real_no):
    real_no = float(real_no)
    if 0 < real_no and real_no < 32:
        int_str = bin(int(real_no))[2:]
        fraction_str = binaryOfFraction(real_no - int(real_no))
        ind = int_str.index("1")
        exp_str = bin((len(int_str) - ind - 1) + 127)[2:]
        mant_str = int_str[ind + 1:] + fraction_str
        mant_str = mant_str + ("0" * (23 - len(mant_str)))
        return exp_str, mant_str
    else:
        return False


def float_to_binary(floating_number):
    try:
        # Convert the string to a floating-point number
        number = float(floating_number)

        # Check if the number can fit into an 8-bit register
        if abs(number) >= 2 ** (8 - 1):
            raise Exception("Number is too large to fit in an 8-bit register.")

        # Convert the number to a binary string with 8 bits
        binary_string = format(int(number), '08b')

        return binary_string

    except Exception as e:
        print("Error:", str(e))


def scan_input():  # Take input from file
    line_no = 0
    raw_assembly = []   # removed empty lines
    while 1:
        try:
            line = input()+' '
            line_no += 1
            if line.isspace():
                continue
            raw_assembly.append([line_no, line])
        except Exception:
            break
    return raw_assembly


def split_instruction_after_label(raw_assembly):
    new_raw_assembly = []
    valid_splits_cnt = 0
    for line_no, line in raw_assembly:
        splitted = line.split(":")
        if len(splitted) == 2:
            leftStr = splitted[0]+":"
            rightStr = splitted[1]
            new_raw_assembly.append([line_no+valid_splits_cnt, leftStr])
            if rightStr.isspace() == False:
                valid_splits_cnt += 1
                new_raw_assembly.append([line_no+valid_splits_cnt, rightStr])
        else:
            new_raw_assembly.append([line_no+valid_splits_cnt, line])

    return new_raw_assembly


def update_var_label(raw_assembly):
    var_ntbegin = False
    assembly = []  # removed variables and labels
    i = 0
    label_line = -1
    for line_no, line in raw_assembly:
        label_line += 1
        line_list = line.split()
        if line_list[0] == "var":
            if 2 != len(line_list):
                raise Exception(f"Error: General Syntax Error, line {line_no}")
            if var_ntbegin:
                raise Exception(
                    f"Error: Variables not declared at beginning, line {line_no}"
                )
            else:
                variables[line_list[1]] = i
                i += 1
            continue
        elif line_list[0][-1] == ":":
            label = line_list[0]
            if len(line_list[0]) < 2 or label == ":":
                raise Exception(f"Error: General Syntax Error, line {line_no}")
            else:
                labels[label[:-1]] = label_line
        
            var_ntbegin = True
            continue
        var_ntbegin = True
        assembly.append([line_no, line_list])
    return assembly


def verify_regregreg(syntax, line_no):
    if len(syntax) != 3:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    for register in syntax:
        if register == "FLAGS":
            raise Exception(
                f"Error: Illegal use of FLAGS register, line {line_no}")
        if register not in registers:
            raise Exception(
                f"Error: Invalid Register name {register}, line {line_no}")
    return None


def verify_regreg(syntax, line_no):
    if len(syntax) != 2:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    for register in syntax:
        if register == "FLAGS":
            raise Exception(
                f"Error: Illegal use of FLAGS register, line {line_no}")
        if register not in registers:
            raise Exception(
                f"Error: Invalid Register name {register}, line {line_no}")
    return None


def verify_jump(syntax, line_no):
    if len(syntax) != 1:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    label = syntax[0]
    if (label in variables) and (label not in labels):
        raise Exception(
            f"Error: Misuse of variables as labels, line {line_no}")
    if label not in labels:
        raise Exception(
            f"Error: Use of undefined labels {label}, line {line_no}")
    return None


def verify_regvar(syntax, line_no):
    if len(syntax) != 2:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    register = syntax[0]
    variable = syntax[1]
    if register == "FLAGS":
        raise Exception(
            f"Error: Illegal use of FLAGS register, line {line_no}")
    if register not in registers:
        raise Exception(
            f"Error: Invalid Register name {register}, line {line_no}")
    if (variable not in variables) and (variable in labels):
        raise Exception(
            f"Error: Misuse of labels as variables, line {line_no}")
    if variable not in variables:
        raise Exception(
            f"Error: Use of undefined variables {variable}, line {line_no}")
    return None


def verify_regimm(syntax, line_no):
    if len(syntax) != 2:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    register = syntax[0]
    imm = syntax[1]
    if register == "FLAGS":
        raise Exception(
            f"Error: Illegal use of FLAGS register, line {line_no}")
    if register not in registers:
        raise Exception(
            f"Error: Invalid Register name {register}, line {line_no}")
    if imm[0] != "$" or len(imm) == 1:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    for x in range(1, len(imm)):
        if not imm[x].isdigit():
            raise Exception(f"Error: Illegal Immediate values, line {line_no}")
    if int(imm[1:]) > 127:
        raise Exception(f"Error: Illegal Immediate values, line {line_no}")


def verify_bonus(syntax, line_no):
    if len(syntax) != 2:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    register = syntax[0]
    imm = syntax[1]
    if register == "FLAGS":
        raise Exception(
            f"Error: Illegal use of FLAGS register, line {line_no}")
    if register not in registers:
        raise Exception(
            f"Error: Invalid Register name {register}, line {line_no}")
    if imm[0] != "$" or len(imm) == 1:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    for x in range(1, len(imm)):
        if not imm[x].isdigit():
            raise Exception(f"Error: Illegal Immediate values, line {line_no}")
    if int(imm[1:]) > 15:
        raise Exception(f"Error: Illegal Immediate values, line {line_no}")


def verify_mov(syntax, line_no):
    if len(syntax) != 2:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    register1 = syntax[0]
    arg2 = syntax[1]
    if register1 == "FLAGS":
        raise Exception(
            f"Error: Illegal use of FLAGS register, line {line_no}")
    if register1 not in registers:
        raise Exception(
            f"Error: Invalid Register name {register1}, line {line_no}")
    if arg2[0] == "$":
        for x in range(1, len(arg2)):
            if not arg2[x].isdigit():
                raise Exception(f"Error: General Syntax Error, line {line_no}")
        if int(arg2[1:]) > 127:
            raise Exception(f"Error: Illegal Immediate values, line {line_no}")
    else:
        if arg2 not in registers:
            raise Exception(
                f"Error: Invalid Register name {arg2}, line {line_no}")


def verify_movf(syntax, line_no):
    if len(syntax) != 2:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    register1 = syntax[0]
    imm = syntax[1]
    if register1 == "FLAGS":
        raise Exception(
            f"Error: Illegal use of FLAGS register, line {line_no}")
    if register1 not in registers:
        raise Exception(
            f"Error: Invalid Register name {register1}, line {line_no}")
    if imm[0] != "$" or len(imm) == 1:
        raise Exception(f"Error: General Syntax Error, line {line_no}")
    imm = imm[1:]
    try:
        imm = float(imm)
    except ValueError:
        raise Exception(f"Error: General Syntax Error, line {line_no}")


def inspect_syntax(assembly):
    for line_no, line in assembly:
        if len(line) == 0:
            continue
        instruction = line[0]

        if instruction not in ISA:
            raise Exception(
                f"Error: Invalid Instruction {instruction}, line {line_no}")
        syntax = line[1:]
        if instruction in ["add", "sub", "mul", "xor", "or", "and", "addf", "subf"]:
            verify_regregreg(syntax, line_no)
        elif instruction in ["jmp", "jlt", "je", "jgt"]:
            verify_jump(syntax, line_no)
        elif instruction in ["ld", "st"]:
            verify_regvar(syntax, line_no)
        elif instruction in ["ls", "rs"]:
            verify_regimm(syntax, line_no)
        elif instruction in ["div", "not", "cmp"]:
            verify_regreg(syntax, line_no)
        elif instruction == "mov":
            verify_mov(syntax, line_no)
        elif instruction == "movf":
            verify_movf(syntax, line_no)
        elif instruction in ["set", "clr", "tgl", "rol", "ror"]:
            verify_bonus(syntax, line_no)
        elif instruction is not assembly[-1][1][0]:
            raise Exception(
                f"Error: Can't execute lines after hlt, line {line_no}")
        else:
            pass
    if assembly[-1][1] != ["hlt"]:
        line_no = assembly[-1][0]
        raise Exception(f"Error: Missing Halt instruction at the end")
    return None


def generate_binary(assembly):
    bin_count = 1
    binary = ""
    for _, line in assembly:
        if len(line) == 0:
            continue
        instruction = line[0]
        syntax = line[1:]
        if instruction == "mov":
            if syntax[1][0] == "$":
                binary += "000100"
                register = syntax[0]
                imm = int(syntax[1][1:])
                binary += registers[register]
                binary += dec2bin(imm)
            else:
                binary += "0001100000"
                for register in syntax:
                    binary += registers[register]
            binary += "\n"
            bin_count += 1
            continue
        binary += ISA[instruction]
        if instruction in [
            "add",
            "sub",
            "mul",
            "xor",
            "or",
            "and",
            "div",
            "not",
            "cmp",
            "addf",
            "subf",
        ]:
            for register in syntax:
                binary += registers[register]
        elif instruction in ["jmp", "jlt", "je", "jgt"]:
            label = syntax[0]
            binary += labels[label]
        elif instruction in ["ld", "st"]:
            register = syntax[0]
            variable = syntax[1]
            binary += registers[register]
            var_x = int(variables[variable], 2)
            new_val = var_x + len(assembly)
            binary += format(new_val, '07b')
        elif instruction in ["ls", "rs"]:
            register = syntax[0]
            imm = int(syntax[1][1:])
            binary += registers[register]
            binary += dec2bin(imm)
        elif instruction in ["set", "clr", "tgl", "rol", "ror"]:
            register = syntax[0]
            imm = int(syntax[1][1:])
            binary += registers[register]
            binary += dec2bin(imm)
        elif instruction == "movf":
            register = syntax[0]
            imm_str = syntax[1][1:]
            binary += registers[register]
            #expo_str,mantissa_str = float2bin(imm_str)
            #binary += expo_str
            #binary += mantissa_str
            binary += float_to_binary(imm_str)
        else:
            break
        binary += "\n"
        bin_count += 1
    if bin_count > 128:
        raise Exception(f"Error: Assembler can write upto 128 lines")
    return binary


def main():
    raw_assembly = scan_input()
    new_raw_assembly = split_instruction_after_label(raw_assembly)
    raw_assembly = new_raw_assembly

    # if len(raw_assembly) > 128:
    #    raise Exception(f"Error: Assembler can write upto 128 lines")
    assembly = update_var_label(raw_assembly)

    skipLabels = 0
    for label in labels:
        labels[label] = dec2bin(labels[label] - len(variables) - skipLabels)
        skipLabels += 1
    for variable in variables:
  
        variables[variable] = dec2bin(variables[variable])
    inspect_syntax(assembly)
    binary = generate_binary(assembly)
    print(binary)

    # f = open("stdout.txt", "w")
    # f.write(binary)
    # f.close()


try:
    main()
except Exception as error:
    print(str(error))
    # f = open("stdout.txt", "w")
    # f.write(str(error))
    # f.close()
