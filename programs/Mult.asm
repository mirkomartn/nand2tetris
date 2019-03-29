// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// PSEUDO CODE:
// 
//  i = R1;
//  R2 = 0;
//  
//  while (i > 0) {
//   R2 += R0
//   i -= 1
//  }
//  
//  END 
//  
//
// set product to 0

@R2 
M = 0

// if any of the products is 0, jump to END
@R0
D = M
@END
D; JEQ
@R1
D = M
@END
D; JEQ

// save the i parameter separately, to keep the R1 and R0 intact
@R1
D = M
@i 
M = D

(LOOP)
@R0
D = M
@R2
M = M + D
@i
M = M - 1
// if i > 0, jump to the top of the loop
@i
D = M
@LOOP
D;JGT

(END)
@END
0;JMP
