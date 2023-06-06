In original Type-B encoding, $Imm can be max 7 bits. 5 bits of
 opcode, 3 bit for register num and 1 unused bit.

For supporting float arithmetic in 'mov' command, we had to 
use modified Type-B encoding. Now $Imm is max 8 bits. 5 bits
of opcode, 3 bits for register and 8 bits for $Imm

