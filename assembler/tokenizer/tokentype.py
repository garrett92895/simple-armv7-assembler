"""
Essentially an enum representing the types of tokens used by the tokenizer and parser
"""
NullType, AlphaNum, SpecialChar, Dec, Hex, Register, UniRegisterImm, BiRegisterImm, TriRegisterImm, BiRegister,\
TriRegister, SimpleArithmeticLogicOperation, ConditionSetterOperation, MulOperation, BranchOperation,\
MovOperation, LdrStrOperation, DivOperation, PushPopOperation, Label, Instruction = range(21)

types_name_first = {"NullType": 0,
                    "AlphaNum": 1,
                    "SpecialChar": 2,
                    "Dec": 3,
                    "Hex": 4,
                    "Register": 5,
                    "UniRegisterImm": 6,
                    "BiRegisterImm": 7,
                    "TriRegisterImm": 8,
                    "BiRegister": 9,
                    "TriRegister": 10,
                    "SimpleArithmeticLogicOperation": 11,
                    "ConditionSetterOperation": 12,
                    "MulOperation": 13,
                    "BranchOperation": 14,
                    "MovOperation": 15,
                    "LdrStrOperation": 16,
                    "DivOperation": 17,
                    "PushPopOperation": 18,
                    "Label": 19,
                    "Instruction": 20,
                    }

types = dict(zip(types_name_first.values(), types_name_first.keys()))


def is_primitive(token_num):
    return token_num in range(1, 5)


def is_comma(token):
    return token.token_type == SpecialChar and token.value == ","


def is_hex(token):
    return token.token_type == Hex
