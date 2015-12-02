from assembler.tokenizer import tokentype
from assembler.tokenizer import tokens
from . import operation_parser

class Parser:
    def __init__(self):
        self.token_stack = []
        self.labels = {}
        self.instruction_counter = 0

    def pop(self):
        if len(self.token_stack) > 0:
            token = self.token_stack.pop()
        else:
            token = tokens.Token(tokentype.NullType, "")
        return token

    def token_at(self, index):
        if index >= 0 and index < len(self.token_stack):
            token = self.token_stack[index]
        else:
            token = tokens.Token(tokentype.NullType, "")
        return token

    # Retrieves token in stack that is a "primitive" type (aka not label or operation)
    # e.x. token_stack = [ Label, AlphaNum, SpecialChar], calling unparsed_token_at(1)
    # would return the SpecialChar, unparsed_token_at(0) would return the AlphaNum, etc.
    def unparsed_token_at(self, index):
        count = 0
        ret_token = tokens.Token(tokentype.NullType, "")
        for token in self.token_stack:
            if tokentype.is_primitive(token.token_type):
                if count == index:
                    ret_token = token
                    break
                count += 1
        return ret_token

    def add_token(self, token):
        self.token_stack.append(token)

    def add_label(self, label_token):
        label_name = label_token.value
        
        if label_name not in self.labels:
            self.labels[label_name] = self.instruction_counter
        else:
            raise ValueError("Label: " + str(label_name) + " already exists in label table")

    def parse(self):
        instruction = None
        label = self.parse_label()
        operation = self.parse_operation()

        if operation:
            instruction = self.make_operation_instruction(label, operation)
        if instruction: 
            if label:
                self.add_label(label)
            self.token_stack.clear()
            self.instruction_counter += 1

        return instruction

    def parse_label(self):
        label_token = None
        if self.token_stack[0].token_type == tokentype.Label:
            label_token = self.token_stack[0]
        elif self.has_label():
            colon = self.token_stack.pop()
            label_name_token = self.token_stack.pop()
            label_token = tokens.Token(tokentype.Label, label_name_token.value)
            self.add_token(label_token)

        return label_token

    def has_label(self):
        first_token = self.token_at(0)
        second_token = self.token_at(1)
        return (first_token.token_type == tokentype.AlphaNum 
               and second_token.token_type == tokentype.SpecialChar
               and second_token.value == ":")

    def parse_operation(self):
        operation = self.parse_branch()
        if not operation:
            operation = self.parse_arithmetic_logic()
        if not operation:
            operation = self.parse_condition_setter()
        if not operation:
            operation = self.parse_multiplication()
        if not operation:
            operation = self.parse_mov()
        if not operation:
            operation = self.parse_ldrstr()
        if not operation:
            operation = self.parse_division()
        return operation

    # Checks validity from top of stack to bottom
    def parse_branch(self):
        top_token = self.pop()
        if top_token.token_type == tokentype.AlphaNum:
            second_token = self.pop() 
            if (second_token.token_type == tokentype.AlphaNum
                and operation_parser.valid_op(second_token.value, "branch", 1)):
                operation_token = tokens.Token.fromChildren(tokentype.BranchOperation, second_token, top_token)
                self.add_token(operation_token)
                return operation_token
            if second_token and second_token.token_type != tokentype.NullType:
                self.add_token(second_token)
        if top_token:
            self.add_token(top_token)

    def parse_arithmetic_logic(self):
        first_token = self.unparsed_token_at(0)
        if first_token.token_type == tokentype.AlphaNum and operation_parser.valid_op(first_token.value, "arithmetic_logic", 3):
            options = first_token.value[5:].upper()
            parameter_token = None
            if options == "I" or options == "IS":
                parameter_token = self.parse_bi_register_imm()
            elif options == "S" or options == "":
                parameter_token = self.parse_tri_register_imm()
           
            if parameter_token:
                self.pop()
                self.pop()
                operation_token = tokens.Token.fromChildren(tokentype.SimpleArithmeticLogicOperation, first_token, parameter_token)
                self.add_token(operation_token) 
                return operation_token

    def parse_condition_setter(self):
        first_token = self.unparsed_token_at(0)
        if first_token.token_type == tokentype.AlphaNum and operation_parser.valid_op(first_token.value, "condition_setter", 3):
            options = first_token.value[5:].upper()
            parameter_token = None
            if options == "I":
                parameter_token = self.parse_uni_register_imm()
            elif options == "":
                parameter_token = self.parse_bi_register_imm()
           
            if parameter_token:
                self.pop()
                self.pop()
                operation_token = tokens.Token.fromChildren(tokentype.ConditionSetterOperation, first_token, parameter_token)
                self.add_token(operation_token) 
                return operation_token

    def parse_multiplication(self):
        first_token = self.unparsed_token_at(0)
        if first_token.token_type == tokentype.AlphaNum and operation_parser.valid_op(first_token.value, "multiplication", 3):
            options = first_token.value[5:].upper()
            parameter_token = None
            if options == "S" or options == "":
                parameter_token = self.parse_tri_register()
           
            if parameter_token:
                self.pop()
                self.pop()
                operation_token = tokens.Token.fromChildren(tokentype.MulOperation, first_token, parameter_token)
                self.add_token(operation_token) 
                return operation_token

    def parse_ldrstr(self):
        first_token = self.unparsed_token_at(0)
        if first_token.token_type == tokentype.AlphaNum and operation_parser.valid_op(first_token.value, "ldrstr", 3):
            options = first_token.value[5:].upper()
            parameter_token = None
            if options == "I" or options == "W" or options == "IW":
                parameter_token = self.parse_bi_register_imm()
           
            if parameter_token:
                self.pop()
                self.pop()
                operation_token = tokens.Token.fromChildren(tokentype.LdrStrOperation, first_token, parameter_token)
                self.add_token(operation_token) 
                return operation_token

    def parse_mov(self):
        first_token = self.unparsed_token_at(0)
        if first_token.token_type == tokentype.AlphaNum and operation_parser.valid_op(first_token.value, "mov", 4):
            options = first_token.value[6:].upper()
            parameter_token = None
            if options == "":
                parameter_token = self.parse_uni_register_imm()
            if parameter_token:
                self.pop()
                self.pop()
                operation_token = tokens.Token.fromChildren(tokentype.MovOperation, first_token, parameter_token)
                self.add_token(operation_token) 
                return operation_token

    def parse_division(self):
        first_token = self.unparsed_token_at(0)
        if first_token.token_type == tokentype.AlphaNum and operation_parser.valid_op(first_token.value, "division", 4):
            options = first_token.value[6:].upper()
            parameter_token = None
            if options == "":
                parameter_token = self.parse_tri_register()
           
            if parameter_token:
                self.pop()
                self.pop()
                operation_token = tokens.Token.fromChildren(tokentype.DivOperation, first_token, parameter_token)
                self.add_token(operation_token) 
                return operation_token

    def parse_tri_register(self):
        register3 = self.parse_register()
        if register3:
            precomma2 = self.pop()
            comma2 = self.pop()
            if tokentype.is_comma(comma2):
                register2 = self.parse_register()
                if register2:
                    precomma1 = self.pop()
                    comma1 = self.pop()
                    if tokentype.is_comma(comma1):
                        register1 = self.parse_register()
                        if register1:
                            self.pop()
                            operation_token = tokens.Token.fromChildren(tokentype.TriRegister, register1, register2, register3)
                            self.add_token(operation_token)
                            return operation_token
                    if comma1 and comma1.token_type != tokentype.NullType:
                        self.add_token(comma1)
                    self.add_token(register2)
            if comma2 and comma2.token_type != tokentype.NullType:
                self.add_token(comma2)
            self.add_token(register3)

    def parse_tri_register_imm(self):
        bi_register_imm = self.parse_bi_register_imm()
        if bi_register_imm:
            self.pop()
            comma = self.pop()
            if tokentype.is_comma(comma):
                register = self.parse_register()
                if register:
                    self.pop()
                    operation_token = tokens.Token.fromChildren(tokentype.TriRegisterImm, register, bi_register_imm)
                    self.add_token(operation_token)
                    return operation_token
            else:
                self.add_token(comma)
                self.add_token(bi_register_imm)

    def parse_bi_register_imm(self):
        uni_register_imm = self.parse_uni_register_imm()
        if uni_register_imm:
            self.pop()
            comma = self.pop()
            if tokentype.is_comma(comma):
                register = self.parse_register()
                if register:
                    self.pop()
                    operation_token = tokens.Token.fromChildren(tokentype.BiRegisterImm, register, uni_register_imm)
                    self.add_token(operation_token)
                    return operation_token
            else:
                self.add_token(comma)
                self.add_token(uni_register_imm)

    def parse_uni_register_imm(self):
        hex = self.pop()
        if tokentype.is_hex(hex):
            comma = self.pop()
            if tokentype.is_comma(comma):
                register = self.parse_register()
                if register:
                    self.pop()
                    operation_token = tokens.Token.fromChildren(tokentype.UniRegisterImm, register, hex)
                    self.add_token(operation_token)
                    return operation_token
            else:
                self.add_token(comma)
                self.add_token(hex)
        if hex and hex.token_type != tokentype.NullType:
            self.add_token(hex)

    def parse_register(self):
        register_token = self.pop()
        if operation_parser.is_register(register_token):
            if register_token.token_type != tokentype.Register:
                register_token.token_type = tokentype.Register
                register_token.value = int(register_token.value[1:])
            self.add_token(register_token)
            return register_token
        self.add_token(register_token)

    def make_operation_instruction(self, label, operation):
        return tokens.Token.fromChildren(tokentype.Instruction, label, operation)
