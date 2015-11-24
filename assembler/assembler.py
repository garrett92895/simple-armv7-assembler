#!/usr/bin/python3
"""
Encodes simple assembly into ARMv7-A machine code
"""
import sys

import sourcestream.filereader as filereader
import tokenizer
import parser
import parser.generator as generator

if len(sys.argv) <= 2:
    raise ValueError('Need to specify and source code and output file')

source_file = sys.argv[1]
destination_file = sys.argv[2]

with filereader(source_file) as source, generator(destination_file) as sink:
    the_parser = parser.fromGenerator(sink)
    the_tokenizer = tokenizer.Tokenizer(source)

    next_token = the_tokenizer.get_next_token()
    while(next_token):
        the_parser.add_token(next_token)
        the_parser.parse()
        next_token = the_tokenizer.get_next_token()
