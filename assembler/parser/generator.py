import array

from assembler.tokenizer import tokentype

def condition_bytes(condition):
    condition_bytes = 0x00000000
    if condition == "AL":
        condition_bytes = 0xE0000000
    elif condition == "CS":
        conditin_bytes = 0x20000000
    elif condition == "NE":
        condition_bytes = 0x10000000
    elif condition == "CC":
        conditin_bytes = 0x30000000
    elif condition == "MI":
        conditin_bytes = 0x40000000
    elif condition == "PL":
        conditin_bytes = 0x50000000
    elif condition == "VS":
        condition_bytes = 0x60000000 
    elif condition == "VC":
        condition_bytes = 0x70000000
    elif condition == "HI":
        condiiton_bytes = 0x80000000
    elif condition == "LS":
        condition_bytes = 0x90000000
    elif condition == "GE":
        conditin_bytes = 0xA0000000
    elif condition == "LT":
        conditin_bytes = 0xB0000000
    elif condition == "GT":
        conditin_bytes = 0xC0000000
    elif condition == "LE":
        conditin_bytes = 0xD0000000

    return condition_bytes

def get_operation_values(operation, code_upper):
    operation_literal = operation.value
    operation_code = operation_literal[:code_upper].upper()
    condition_string = operation_literal[code_upper:code_upper + 2].upper()
    condition = condition_bytes(condition_string)
    options = operation_literal[code_upper + 2:].upper()
    return operation_code, condition, options

def from_bi_register_imm(params):
    destination_register = params.value[0].value
    operand_register = params.value[1].value[0].value
    imm = params.value[1].value[1].value

    return destination_register, operand_register, imm

class Generator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.labels = {}
        self.byte_buffer = array.array('I')
        self.byte_buffer.append(0)
        self.unresolved_label_refs = {}
        self.instruction_counter = 0

    def __enter__(self):
        self.f = open(self.file_path, "wb")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.f.close()
        #reloop over file and replace necessary labels
        self.resolve_label_refs()

    def resolve_label_refs(self):
        self.f = open(self.file_path, "rb+")
        
        for instruction_index, label_name in self.unresolved_label_refs.items():
            label_instruction_index = self.labels[label_name]
            address = self.get_signed_relative_address(label_instruction_index, instruction_index)

            seek_point = (instruction_index * 4) 
            self.f.seek(seek_point)
            instruction = int.from_bytes(self.f.read(4), byteorder='little')
            self.f.seek(seek_point)

            bytecode = address | instruction

            address_byte_array = array.array('I')
            address_byte_array.append(bytecode)
            self.f.write(address_byte_array.tobytes())

    def get_signed_relative_address(self, instruction1_index, instruction2_index):
        difference = instruction1_index - instruction2_index
        address = 0x000000

        if difference < 0:
            address = 0xFFFFFE
        address += difference
        
        return address

    def write_instruction(self, instruction_token):
        label = instruction_token.value[0]
        instruction = instruction_token.value[1]
        if label:
            self.labels[label.value] = self.instruction_counter

        operation_token = instruction_token.value[1]
        if operation_token.token_type == tokentype.SimpleArithmeticLogicOperation:
            encoding_method = self.simple_arithmetic_logic_encoding
        elif operation_token.token_type == tokentype.ConditionSetterOperation:
            encoding_method = self.condition_setter_encoding
        elif operation_token.token_type == tokentype.MulOperation:
            encoding_method = self.mul_operation_encoding
        elif operation_token.token_type == tokentype.BranchOperation:
            encoding_method = self.branch_operation_encoding
        elif operation_token.token_type == tokentype.MovOperation:
            encoding_method = self.mov_operation_encoding
        elif operation_token.token_type == tokentype.LdrStrOperation:
            encoding_method = self.ldrstr_operation_encoding
        elif operation_token.token_type == tokentype.DivOperation:
            encoding_method = self.div_operation_encoding

        bytecode = encoding_method(instruction)
        self.write_bytes(bytecode)
        self.instruction_counter += 1

    #TODO implement so that buffering is actually implemented
    def write_bytes(self, bytecode):
        self.byte_buffer[0] = bytecode
        self.f.write(self.byte_buffer.tobytes())

    def simple_arithmetic_logic_encoding(self, instruction):
        operation = instruction.value[0]
        params = instruction.value[1]
        operation_code, condition, options = get_operation_values(operation, 3)
        bytecode = condition

        if "S" in options:
            bytecode |= 0x00100000
    
        if operation_code == "ADC":
            #TODO
            print("TODO")
        elif operation_code == "ADD":
            bytecode |= 0x00800000
            if "I" in options:
                bytecode |= 0x02000000
                destination_register, operand_register, imm = from_bi_register_imm(params)
                operand_register = operand_register << 16
                destination_register = destination_register << 12
                imm = int(imm, 0)
                bytecode |= operand_register | destination_register | imm
            else:
                #TODO
                print("TODO")
        elif operation_code == "AND":
            #TODO
            print("TODO")
        elif operation_code == "EOR":
            #TODO
            print("TODO")
        elif operation_code == "ORR":
            #TODO
            print("TODO")
        elif operation_code == "SBC":
            #TODO
            print("TODO")
        elif operation_code == "SUB":
            bytecode |= 0x00400000
            if "I" in options:
                bytecode |= 0x02000000
                destination_register, operand_register, imm = from_bi_register_imm(params)
                operand_register = operand_register << 16
                destination_register = destination_register << 12
                imm = int(imm, 0)
                bytecode |= operand_register | destination_register | imm
            else:
                #TODO
                print("TODO")

        return bytecode
    
    def condition_setter_operation_encoding(self, instruction):
        operation = instruction.value[0]
        operation_code, condition, options = get_operation_values(operation, 3)
        bytecode = condition
    
        if operation_code == "CMP":
            print("TODO")
            #TODO
    
        return bytecode
    
    def mul_operation_encoding(self, instruction):
        operation = instruction.value[0]
        operation_code, condition, options = get_operation_values(operation, 3)
        bytecode = None
    
        if operation_code == "MUL":
            print("TODO")
    
        return bytecode
    
    def branch_operation_encoding(self, instruction):
        operation = instruction.value[0]
        params = instruction.value[1]
        operation_code, condition, options = get_operation_values(operation, 1)
        bytecode = condition

        label = params.value
    
        if operation_code == "B":
            bytecode |= 0x0A000000
            if label in self.labels:
                label_address = self.labels[label]
                address = self.get_signed_relative_address(label_address, self.instruction_counter)
                bytecode |= address
            else:
                self.unresolved_label_refs[self.instruction_counter] = label
    
        return bytecode
    
    def mov_operation_encoding(self, instruction):
        operation = instruction.value[0]
        operation_code, condition, options = get_operation_values(operation, 4)
        bytecode = condition
        params = instruction.value[1]
        register = params.value[0].value << 12
    
        imm = params.value[1].value[2:6]
        hex_code = bytearray.fromhex(imm)
        imm4 = (hex_code[0] >> 4) << 16
        imm12 = ((hex_code[0] << 8) & 0x0f00) | hex_code[1]
    
        if operation_code == "MOVW":
            bytecode |= 0x03000000
        elif operation_code == "MOVT":
            bytecode |= 0x03400000
    
        bytecode |= imm4 
        bytecode |= imm12 
        bytecode |= register
    
        return bytecode
    
    def ldrstr_operation_encoding(self, instruction):
        operation = instruction.value[0]
        operation_code, condition, options = get_operation_values(operation, 3)
        bytecode = condition
    
        params = instruction.value[1]
        register1 = params.value[0].value << 12
        register2 = params.value[1].value[0].value << 16
        imm = int("0" + params.value[1].value[1].value[2:5])
    
        if operation_code == "STR":
            bytecode |= 0x04000000
        elif operation_code == "LDR":
            bytecode |= 0x04100000
        if "W" in options.upper():
            bytecode |= 0x00200000
    
        bytecode |= register1 | register2 | imm
    
        return bytecode
    
    def division_operation_encoding(self, instruction):
        operation = instruction.value[0]
        operation_code, condition, options = get_operation_values(operation, 3)
        bytecode = condition
    
        if operation_code == "UDIV":
            print("TODO")
        elif operation_code == "SDIV":
            print("TODO")
    
        return bytecode
