"""
Essentially an enum representing the types of tokens used by the tokenizer and parser
"""
NullType, AlphaNum, SpecialChar, Dec, Hex, Register, UniRegisterImm, BiRegisterImm, TriRegisterImm, TriRegister, SimpleArithmeticLogicOperation, ConditionSetterOperation, MulOperation, BranchOperation, MovOperation, LdrStrOperation, DivOperation, Label, Instruction = range(19)

types_name_first = { "NullType": 0,
        "AlphaNum": 1,
        "SpecialChar": 2,
        "Dec": 3,
        "Hex": 4,
        "Register": 5,
        "UniRegisterImm": 6,
        "BiRegisterImm": 7,
        "TriRegisterImm": 8,
        "TriRegister": 9,
        "SimpleArithmeticLogicOperation": 10,
        "ConditionSetterOperation": 11,
        "MulOperation": 12,
        "BranchOperation": 13,
        "MovOperation": 14,
        "LdrStrOperation": 15,
        "DivOperation": 16,
        "Label": 17,
        "Instruction": 18,
}

types = dict(zip(types_name_first.values(), types_name_first.keys()))

def is_primitive(token_num):
    return token_num in range(1, 5)

def is_comma(token):
    return token.token_type == SpecialChar and token.value == ","

def is_hex(token):
    return token.token_type == Hex
