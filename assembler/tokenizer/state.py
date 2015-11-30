from . import tokens
from . import tokentype

class State:
    def __init__(self, eval_method):
        self.tokens = []
        self.token_builder_string = ""
        self.eval_method = eval_method

    @classmethod
    def fromState(cls, state, eval_method):
        new_state = State(eval_method)
        new_state.tokens = state.tokens
        new_state.token_builder_string = state.token_builder_string
        return new_state

    def evaluate(self, char):
        return self.eval_method(self, char)

    def add_char(self, char):
        self.token_builder_string += char

    def add_token(self, token):
        self.tokens.append(token)
        self.token_builder_string = ""

    def has_tokens(self):
        return len(self.tokens) != 0

    def next_token(self):
        return self.tokens.pop()

def change_state(state, new_state_name):
    eval_method = None

    if new_state_name == "a":
        eval_method = a_state_eval
    elif new_state_name == "b":
        eval_method = b_state_eval
    elif new_state_name == "c":
        eval_method = c_state_eval
    elif new_state_name == "d":
        eval_method = d_state_eval
    elif new_state_name == "e":
        eval_method = e_state_eval
    elif new_state_name == "f":
        eval_method = f_state_eval
    elif new_state_name == "g":
        eval_method = g_state_eval
    elif new_state_name == "h":
        eval_method = h_state_eval
    elif new_state_name == "i":
        eval_method = i_state_eval
    else:
        raise ValueError("State " + str(new_state_name) + " does not exist")

    return state.fromState(state, eval_method)

def append_and_change_state(state, char, new_state_name):
    state.token_builder_string += char
    return change_state(state, new_state_name)

def throw(state, message):
    raise ValueError(message)

def a_state_eval(state, char):
    if char.isspace():
        return state
    elif char.isalpha():
        return append_and_change_state(state, char, "b")
    elif char == "0":
        return append_and_change_state(state, char, "c")
    elif char.isdigit():
        return append_and_change_state(state, char, "e")
    elif char == "/":
        return change_state(state, "g")
    elif char == "*":
        throw(state, "\"*\" not acceptable here")
    else:
        return append_and_change_state(state, char, "f")

def b_state_eval(state, char):
    if char.isspace():
        token = tokens.Token(tokentype.AlphaNum, state.token_builder_string)
        state.add_token(token)
        return change_state(state, "a")
    elif char.isalpha():
        state.add_char(char)
        return state
    elif char == "0":
        state.add_char(char)
        return state
    elif char.isdigit():
        state.add_char(char)
        return state
    elif char == "/":
        token = tokens.Token(tokentype.AlphaNum, state.token_builder_string)
        state.add_token(token)
        return change_state(state, "g")
    elif char == "*":
        throw(state, "\"*\" not acceptable here")
    else:
        token = tokens.Token(tokentype.AlphaNum, state.token_builder_string)
        state.add_token(token)
        state.add_char(char)
        return change_state(state, "f")

def c_state_eval(state, char):
    if char.isspace():
        token = tokens.Token(tokentype.Dec, state.token_builder_string)
        state.add_token(token)
        return change_state(state, "a")
    elif char == "x":
        return append_and_change_state(state, char, "d")
    elif char.isalpha():
        throw(state, "Cannot add alpha after num in non-hex context")
    elif char == "0":
        return append_and_change_state(state, char, "e")
    elif char.isdigit():
        return append_and_change_state(state, char, "e")
    elif char == "/":
        token = tokens.Token(tokentype.Dec, state.token_builder_string)
        state.add_token(token)
        return change_state(state, "g")
    elif char == "*":
        throw(state, "\"*\" not acceptable here")
    else:
        token = tokens.Token(tokentype.Dec, state.token_builder_string)
        state.add_token(token)
        state.add_char(char)
        return change_state(state, "f")
        
def d_state_eval(state, char):
    if char.isspace():
        token = tokens.Token(tokentype.Hex, state.token_builder_string)
        state.add_token(token)
        return change_state(state, "a")
    elif char.isalpha():
        state.add_char(char)
        return state
    elif char.isdigit():
        state.add_char(char)
        return state
    elif char == "/":
        token = tokens.Token(tokentype.Hex, state.token_builder_string)
        state.add_token(token)
        return change_state(state, "g")
    elif char == "*":
        throw(state, "\"*\" not acceptable here")
    else:
        token = tokens.Token(tokentype.Hex, state.token_builder_string)
        state.add_token(token)
        state.add_char(char)
        return change_state(state, "f")

def e_state_eval(state, char):
    if char.isspace():
        token = tokens.Token(tokentype.Dec, state.token_builder_string)
        state.add_token(token)
        return change_state(state, "a")
    elif char.isalpha():
        throw(state, "Cannot add alpha after num in non-hex context")
    elif char.isdigit():
        state.add_char(char)
        return state
    elif char == "/":
        token = tokens.Token(tokentype.Dec, state.token_builder_string)
        state.add_token(token)
        return change_state(state, "g")
    elif char == "*":
        throw(state, "\"*\" not acceptable here")
    else:
        token = tokens.Token(tokentype.Dec, state.token_builder_string)
        state.add_token(token)
        state.add_char(char)
        return change_state(state, "f")

def f_state_eval(state, char):
    if char.isspace():
        token = tokens.Token(tokentype.SpecialChar, state.token_builder_string)
        state.add_token(token)
        return change_state(state, "a")
    elif char.isalpha():
        token = tokens.Token(tokentype.SpecialChar, state.token_builder_string)
        state.add_token(token)
        state.add_char(char)
        return change_state(state, "b")
    elif char == "0":
        token = tokens.Token(tokentype.SpecialChar, state.token_builder_string)
        state.add_token(token)
        state.add_char(char)
        return change_state(state, "c")
    elif char.isdigit():
        token = tokens.Token(tokentype.SpecialChar, state.token_builder_string)
        state.add_token(token)
        state.add_char(char)
        return change_state(state, "e")
    elif char == "/":
        token = tokens.Token(tokentype.SpecialChar, state.token_builder_string)
        state.add_token(token)
        return change_state(state, "g")
    elif char == "*":
        throw(state, "\"*\" not acceptable here")
    else:
        token = tokens.Token(tokentype.SpecialChar, state.token_builder_string)
        state.add_token(token)
        state.add_char(char)
        return change_state(state, "f")

def g_state_eval(state, char):
    if char == "*":
        return change_state(state, "h")
    else:
        throw(state, "Comments require a \"*\" after a \\")

def h_state_eval(state, char):
    if char == "*":
        return change_state(state, "i")
    else:
        return state

def i_state_eval(state, char):
    if char == "/":
        return change_state(state, "a")
    elif char == "*":
        return state
    else:
        return change_state(state, "h")

a_state_method = a_state_eval
b_state_method = b_state_eval
c_state_method = c_state_eval
d_state_method = d_state_eval
e_state_method = e_state_eval
f_state_method = f_state_eval
g_state_method = g_state_eval
h_state_method = h_state_eval
i_state_method = i_state_eval

def initial_state():
    return State(a_state_method)
