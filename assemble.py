#!/usr/bin/python3
"""
Encodes simple assembly into ARMv7-A machine code
"""
import sys

import assembler.sourcestream.filereader as filereader
import assembler.tokenizer as tokenizer
import assembler.parser as parser
import assembler.parser.generator as generator

if len(sys.argv) <= 1:
    raise ValueError('Need to specify and source code and output file')

source_file = sys.argv[1]
destination_file = sys.argv[2]

with filereader.FileReader(source_file) as source, generator.Generator(destination_file) as sink:
    the_parser = parser.Parser()
    the_tokenizer = tokenizer.Tokenizer(source)

    next_token = the_tokenizer.get_next_token()
    while(next_token):
        the_parser.add_token(next_token)
        instruction = the_parser.parse()

        if instruction:
            sink.write_instruction(instruction)
        next_token = the_tokenizer.get_next_token()

    #get label table
    #resolve label and overwrite addresses into file
