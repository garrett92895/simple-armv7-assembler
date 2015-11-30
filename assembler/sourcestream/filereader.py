"""
Reads from a file like a stream
"""
import re

class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.f = open(self.file_path, "r")
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.f.close()

    def next_char(self):
        return self.f.read(1)

    def next_chars(self, num_chars):
        return self.f.read(num_chars)

    def next_until_delimiter(self, *delimiters):
        chars = []
        current_char = self.nextChar()

        if current_char is not '':
            keep_reading = True
            while keep_reading:
                chars.append(current_char)
                keep_reading = any(map(lambda d : re.match(d, current_char), delimiters))
                current_char = self.nextChar()
            
        else:
            chars.append('')

        return ''.join(c for c in chars)
