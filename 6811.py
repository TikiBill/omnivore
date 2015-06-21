##########################################################################
#
# Processor specific code

# CPU = "6811"
# Description = "FreeScale 68HC11 8-bit microcontroller."
# DataWidth = 8 # 8-bit data
# AddressWidth = 16 # 16-bit addresses

# Maximum length of an instruction (for formatting purposes)
maxLength = 5;

# Leadin bytes for multbyte instructions
leadInBytes = [0x18, 0x1a, 0xcd]

# Addressing mode table
addressModeTable = {
"inherent"   : "",
"immediate"  : "#${0:02X}",
"immediatex" : "#${0:02X}{1:02X}",
"direct"     : "${0:02X}",
"direct2"    : "${0:02X} ${1:02X}",
"direct3"    : "${0:02X} ${1:02X} ${2:02X}",
"extended"   : "${0:02X}{1:02X}",
"indexedx"   : "${0:02X},x",
"indexedx2"  : "${0:02X},x ${1:02X}",
"indexedx3"  : "${0:02X},x ${1:02X} ${2:02X}",
"indexedy"   : "${0:02X},y",
"indexedy2"  : "${0:02X},y ${1:02X}",
"indexedy3"  : "${0:02X},y ${1:02X} ${2:02X}",
"relative"   : "${0:04X}",
}

# Op Code Table
# Key is numeric opcode (possibly multiple bytes)
# Value is a list:
#   # bytes
#   mnemonic
#   addressing mode.
#   flags (e.g. pcr)
opcodeTable = {

0x1b   :  [ 1, "aba",  "inherent"        ],
0x3a   :  [ 1, "abx",  "inherent"        ],
0x183a :  [ 2, "aby",  "inherent"        ],
0x89   :  [ 2, "adca", "immediate"       ],
0x99   :  [ 2, "adca", "direct"          ],
0xb9   :  [ 3, "adca", "extended"        ],
0xa9   :  [ 2, "adca", "indexedx"        ],
0x18a9 :  [ 3, "adca", "indexedy"        ],
0xc9   :  [ 2, "adcb", "immediate"       ],
0xd9   :  [ 2, "adcb", "direct"          ],
0xf9   :  [ 3, "adcb", "extended"        ],
0xe9   :  [ 2, "adcb", "indexedx"        ],
0x18e9 :  [ 3, "adcb", "indexedy"        ],
0x8b   :  [ 2, "adda", "immediate"       ],
0x9b   :  [ 2, "adda", "direct"          ],
0xbb   :  [ 3, "adda", "extended"        ],
0xab   :  [ 2, "adda", "indexedx"        ],
0x18ab :  [ 3, "adda", "indexedy"        ],
0xcb   :  [ 2, "addb", "immediate"       ],
0xdb   :  [ 2, "addb", "direct"          ],
0xfb   :  [ 3, "addb", "extended"        ],
0xeb   :  [ 2, "addb", "indexedx"        ],
0x18eb :  [ 3, "addb", "indexedy"        ],
0xc3   :  [ 3, "addd", "immediatex"      ],
0xd3   :  [ 2, "addd", "direct"          ],
0xf3   :  [ 3, "addd", "extended"        ],
0xe3   :  [ 2, "addd", "indexedx"        ],
0x18e3 :  [ 3, "addd", "indexedy"        ],
0x84   :  [ 2, "anda", "immediate"       ],
0x94   :  [ 2, "anda", "direct"          ],
0xb4   :  [ 3, "anda", "extended"        ],
0xa4   :  [ 2, "anda", "indexedx"        ],
0x18a4 :  [ 3, "anda", "indexedy"        ],
0xc4   :  [ 2, "andb", "immediate"       ],
0xd4   :  [ 2, "andb", "direct"          ],
0xf4   :  [ 3, "andb", "extended"        ],
0xe4   :  [ 2, "andb", "indexedx"        ],
0x18e4 :  [ 3, "andb", "indexedy"        ],
0x78   :  [ 3, "asl",  "extended"        ],
0x68   :  [ 2, "asl",  "indexedx"        ],
0x1868 :  [ 3, "asl",  "indexedy"        ],
0x48   :  [ 1, "asla", "inherent"        ],
0x58   :  [ 1, "aslb", "inherent"        ],
0x05   :  [ 1, "asld", "inherent"        ],
0x77   :  [ 3, "asr",  "extended"        ],
0x67   :  [ 2, "asr",  "indexedx"        ],
0x1867 :  [ 3, "asr",  "indexedy"        ],
0x47   :  [ 1, "asra", "inherent"        ],
0x57   :  [ 1, "asrb", "inherent"        ],
0x24   :  [ 2, "bcc",  "relative", pcr   ],
0x15   :  [ 3, "bclr", "direct2",        ],
0x1d   :  [ 3, "bclr", "indexedx2",      ],
0x181d :  [ 4, "bclr", "indexedy2",      ],
0x25   :  [ 2, "bcs",  "relative", pcr   ],
0x27   :  [ 2, "beq",  "relative", pcr   ],
0x2c   :  [ 2, "bge",  "relative", pcr   ],
0x2e   :  [ 2, "bgt",  "relative", pcr   ],
0x22   :  [ 2, "bhi",  "relative", pcr   ],
0x24   :  [ 2, "bhs",  "relative", pcr   ],
0x85   :  [ 2, "bita", "immediate"       ],
0x95   :  [ 2, "bita", "direct"          ],
0xb5   :  [ 3, "bita", "extended"        ],
0xa5   :  [ 2, "bita", "indexedx"        ],
0x18a5 :  [ 3, "bita", "indexedy"        ],
0xc5   :  [ 2, "bitb", "immediate"       ],
0xd5   :  [ 2, "bitb", "direct"          ],
0xf5   :  [ 3, "bitb", "extended"        ],
0xe5   :  [ 2, "bitb", "indexedx"        ],
0x18e5 :  [ 3, "bitb", "indexedy"        ],
0x2f   :  [ 2, "ble",  "relative", pcr   ],
0x25   :  [ 2, "blo",  "relative", pcr   ],
0x23   :  [ 2, "bls",  "relative", pcr   ],
0x2d   :  [ 2, "blt",  "relative", pcr   ],
0x2b   :  [ 2, "bmi",  "relative", pcr   ],
0x26   :  [ 2, "bne",  "relative", pcr   ],
0x2a   :  [ 2, "bpl",  "relative", pcr   ],
0x20   :  [ 2, "bra",  "relative", pcr   ],
0x13   :  [ 4, "brclr", "direct3",       ],
0x1f   :  [ 4, "brclr", "indexedx3",     ],
0x181f :  [ 5, "brclr", "indexedy3",     ],
0x21   :  [ 2, "brn",  "relative", pcr   ],
0x12   :  [ 4, "brset", "direct3",       ],
0x1e   :  [ 4, "brset", "indexedx3",     ],
0x181e :  [ 5, "brset", "indexedy3",     ],
0x14   :  [ 3, "bset", "direct2",        ],
0x1c   :  [ 3, "bset", "indexedx2",      ],
0x181c :  [ 4, "bset", "indexedy2",      ],
0x8d   :  [ 2, "bsr",  "relative", pcr   ],
0x28   :  [ 2, "bvc",  "relative", pcr   ],
0x29   :  [ 2, "bvs",  "relative", pcr   ],
0x11   :  [ 1, "cba",  "inherent"        ],
0x0c   :  [ 1, "clc",  "inherent"        ],
0x0e   :  [ 1, "cli",  "inherent"        ],
0x7f   :  [ 3, "clr",  "extended"        ],
0x6f   :  [ 2, "clr",  "indexedx"        ],
0x187f :  [ 3, "clr",  "indexedy"        ],
0x4f   :  [ 1, "clra", "inherent"        ],
0x5f   :  [ 1, "clrb", "inherent"        ],
0x0a   :  [ 1, "clv",  "inherent"        ],
0x81   :  [ 2, "cmpa", "immediate"       ],
0x91   :  [ 2, "cmpa", "direct"          ],
0xb1   :  [ 3, "cmpa", "extended"        ],
0xa1   :  [ 2, "cmpa", "indexedx"        ],
0x18a1 :  [ 3, "cmpa", "indexedy"        ],
0xc1   :  [ 2, "cmpb", "immediate"       ],
0xd1   :  [ 2, "cmpb", "direct"          ],
0xf1   :  [ 3, "cmpb", "extended"        ],
0xe1   :  [ 2, "cmpb", "indexedx"        ],
0x18e1 :  [ 3, "cmpb", "indexedy"        ],
0x73   :  [ 3, "com",  "extended"        ],
0x63   :  [ 2, "com",  "indexedx"        ],
0x1863 :  [ 3, "com",  "indexedy"        ],
0x43   :  [ 1, "coma", "inherent"        ],
0x53   :  [ 1, "comb", "inherent"        ],
0x1a83 :  [ 4, "cpd",  "immediatex"      ],
0x1a93 :  [ 3, "cpd",  "direct"          ],
0x1ab3 :  [ 4, "cpd",  "extended"        ],
0x1aa3 :  [ 3, "cpd",  "indexedx"        ],
0xcda3 :  [ 3, "cpd",  "indexedy"        ],
0x8c   :  [ 3, "cpx",  "immediatex"      ],
0x9c   :  [ 2, "cpx",  "direct"          ],
0xbc   :  [ 3, "cpx",  "extended"        ],
0xac   :  [ 2, "cpx",  "indexedx"        ],
0xcdac :  [ 3, "cpx",  "indexedy"        ],
0x188c :  [ 4, "cpy",  "immediatex"      ],
0x189c :  [ 3, "cpy",  "direct"          ],
0x18bc :  [ 4, "cpy",  "extended"        ],
0x1aac :  [ 3, "cpy",  "indexedx"        ],
0x18ac :  [ 3, "cpy",  "indexedy"        ],
0x19   :  [ 1, "daa",  "inherent"        ],
0x7a   :  [ 3, "dec",  "extended"        ],
0x6a   :  [ 2, "dec",  "indexedx"        ],
0x186a :  [ 3, "dec",  "indexedy"        ],
0x4a   :  [ 1, "deca", "inherent"        ],
0x5a   :  [ 1, "decb", "inherent"        ],
0x34   :  [ 1, "des",  "inherent"        ],
0x09   :  [ 1, "dex",  "inherent"        ],
0x1809 :  [ 2, "dey",  "inherent"        ],
0x88   :  [ 2, "eora", "immediate"       ],
0x98   :  [ 2, "eora", "direct"          ],
0xb8   :  [ 3, "eora", "extended"        ],
0xa8   :  [ 2, "eora", "indexedx"        ],
0x18a8 :  [ 3, "eora", "indexedy"        ],
0xc8   :  [ 2, "eorb", "immediate"       ],
0xd8   :  [ 2, "eorb", "direct"          ],
0xf8   :  [ 3, "eorb", "extended"        ],
0xe8   :  [ 2, "eorb", "indexedx"        ],
0x18e8 :  [ 3, "eorb", "indexedy"        ],
0x03   :  [ 1, "fdiv", "inherent"        ],
0x02   :  [ 1, "idiv", "inherent"        ],
0x7c   :  [ 3, "inc",  "extended"        ],
0x6c   :  [ 2, "inc",  "indexedx"        ],
0x186c :  [ 3, "inc",  "indexedy"        ],
0x4c   :  [ 1, "inca", "inherent"        ],
0x5c   :  [ 1, "incb", "inherent"        ],
0x31   :  [ 1, "ins",  "inherent"        ],
0x08   :  [ 1, "inx",  "inherent"        ],
0x1808 :  [ 2, "iny",  "inherent"        ],
0x7e   :  [ 3, "jmp",  "extended"        ],
0x6e   :  [ 2, "jmp",  "indexedx"        ],
0x186e :  [ 3, "jmp",  "indexedy"        ],
0x9d   :  [ 2, "jsr",  "direct"          ],
0xbd   :  [ 3, "jsr",  "extended"        ],
0xad   :  [ 2, "jsr",  "indexedx"        ],
0x18ad :  [ 3, "jsr",  "indexedy"        ],
0x86   :  [ 2, "ldaa", "immediate"       ],
0x96   :  [ 2, "ldaa", "direct"          ],
0xb6   :  [ 3, "ldaa", "extended"        ],
0xa6   :  [ 2, "ldaa", "indexedx"        ],
0x18a6 :  [ 3, "ldaa", "indexedy"        ],
0xc6   :  [ 2, "ldab", "immediate"       ],
0xd6   :  [ 2, "ldab", "direct"          ],
0xf6   :  [ 3, "ldab", "extended"        ],
0xe6   :  [ 2, "ldab", "indexedx"        ],
0x18e6 :  [ 3, "ldab", "indexedy"        ],
0xcc   :  [ 3, "ldd",  "immediatex"      ],
0xdc   :  [ 2, "ldd",  "direct"          ],
0xfc   :  [ 3, "ldd",  "extended"        ],
0xec   :  [ 2, "ldd",  "indexedx"        ],
0x18ec :  [ 3, "ldd",  "indexedy"        ],
0x8e   :  [ 3, "lds",  "immediatex"      ],
0x9e   :  [ 2, "lds",  "direct"          ],
0xbe   :  [ 3, "lds",  "extended"        ],
0xae   :  [ 2, "lds",  "indexedx"        ],
0x18ae :  [ 3, "lds",  "indexedy"        ],
0xce   :  [ 3, "ldx",  "immediatex"      ],
0xde   :  [ 2, "ldx",  "direct"          ],
0xfe   :  [ 3, "ldx",  "extended"        ],
0xee   :  [ 2, "ldx",  "indexedx"        ],
0xcdee :  [ 3, "ldx",  "indexedy"        ],
0x18ce :  [ 4, "ldy",  "immediatex"      ],
0x18de :  [ 3, "ldy",  "direct"          ],
0x18fe :  [ 4, "ldy",  "extended"        ],
0x1aee :  [ 3, "ldy",  "indexedx"        ],
0x18ee :  [ 3, "ldy",  "indexedy"        ],
0x78   :  [ 3, "lsl",  "extended"        ],
0x68   :  [ 2, "lsl",  "indexedx"        ],
0x1868 :  [ 3, "lsl",  "indexedy"        ],
0x48   :  [ 1, "lsla", "inherent"        ],
0x58   :  [ 1, "lslb", "inherent"        ],
0x05   :  [ 1, "lsld", "inherent"        ],
0x74   :  [ 3, "lsr",  "extended"        ],
0x64   :  [ 2, "lsr",  "indexedx"        ],
0x1864 :  [ 3, "lsr",  "indexedy"        ],
0x44   :  [ 1, "lsra", "inherent"        ],
0x54   :  [ 1, "lsrb", "inherent"        ],
0x04   :  [ 1, "lsrd", "inherent"        ],
0x3d   :  [ 1, "mul",  "inherent"        ],
0x70   :  [ 3, "neg",  "extended"        ],
0x60   :  [ 2, "neg",  "indexedx"        ],
0x1860 :  [ 3, "neg",  "indexedy"        ],
0x40   :  [ 3, "nega", "inherent"        ],
0x50   :  [ 3, "negb", "inherent"        ],
0x01   :  [ 1, "nop",  "inherent"        ],
0x8a   :  [ 2, "oraa", "immediate"       ],
0x9a   :  [ 2, "oraa", "direct"          ],
0xba   :  [ 3, "oraa", "extended"        ],
0xaa   :  [ 2, "oraa", "indexedx"        ],
0x18aa :  [ 3, "oraa", "indexedy"        ],
0xca   :  [ 2, "orab", "immediate"       ],
0xda   :  [ 2, "orab", "direct"          ],
0xfa   :  [ 3, "orab", "extended"        ],
0xea   :  [ 2, "orab", "indexedx"        ],
0x18ea :  [ 3, "orab", "indexedy"        ],
0x36   :  [ 1, "psha", "inherent"        ],
0x37   :  [ 1, "pshb", "inherent"        ],
0x3c   :  [ 1, "pshx", "inherent"        ],
0x183c :  [ 2, "pshy", "inherent"        ],
0x32   :  [ 1, "pula", "inherent"        ],
0x33   :  [ 1, "pulb", "inherent"        ],
0x38   :  [ 1, "pulx", "inherent"        ],
0x1838 :  [ 2, "puly", "inherent"        ],
0x79   :  [ 3, "rol",  "extended"        ],
0x69   :  [ 2, "rol",  "indexedx"        ],
0x1869 :  [ 3, "rol",  "indexedy"        ],
0x49   :  [ 1, "rola", "inherent"        ],
0x59   :  [ 1, "rolb", "inherent"        ],
0x76   :  [ 3, "ror",  "extended"        ],
0x66   :  [ 2, "ror",  "indexedx"        ],
0x1866 :  [ 3, "ror",  "indexedy"        ],
0x46   :  [ 1, "rora", "inherent"        ],
0x55   :  [ 1, "rorb", "inherent"        ],
0x3b   :  [ 1, "rti",  "inherent"        ],
0x39   :  [ 1, "rts",  "inherent"        ],
0x10   :  [ 1, "sba",  "inherent"        ],
0x82   :  [ 2, "sbca", "immediate"       ],
0x92   :  [ 2, "sbca", "direct"          ],
0xb2   :  [ 3, "sbca", "extended"        ],
0xa2   :  [ 2, "sbca", "indexedx"        ],
0x18a2 :  [ 3, "sbca", "indexedy"        ],
0xc2   :  [ 2, "sbcb", "immediate"       ],
0xd2   :  [ 2, "sbcb", "direct"          ],
0xf2   :  [ 3, "sbcb", "extended"        ],
0xe2   :  [ 2, "sbcb", "indexedx"        ],
0x18e2 :  [ 3, "sbcb", "indexedy"        ],
0x0d   :  [ 1, "sec",  "inherent"        ],
0x0f   :  [ 1, "sei",  "inherent"        ],
0x0b   :  [ 1, "sev",  "inherent"        ],
0x97   :  [ 2, "staa", "direct"          ],
0xb7   :  [ 3, "staa", "extended"        ],
0xa7   :  [ 2, "staa", "indexedx"        ],
0x18a7 :  [ 3, "staa", "indexedy"        ],
0xd7   :  [ 2, "stab", "direct"          ],
0xf7   :  [ 3, "stab", "extended"        ],
0xe7   :  [ 2, "stab", "indexedx"        ],
0x18e7 :  [ 3, "stab", "indexedy"        ],
0xdd   :  [ 2, "std",  "direct"          ],
0xfd   :  [ 3, "std",  "extended"        ],
0xed   :  [ 2, "std",  "indexedx"        ],
0x18ed :  [ 3, "std",  "indexedy"        ],
0xcf   :  [ 1, "stop", "inherent"        ],
0x9f   :  [ 2, "sts",  "direct"          ],
0xbf   :  [ 3, "sts",  "extended"        ],
0xaf   :  [ 2, "sts",  "indexedx"        ],
0x18af :  [ 3, "sts",  "indexedy"        ],
0xdf   :  [ 2, "stx",  "direct"          ],
0xff   :  [ 3, "stx",  "extended"        ],
0xef   :  [ 2, "stx",  "indexedx"        ],
0x18ef :  [ 3, "stx",  "indexedy"        ],
0x18df :  [ 3, "sty",  "direct"          ],
0x18ff :  [ 4, "sty",  "extended"        ],
0x1aef :  [ 3, "sty",  "indexedx"        ],
0x18ef :  [ 3, "sty",  "indexedy"        ],
0x80   :  [ 2, "suba", "immediate"       ],
0x90   :  [ 2, "suba", "direct"          ],
0xb0   :  [ 3, "suba", "extended"        ],
0xa0   :  [ 2, "suba", "indexedx"        ],
0x18a0 :  [ 3, "suba", "indexedy"        ],
0xc0   :  [ 2, "subb", "immediate"       ],
0xd0   :  [ 2, "subb", "direct"          ],
0xf0   :  [ 3, "subb", "extended"        ],
0xe0   :  [ 2, "subb", "indexedx"        ],
0x18e0 :  [ 3, "subb", "indexedy"        ],
0x83   :  [ 3, "subd", "immediatex"      ],
0x93   :  [ 2, "subd", "direct"          ],
0xb3   :  [ 3, "subd", "extended"        ],
0xa3   :  [ 2, "subd", "indexedx"        ],
0x18a3 :  [ 3, "subd", "indexedy"        ],
0x3f   :  [ 1, "swi",  "inherent"        ],
0x16   :  [ 1, "tab",  "inherent"        ],
0x06   :  [ 1, "tap",  "inherent"        ],
0x17   :  [ 1, "tba",  "inherent"        ],
0x00   :  [ 1, "test", "inherent"        ],
0x07   :  [ 1, "tpa",  "inherent"        ],
0x7d   :  [ 3, "tst",  "extended"        ],
0x6d   :  [ 2, "tst",  "indexedx"        ],
0x186d :  [ 3, "tst",  "indexedy"        ],
0x4d   :  [ 1, "tsta",  "inherent"       ],
0x5d   :  [ 1, "tstb",  "inherent"       ],
0x30   :  [ 1, "tsx",   "inherent"       ],
0x1830 :  [ 2, "tsy",   "inherent"       ],
0x35   :  [ 1, "txs",   "inherent"       ],
0x1835 :  [ 2, "tys",   "inherent"       ],
0x3e   :  [ 1, "wai",   "inherent"       ],
0x8f   :  [ 1, "xgdx", "inherent"        ],
0x188f :  [ 2, "xgdy", "inherent"        ],

}

# End of processor specific code
##########################################################################
