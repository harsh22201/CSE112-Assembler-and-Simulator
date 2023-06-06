-----------------------------------------------------------------------------
|  Opcode  |  Instrucntion  |      Semantics      |    Syntax      |  Type   |
-----------------------------------------------------------------------------
|          |                |                     |                |         |
| 10011    |  Set           |  Sets the $Imm'th   | set reg1 $Imm  |  B      |
|          |                |  bit of reg1. Where |                |         |
|          |                |   $Imm is a 4 bit   |                |         |
|          |                |   value             |                |         |
-----------------------------------------------------------------------------
|          |                |                     |                |         |
| 10100    |  Clear         |  Clears the $Imm'th | clr reg1 $Imm  |  B      |
|          |                |  bit of reg1. Where |                |         |
|          |                |   $Imm is a 4 bit   |                |         |
|          |                |   value             |                |         |
-----------------------------------------------------------------------------
|          |                |                     |                |         |
| 10101    |  Toggle        | Toggles the $Imm'th | tgl reg1 $Imm  |  B      |
|          |                |  bit of reg1. Where |                |         |
|          |                |   $Imm is a 4 bit   |                |         |
|          |                |   value             |                |         |
-----------------------------------------------------------------------------
|          |                |                     |                |         |
| 10110    |  Rotate left   | Left rotates reg1 by| rol reg1 $Imm  |  B      |
|          |                | $Imm. Where $Imm    |                |         |
|          |                |   is a 4 bit        |                |         |
|          |                |   value             |                |         |
-----------------------------------------------------------------------------
|          |                |                     |                |         |
| 10111    |  Rotate Right  |Right rotates reg1 by| ror reg1 $Imm  |  B      |
|          |                | $Imm. Where $Imm    |                |         |
|          |                |   is a 4 bit        |                |         |
|          |                |   value             |                |         |
-----------------------------------------------------------------------------

Note about ROL and ROR: 
- Rotation is circular. As if MSB and LSB are connected through a circular ring
- E.g. reg1 = 0b0000000001111111. ROL by 3 would make the new value of 
  reg1=0b0000001111111000
- E.g. reg1 = 0b0000000001111111. ROR by 4 would make the new value of 
  reg1=0b1111000000000111 

