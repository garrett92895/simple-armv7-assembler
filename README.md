# simple-armv7-assembler
A basic assembler for the ARMv7-A ARM architecture which is part of the Cortex-A ARM family

This assembler is written in Python 3.5.0

The syntax is a shortened version of the official assembly for this architecture. It contains enough of the fundamental operations that most machine instructions can be encoded with it.

It currently does not support exchanges to Thumb or Jazelle instruction sets

Syntax
------
Where <> means optional
* <{Label}:> {OpCode} <{Condition}> <{Options}> {Params}
or
* {Label}: R{RegisterNum}
or
* {Label}: <0x>{Num}

`{Options}` can include "I" and/or "S" where "I" means immediate and "S" means that the instruction will update the condition flags based on the result

`{Params}` will vary based on the `{OpCode}`, I'm assuming that if you're writing assembly code you know the appropriate parameters for each operation

Decimal and hexadecimal are differentiated by prepending "0x" before hex values

If you omit the `{Condition}`, it will default to AL which is the execute always condition

Examples:

	MOVT R1, 0x3F20
	B 0xFFFFFF
	SUBIS R2,R1,0x3F20 /* SUB immediate with S bit set */
	BEQ 0xFFFFFB /* B OpCode with EQ condition. Condition met based off of condition flags (which were set in previous instruction) */

Resources
--------
This was tested on the Raspbery Pi 2 by installing Raspbian on the SD card and replacing the kernel7.img with my own machine instructions

ARMv7-A Reference Manual: http://liris.cnrs.fr/~mmrissa/lib/exe/fetch.php?media=armv7-a-r-manual.pdf
