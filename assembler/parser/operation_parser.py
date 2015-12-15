"""
Set of helper methods for parsing operations
"""
from assembler.tokenizer import tokentype

conditions = set(["AL", "EQ", "NE", "LT", "LE", "GT", "GE"])
op_sets = {"condition_setter": set(["CMP"]),
           "arithmetic_logic": set(["ADC", "ADD", "AND", "EOR", "ORR", "SBC", "SUB"]),
           "multiplication": set(["MUL"]),
           "branch": set(["B", "BL"]),
           "mov": set(["MOVW", "MOVT", "MOV"]),
           "ldrstr": set(["LDR", "STR"]),
           "division": set(["SDIV", "UDIV"]),
           "push": set(["PUSH"]),
           "pop": set(["POP"])
           }

debug = False


def valid_condition(condition_string, index1, index2):
    condition = condition_string[index1:index2].upper()
    return condition in conditions


def valid_op(op_string, op_set_name, op_upper):
    op = op_string[:op_upper]
    if debug:
        print("\t\top: " + op)
        print("\t\tset: " + str(op_sets[op_set_name]))
        print("\t\tvalid_condition: " + str(valid_condition(op_string, op_upper, op_upper + 2)))
    return op.upper() in op_sets[op_set_name] and valid_condition(op_string, op_upper, op_upper + 2)


def is_register(register_token):
    if register_token.token_type == tokentype.Register:
        return True
    elif register_token.token_type == tokentype.AlphaNum:
        register_token_string = register_token.value
        register_letter = register_token_string[:1]
        register_value = register_token_string[1:]
        return register_letter.lower() == "r" and register_value.isdigit() and int(register_value) < 16 and int(
            register_value) >= 0
    else:
        return False
