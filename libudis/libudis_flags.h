#ifndef LIBUDIS_FLAGS_H
#define LIBUDIS_FLAGS_H

/* the flags must match omni8bit/disassembler/flags.py */

/* flags */
#define FLAG_BRANCH_TAKEN 1
#define FLAG_BRANCH_NOT_TAKEN 2
#define FLAG_REPEATED_BYTES 3
#define FLAG_REG_A 4
#define FLAG_REG_X 5
#define FLAG_REG_Y 6
#define FLAG_LOAD_A_FROM_MEMORY 7
#define FLAG_LOAD_X_FROM_MEMORY 8
#define FLAG_LOAD_Y_FROM_MEMORY 9
#define FLAG_MEMORY_ALTER 10
#define FLAG_MEMORY_READ_ALTER_A 11 
#define FLAG_PEEK_MEMORY 12
#define FLAG_PULL_A 13
#define FLAG_PULL_SR 14
#define FLAG_PUSH_A 15
#define FLAG_PUSH_SR 16
#define FLAG_RTI 17
#define FLAG_RTS 18
#define FLAG_STORE_A_IN_MEMORY 19
#define FLAG_STORE_X_IN_MEMORY 20
#define FLAG_STORE_Y_IN_MEMORY 21
#define FLAG_JMP_INDIRECT 22
#define FLAG_TARGET_ADDR 64
#define FLAG_REG_SR 128

#define FLAG_RESULT_MASK 0x3f

/* disassembler types */
#define DISASM_DATA 0
#define DISASM_6502 10
#define DISASM_6502UNDOC 11
#define DISASM_65816 12
#define DISASM_65C02 13
#define DISASM_6800 14
#define DISASM_6809 15
#define DISASM_6811 16
#define DISASM_8051 17
#define DISASM_8080 18
#define DISASM_Z80 19
#define DISASM_ANTIC_DL 30
#define DISASM_JUMPMAN_HARVEST 31
#define DISASM_JUMPMAN_LEVEL 32

/* types 128-191 are for history entries that have result entries */
#define DISASM_6502_HISTORY 128
#define DISASM_6502_HISTORY_RESULT 129
#define DISASM_ATARI800_HISTORY 130
#define DISASM_ATARI800_HISTORY_RESULT 131
#define DISASM_NEXT_INSTRUCTION 132
#define DISASM_NEXT_INSTRUCTION_RESULT 133

/* types 192-254 don't have results */
#define DISASM_FRAME_START 192
#define DISASM_FRAME_END 193
#define DISASM_ATARI800_VBI_START 194
#define DISASM_ATARI800_VBI_END 195
#define DISASM_ATARI800_DLI_START 196
#define DISASM_ATARI800_DLI_END 197

#define DISASM_BREAKPOINT 253
#define DISASM_USER_DEFINED 254
#define DISASM_UNKNOWN 255


#endif /* LIBUDIS_FLAGS_H */
