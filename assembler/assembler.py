#!/usr/bin/python3
"""
Encodes simple assembly into ARMv7-A machine code
"""
import sys
import sourcestream.filereader
import tokenizer
import parser
import generator

if len(sys.argv) <= 2:
    raise ValueError('Need to specify and source code and output file')

source_file = sys.argv[1]
destination_file = sys.argv[2]

with sourcestream.filereader.fromFilePath(source_file) as source, generator.fromFilePath(destination_file) as sink:
    parser.fromGenerator(sink)
    tokenizer = tokenizer.Tokenizer(source, sink)

    #While source.nextChar() not at EOF
