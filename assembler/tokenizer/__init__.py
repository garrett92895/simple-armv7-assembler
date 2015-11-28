"""

"""
import tokens

class Tokenizer:
    def __init__(self, source):
        self.source_stream = source
        self.state = tokens.initial_state()

    def get_next_token(self):
        while not self.state.has_tokens():
            char = self.source_stream.next_char()
            self.state = self.state.evaluate(char)
        next_token = self.state.next_token()
        if next_token.value:
            return next_token
