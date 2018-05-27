import hashlib, uuid

import numpy as np
import wx

from . import colors

# Font is a dict (easily serializable with JSON) with the following attributes:
#    data: string containing font data
#    name: human readable name
#    x_bits: number of bits to display
#    y_bytes: number of bytes per character
#
# template:
# Font = {
#    'data': data_bytes,
#    'name':"Default Atari Font",
#    'char_w': 8,
#    'char_h': 8,
#    'uuid': uuid.UUID(bytes=hashlib.md5(data_bytes).digest()),
#    }

A8DefaultFont = {
    'data': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x18\x18\x18\x00\x18\x00\x00fff\x00\x00\x00\x00\x00f\xffff\xfff\x00\x18>`<\x06|\x18\x00\x00fl\x180fF\x00\x1c6\x1c8of;\x00\x00\x18\x18\x18\x00\x00\x00\x00\x00\x0e\x1c\x18\x18\x1c\x0e\x00\x00p8\x18\x188p\x00\x00f<\xff<f\x00\x00\x00\x18\x18~\x18\x18\x00\x00\x00\x00\x00\x00\x00\x18\x180\x00\x00\x00~\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x18\x00\x00\x06\x0c\x180`@\x00\x00<fnvf<\x00\x00\x188\x18\x18\x18~\x00\x00<f\x0c\x180~\x00\x00~\x0c\x18\x0cf<\x00\x00\x0c\x1c<l~\x0c\x00\x00~`|\x06f<\x00\x00<`|ff<\x00\x00~\x06\x0c\x1800\x00\x00<f<ff<\x00\x00<f>\x06\x0c8\x00\x00\x00\x18\x18\x00\x18\x18\x00\x00\x00\x18\x18\x00\x18\x180\x06\x0c\x180\x18\x0c\x06\x00\x00\x00~\x00\x00~\x00\x00`0\x18\x0c\x180`\x00\x00<f\x0c\x18\x00\x18\x00\x00<fnn`>\x00\x00\x18<ff~f\x00\x00|f|ff|\x00\x00<f``f<\x00\x00xlfflx\x00\x00~`|``~\x00\x00~`|```\x00\x00>``nf>\x00\x00ff~fff\x00\x00~\x18\x18\x18\x18~\x00\x00\x06\x06\x06\x06f<\x00\x00flxxlf\x00\x00`````~\x00\x00cw\x7fkcc\x00\x00fv~~nf\x00\x00<ffff<\x00\x00|ff|``\x00\x00<fffl6\x00\x00|ff|lf\x00\x00<`<\x06\x06<\x00\x00~\x18\x18\x18\x18\x18\x00\x00fffff~\x00\x00ffff<\x18\x00\x00cck\x7fwc\x00\x00ff<<ff\x00\x00ff<\x18\x18\x18\x00\x00~\x0c\x180`~\x00\x00\x1e\x18\x18\x18\x18\x1e\x00\x00@`0\x18\x0c\x06\x00\x00x\x18\x18\x18\x18x\x00\x00\x08\x1c6c\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x006\x7f\x7f>\x1c\x08\x00\x18\x18\x18\x1f\x1f\x18\x18\x18\x03\x03\x03\x03\x03\x03\x03\x03\x18\x18\x18\xf8\xf8\x00\x00\x00\x18\x18\x18\xf8\xf8\x18\x18\x18\x00\x00\x00\xf8\xf8\x18\x18\x18\x03\x07\x0e\x1c8p\xe0\xc0\xc0\xe0p8\x1c\x0e\x07\x03\x01\x03\x07\x0f\x1f?\x7f\xff\x00\x00\x00\x00\x0f\x0f\x0f\x0f\x80\xc0\xe0\xf0\xf8\xfc\xfe\xff\x0f\x0f\x0f\x0f\x00\x00\x00\x00\xf0\xf0\xf0\xf0\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\xf0\xf0\xf0\xf0\x00\x1c\x1cww\x08\x1c\x00\x00\x00\x00\x1f\x1f\x18\x18\x18\x00\x00\x00\xff\xff\x00\x00\x00\x18\x18\x18\xff\xff\x18\x18\x18\x00\x00<~~~<\x00\x00\x00\x00\x00\xff\xff\xff\xff\xc0\xc0\xc0\xc0\xc0\xc0\xc0\xc0\x00\x00\x00\xff\xff\x18\x18\x18\x18\x18\x18\xff\xff\x00\x00\x00\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\x18\x18\x18\x1f\x1f\x00\x00\x00x`x`~\x18\x1e\x00\x00\x18<~\x18\x18\x18\x00\x00\x18\x18\x18~<\x18\x00\x00\x180~0\x18\x00\x00\x00\x18\x0c~\x0c\x18\x00\x00\x00\x18<~~<\x18\x00\x00\x00<\x06>f>\x00\x00``|ff|\x00\x00\x00<```<\x00\x00\x06\x06>ff>\x00\x00\x00<f~`<\x00\x00\x0e\x18>\x18\x18\x18\x00\x00\x00>ff>\x06|\x00``|fff\x00\x00\x18\x008\x18\x18<\x00\x00\x06\x00\x06\x06\x06\x06<\x00``lxlf\x00\x008\x18\x18\x18\x18<\x00\x00\x00f\x7f\x7fkc\x00\x00\x00|ffff\x00\x00\x00<fff<\x00\x00\x00|ff|``\x00\x00>ff>\x06\x06\x00\x00|f```\x00\x00\x00>`<\x06|\x00\x00\x18~\x18\x18\x18\x0e\x00\x00\x00ffff>\x00\x00\x00fff<\x18\x00\x00\x00ck\x7f>6\x00\x00\x00f<\x18<f\x00\x00\x00fff>\x0cx\x00\x00~\x0c\x180~\x00\x00\x18<~~\x18<\x00\x18\x18\x18\x18\x18\x18\x18\x18\x00~x|nf\x06\x00\x08\x188x8\x18\x08\x00\x10\x18\x1c\x1e\x1c\x18\x10\x00',
    'name': "8x8 Atari Default Font",
    'char_w': 8,
    'char_h': 8,
    'uuid': 'e46c1a08-b718-de27-3303-6e2701f0b0b3',
    }

A8ComputerFont = {
    'data': b'\x00\x00\x00\x00\x00\x00\x00\x0088\x18\x18\x00\x18\x18\x00\xee\xeeDD\x00\x00\x00\x00f\xffff\xfff\x00\x00\x18>`<\x06|\x18\x00\x00fl\x180fF\x00\x1c6\x1c8of;\x00\x18\x18\x18\x00\x00\x00\x00\x00\x1e\x18\x18888>\x00x\x18\x18\x1c\x1c\x1c|\x00\x00f<\xff<f\x00\x00\x00\x18\x18~\x18\x18\x00\x00\x00\x00\x00\x00\x00\x18\x180\x00\x00\x00~\x00\x00\x00\x00\x00\x00\x00\x00\x00\x18\x18\x00\x03\x06\x0c\x180`@\x00\x7fccccc\x7f\x008\x18\x18\x18>>>\x00\x7f\x03\x03\x7f``\x7f\x00~\x06\x06\x7f\x07\x07\x7f\x00ppppw\x7f\x07\x00\x7f``\x7f\x03\x03\x7f\x00|l`\x7fcc\x7f\x00\x7f\x03\x03\x1f\x18\x18\x18\x00>66\x7fww\x7f\x00\x7fcc\x7f\x07\x07\x07\x00<<<\x00<<<\x00<<<\x00<<\x180\x06\x0c\x180\x18\x0c\x06\x00\x00~\x00\x00~\x00\x00\x00`0\x18\x0c\x180`\x00\x7fc\x03\x1f\x1c\x00\x1c\x00\x7fcooo`\x7f\x00?33\x7fsss\x00~ff\x7fgg\x7f\x00\x7fgg`cc\x7f\x00~ffwww\x7f\x00\x7f``\x7fpp\x7f\x00\x7f``\x7fppp\x00\x7fc`ogg\x7f\x00sss\x7fsss\x00\x7f\x1c\x1c\x1c\x1c\x1c\x7f\x00\x0c\x0c\x0c\x0e\x0en~\x00ffl\x7fggg\x00000ppp~\x00g\x7f\x7fwggg\x00gw\x7foggg\x00\x7fccggg\x7f\x00\x7fcc\x7fppp\x00\x7fccggg\x7f\x07~ff\x7fwww\x00\x7f`\x7f\x03ss\x7f\x00\x7f\x1c\x1c\x1c\x1c\x1c\x1c\x00gggggg\x7f\x00ggggo>\x1c\x00gggo\x7f\x7fg\x00sss>ggg\x00ggg\x7f\x1c\x1c\x1c\x00\x7ffl\x187g\x7f\x00\x1e\x18\x18\x18\x18\x18\x1e\x00@`0\x18\x0c\x06\x03\x00x\x18\x18\x18\x18\x18x\x00\x00\x08\x1c6c\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x00\x006\x7f\x7f>\x1c\x08\x00\x18\x18\x18\x1f\x1f\x18\x18\x18\x03\x03\x03\x03\x03\x03\x03\x03\x18\x18\x18\xf8\xf8\x00\x00\x00\x18\x18\x18\xf8\xf8\x18\x18\x18\x00\x00\x00\xf8\xf8\x18\x18\x18\x03\x07\x0e\x1c8p\xe0\xc0\xc0\xe0p8\x1c\x0e\x07\x03\x01\x03\x07\x0f\x1f?\x7f\xff\x00\x00\x00\x00\x0f\x0f\x0f\x0f\x80\xc0\xe0\xf0\xf8\xfc\xfe\xff\x0f\x0f\x0f\x0f\x00\x00\x00\x00\xf0\xf0\xf0\xf0\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\x00\x00\x00\xf0\xf0\xf0\xf0\x00\x1c\x1cww\x08\x1c\x00\x00\x00\x00\x1f\x1f\x18\x18\x18\x00\x00\x00\xff\xff\x00\x00\x00\x18\x18\x18\xff\xff\x18\x18\x18\x00\x00<~~~<\x00\x00\x00\x00\x00\xff\xff\xff\xff\xc0\xc0\xc0\xc0\xc0\xc0\xc0\xc0\x00\x00\x00\xff\xff\x18\x18\x18\x18\x18\x18\xff\xff\x00\x00\x00\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0\x18\x18\x18\x1f\x1f\x00\x00\x00x`x`~\x18\x1e\x00\x00\x18<~\x18\x18\x18\x00\x00\x18\x18\x18~<\x18\x00\x00\x180~0\x18\x00\x00\x00\x18\x0c~\x0c\x18\x00\x00\x00\x18<~~<\x18\x00\x00\x00>\x02~v~\x00```~fn~\x00\x00\x00>20:>\x00\x06\x06\x06~fv~\x00\x00\x00~f~p~\x00\x00\x1e\x18>\x18\x1c\x1c\x00\x00\x00~fv~\x06~```~fvv\x00\x00\x18\x00\x18\x18\x1c\x1c\x00\x00\x0c\x00\x0c\x0c\x0e\x0e~\x00006|vw\x00\x00\x18\x18\x18\x1e\x1e\x1e\x00\x00\x00f\x7f\x7fkc\x00\x00\x00|fvvv\x00\x00\x00~fvv~\x00\x00\x00~fv~``\x00\x00~fn~\x06\x06\x00\x00>0888\x00\x00\x00> >\x0e~\x00\x00\x18~\x18\x1c\x1c\x1c\x00\x00\x00ffnn~\x00\x00\x00fnn>\x1c\x00\x00\x00ck\x7f>6\x00\x00\x00f>\x18>n\x00\x00\x00fff~\x0e~\x00\x00~\x1c\x186~\x00\x00\x18<~~\x18<\x00\x18\x18\x18\x18\x18\x18\x18\x18\x00~x|nf\x06\x00\x08\x188x8\x18\x08\x00\x10\x18\x1c\x1e\x1c\x18\x10\x00',
    'name': "8x8 Atari Custom Computer Font",
    'char_w': 8,
    'char_h': 8,
    'uuid': '5e605b00-56cd-1e63-92ac-7dcee6c2418e',
    }

A2DefaultFont = {
    'data': b"\x1c\x22*:\x1a\x02<\x00\x08\x14\x22\x22>\x22\x22\x00\x1e\x22\x22\x1e\x22\x22\x1e\x00\x1c\x22\x02\x02\x02\x22\x1c\x00\x1e\x22\x22\x22\x22\x22\x1e\x00>\x02\x02\x1e\x02\x02>\x00>\x02\x02\x1e\x02\x02\x02\x00<\x02\x02\x022\x22<\x00\x22\x22\x22>\x22\x22\x22\x00\x1c\x08\x08\x08\x08\x08\x1c\x00    \x22\x22\x1c\x00\x22\x12\n\x06\n\x12\x22\x00\x02\x02\x02\x02\x02\x02~\x00\x226**\x22\x22\x22\x00\x22\x22&*2\x22\x22\x00\x1c\x22\x22\x22\x22\x22\x1c\x00\x1e\x22\x22\x1e\x02\x02\x02\x00\x1c\x22\x22\x22*\x12,\x00\x1e\x22\x22\x1e\n\x12\x22\x00\x1c\x22\x02\x1c \x22\x1c\x00>\x08\x08\x08\x08\x08\x08\x00\x22\x22\x22\x22\x22\x22\x1c\x00\x22\x22\x22\x22\x22\x14\x08\x00\x22\x22***6\x22\x00\x22\x22\x14\x08\x14\x22\x22\x00\x22\x22\x14\x08\x08\x08\x08\x00> \x10\x08\x04\x02>\x00>\x06\x06\x06\x06\x06>\x00\x00\x02\x04\x08\x10 \x00\x00>00000>\x00\x08\x14\x22\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x80\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x08\x08\x08\x08\x00\x08\x00\x14\x14\x14\x00\x00\x00\x00\x00\x14\x14>\x14>\x14\x14\x00\x08<\n\x1c(\x1e\x08\x00\x06&\x10\x08\x0420\x00\x04\n\n\x04*\x12,\x00\x08\x08\x08\x00\x00\x00\x00\x00\x10\x08\x04\x04\x04\x08\x10\x00\x04\x08\x10\x10\x10\x08\x04\x00\x08*\x1c\x08\x1c*\x08\x00\x00\x08\x08>\x08\x08\x00\x00\x00\x00\x00\x00\x00\x10\x10\x08\x00\x00\x00>\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00 \x10\x08\x04\x02\x00\x00\x1c\x222*&\x22\x1c\x00\x08\x0c\x08\x08\x08\x08\x1c\x00\x1c\x22 \x18\x04\x02>\x00> \x10\x18 \x22\x1c\x00\x10\x18\x14\x12>\x10\x10\x00>\x02\x1e  \x22\x1c\x008\x04\x02\x1e\x22\x22\x1c\x00> \x10\x08\x04\x04\x04\x00\x1c\x22\x22\x1c\x22\x22\x1c\x00\x1c\x22\x22< \x10\x0e\x00\x00\x00\x08\x00\x00\x08\x00\x00\x00\x00\x00\x08\x00\x08\x08\x04\x10\x08\x04\x02\x04\x08\x10\x00\x00\x00>\x00>\x00\x00\x00\x04\x08\x10 \x10\x08\x04\x00\x1c\x22\x10\x08\x08\x00\x08\x00\x1c\x22*:\x1a\x02<\x00\x08\x14\x22\x22>\x22\x22\x00\x1e\x22\x22\x1e\x22\x22\x1e\x00\x1c\x22\x02\x02\x02\x22\x1c\x00\x1e\x22\x22\x22\x22\x22\x1e\x00>\x02\x02\x1e\x02\x02>\x00>\x02\x02\x1e\x02\x02\x02\x00<\x02\x02\x022\x22<\x00\x22\x22\x22>\x22\x22\x22\x00\x1c\x08\x08\x08\x08\x08\x1c\x00    \x22\x22\x1c\x00\x22\x12\n\x06\n\x12\x22\x00\x02\x02\x02\x02\x02\x02~\x00\x226**\x22\x22\x22\x00\x22\x22&*2\x22\x22\x00\x1c\x22\x22\x22\x22\x22\x1c\x00\x1e\x22\x22\x1e\x02\x02\x02\x00\x1c\x22\x22\x22*\x12,\x00\x1e\x22\x22\x1e\n\x12\x22\x00\x1c\x22\x02\x1c \x22\x1c\x00>\x08\x08\x08\x08\x08\x08\x00\x22\x22\x22\x22\x22\x22\x1c\x00\x22\x22\x22\x22\x22\x14\x08\x00\x22\x22***6\x22\x00\x22\x22\x14\x08\x14\x22\x22\x00\x22\x22\x14\x08\x08\x08\x08\x00> \x10\x08\x04\x02>\x00>\x06\x06\x06\x06\x06>\x00\x00\x02\x04\x08\x10 \x00\x00>00000>\x00\x08\x14\x22\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x80\xff\x00\x04\x08\x10\x00\x00\x00\x00\x00\x00\x00\x1c <\x22<\x00\x02\x02\x1a&\x22\x22\x1e\x00\x00\x00\x1c\x22\x02\x22\x1c\x00  ,2\x22\x22<\x00\x00\x00\x1c\x22>\x02<\x00\x18$\x04\x0e\x04\x04\x04\x00\x00\x00,2\x22< \x1e\x02\x02\x1a&\x22\x22\x22\x00\x08\x00\x0c\x08\x08\x08\x1c\x00 \x00    \x22\x1c\x02\x02\x12\n\x06\n\x12\x00\x0c\x08\x08\x08\x08\x08\x1c\x00\x00\x00\x16****\x00\x00\x00\x1a&\x22\x22\x22\x00\x00\x00\x1c\x22\x22\x22\x1c\x00\x00\x00\x1e\x22\x22\x1e\x02\x02\x00\x00<\x22\x22<  \x00\x00\x1a&\x02\x02\x02\x00\x00\x00<\x02\x1c \x1e\x00\x04\x04\x1e\x04\x04$\x18\x00\x00\x00\x22\x22\x222,\x00\x00\x00\x22\x22\x14\x14\x08\x00\x00\x00****\x14\x00\x00\x00\x22\x14\x08\x14\x22\x00\x00\x00\x22\x22\x22< \x1e\x00\x00>\x10\x08\x04>\x00\x08\x04\x04\x02\x04\x04\x08\x00\x08\x08\x08\x08\x08\x08\x08\x00\x08\x10\x10 \x10\x10\x08\x00\x00&\x19\x00\x00\x00\x00\x00\x00*\x14*\x14*\x00\x00",
    'name': "7x8 Apple ][ Default Font",
    'char_w': 7,
    'char_h': 8,
    'blink': True,
    'uuid': 'bfee0385-a80f-072d-ee1c-ac3fc034ba22',
    }

A2MouseTextFont = {
    'data': b"\xe3\xdd\xd5\xc5\xe5\xfd\xc3\xff\xf7\xeb\xdd\xdd\xc1\xdd\xdd\xff\xe1\xdd\xdd\xe1\xdd\xdd\xe1\xff\xe3\xdd\xfd\xfd\xfd\xdd\xe3\xff\xe1\xdd\xdd\xdd\xdd\xdd\xe1\xff\xc1\xfd\xfd\xe1\xfd\xfd\xc1\xff\xc1\xfd\xfd\xe1\xfd\xfd\xfd\xff\xc3\xfd\xfd\xfd\xcd\xdd\xc3\xff\xdd\xdd\xdd\xc1\xdd\xdd\xdd\xff\xe3\xf7\xf7\xf7\xf7\xf7\xe3\xff\xdf\xdf\xdf\xdf\xdf\xdd\xe3\xff\xdd\xed\xf5\xf9\xf5\xed\xdd\xff\xfd\xfd\xfd\xfd\xfd\xfd\xc1\xff\xdd\xc9\xd5\xd5\xdd\xdd\xdd\xff\xdd\xdd\xd9\xd5\xcd\xdd\xdd\xff\xe3\xdd\xdd\xdd\xdd\xdd\xe3\xff\xe1\xdd\xdd\xe1\xfd\xfd\xfd\xff\xe3\xdd\xdd\xdd\xd5\xed\xd3\xff\xe1\xdd\xdd\xe1\xf5\xed\xdd\xff\xe3\xdd\xfd\xe3\xdf\xdd\xe3\xff\xc1\xf7\xf7\xf7\xf7\xf7\xf7\xff\xdd\xdd\xdd\xdd\xdd\xdd\xe3\xff\xdd\xdd\xdd\xdd\xdd\xeb\xf7\xff\xdd\xdd\xdd\xd5\xd5\xc9\xdd\xff\xdd\xdd\xeb\xf7\xeb\xdd\xdd\xff\xdd\xdd\xeb\xf7\xf7\xf7\xf7\xff\xc1\xdf\xef\xf7\xfb\xfd\xc1\xff\xc1\xf9\xf9\xf9\xf9\xf9\xc1\xff\xff\xfd\xfb\xf7\xef\xdf\xff\xff\xc1\xcf\xcf\xcf\xcf\xcf\xc1\xff\xff\xff\xf7\xeb\xdd\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x80\xff\xff\xff\xff\xff\xff\xff\xff\xf7\xf7\xf7\xf7\xf7\xff\xf7\xff\xeb\xeb\xeb\xff\xff\xff\xff\xff\xeb\xeb\xc1\xeb\xc1\xeb\xeb\xff\xf7\xc3\xf5\xe3\xd7\xe1\xf7\xff\xf9\xd9\xef\xf7\xfb\xcd\xcf\xff\xfb\xf5\xf5\xfb\xd5\xed\xd3\xff\xf7\xf7\xf7\xff\xff\xff\xff\xff\xf7\xfb\xfd\xfd\xfd\xfb\xf7\xff\xf7\xef\xdf\xdf\xdf\xef\xf7\xff\xf7\xd5\xe3\xf7\xe3\xd5\xf7\xff\xff\xf7\xf7\xc1\xf7\xf7\xff\xff\xff\xff\xff\xff\xf7\xf7\xfb\xff\xff\xff\xff\xc1\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xf7\xff\xff\xdf\xef\xf7\xfb\xfd\xff\xff\xe3\xdd\xcd\xd5\xd9\xdd\xe3\xff\xf7\xf3\xf7\xf7\xf7\xf7\xe3\xff\xe3\xdd\xdf\xe7\xfb\xfd\xc1\xff\xc1\xdf\xef\xe7\xdf\xdd\xe3\xff\xef\xe7\xeb\xed\xc1\xef\xef\xff\xc1\xfd\xe1\xdf\xdf\xdd\xe3\xff\xc7\xfb\xfd\xe1\xdd\xdd\xe3\xff\xc1\xdf\xef\xf7\xfb\xfb\xfb\xff\xe3\xdd\xdd\xe3\xdd\xdd\xe3\xff\xe3\xdd\xdd\xc3\xdf\xef\xf1\xff\xff\xff\xf7\xff\xf7\xff\xff\xff\xff\xff\xf7\xff\xf7\xf7\xfb\xff\xef\xf7\xfb\xfd\xfb\xf7\xef\xff\xff\xff\xc1\xff\xc1\xff\xff\xff\xfb\xf7\xef\xdf\xef\xf7\xfb\xff\xe3\xdd\xef\xf7\xf7\xff\xf7\xff\x10\x086\x7f??~6\x10\x086A!!J6\x00\x00\x02\x06\x0e\x1e6B\x7f\x22\x14\x08\x08\x14*\x7f\x00@ \x11\n\x04\x04\x00\x7f?_lu{{\x7fp`~1y0?\x02\x00\x18\x07\x00\x07\x0c\x08p\x08\x04\x02\x7f\x02\x04\x08\x00\x00\x00\x00\x00\x00\x00\x00*\x08\x08\x08\x08I*\x1c\x08\x08\x1c*I\x08\x08\x08\x08\x7f\x00\x00\x00\x00\x00\x00\x00@@@DF\x7f\x06\x04????????\x13\x18\x1c~\x1c\x18\x10od\x0c\x1c?\x1c\x0c\x04{@H\x08\x7f>\x1cH@@H\x1c>\x7f\x08H@\x00\x00\x00\x7f\x00\x00\x00\x00\x01\x01\x01\x01\x01\x01\x01\x7f\x08\x10 \x7f \x10\x08\x00*U*U*U*UU*U*U*U*\x00>A\x01\x01\x01\x7f\x00\x00\x00?@@@\x7f\x00@@@@@@@@\x08\x1c>\x7f>\x1c\x08\x00\x7f\x00\x00\x00\x00\x00\x00\x7f\x14\x14w\x00w\x14\x14\x00\x7f@@LL@@\x7f\x01\x01\x01\x01\x01\x01\x01\x01\xfb\xf7\xef\xff\xff\xff\xff\xff\xff\xff\xe3\xdf\xc3\xdd\xc3\xff\xfd\xfd\xe1\xdd\xdd\xdd\xe1\xff\xff\xff\xc3\xfd\xfd\xfd\xc3\xff\xdf\xdf\xc3\xdd\xdd\xdd\xc3\xff\xff\xff\xe3\xdd\xc1\xfd\xc3\xff\xe7\xdb\xfb\xe1\xfb\xfb\xfb\xff\xff\xff\xe3\xdd\xdd\xc3\xdf\xe3\xfd\xfd\xe1\xdd\xdd\xdd\xdd\xff\xf7\xff\xf3\xf7\xf7\xf7\xe3\xff\xef\xff\xe7\xef\xef\xef\xed\xf3\xfd\xfd\xdd\xed\xf1\xed\xdd\xff\xf3\xf7\xf7\xf7\xf7\xf7\xe3\xff\xff\xff\xc9\xd5\xd5\xd5\xdd\xff\xff\xff\xe1\xdd\xdd\xdd\xdd\xff\xff\xff\xe3\xdd\xdd\xdd\xe3\xff\xff\xff\xe1\xdd\xdd\xe1\xfd\xfd\xff\xff\xc3\xdd\xdd\xc3\xdf\xdf\xff\xff\xc5\xf9\xfd\xfd\xfd\xff\xff\xff\xc3\xfd\xe3\xdf\xe1\xff\xfb\xfb\xe1\xfb\xfb\xdb\xe7\xff\xff\xff\xdd\xdd\xdd\xcd\xd3\xff\xff\xff\xdd\xdd\xdd\xeb\xf7\xff\xff\xff\xdd\xdd\xd5\xd5\xc9\xff\xff\xff\xdd\xeb\xf7\xeb\xdd\xff\xff\xff\xdd\xdd\xdd\xc3\xdf\xe3\xff\xff\xc1\xef\xf7\xfb\xc1\xff\xc7\xf3\xf3\xf9\xf3\xf3\xc7\xff\xf7\xf7\xf7\xf7\xf7\xf7\xf7\xf7\xf1\xe7\xe7\xcf\xe7\xe7\xf1\xff\xd3\xe5\xff\xff\xff\xff\xff\xff\xff\xd5\xeb\xd5\xeb\xd5\xff\xff\x1c\x22*:\x1a\x02<\x00\x08\x14\x22\x22>\x22\x22\x00\x1e\x22\x22\x1e\x22\x22\x1e\x00\x1c\x22\x02\x02\x02\x22\x1c\x00\x1e\x22\x22\x22\x22\x22\x1e\x00>\x02\x02\x1e\x02\x02>\x00>\x02\x02\x1e\x02\x02\x02\x00<\x02\x02\x022\x22<\x00\x22\x22\x22>\x22\x22\x22\x00\x1c\x08\x08\x08\x08\x08\x1c\x00     \x22\x1c\x00\x22\x12\n\x06\n\x12\x22\x00\x02\x02\x02\x02\x02\x02>\x00\x226**\x22\x22\x22\x00\x22\x22&*2\x22\x22\x00\x1c\x22\x22\x22\x22\x22\x1c\x00\x1e\x22\x22\x1e\x02\x02\x02\x00\x1c\x22\x22\x22*\x12,\x00\x1e\x22\x22\x1e\n\x12\x22\x00\x1c\x22\x02\x1c \x22\x1c\x00>\x08\x08\x08\x08\x08\x08\x00\x22\x22\x22\x22\x22\x22\x1c\x00\x22\x22\x22\x22\x22\x14\x08\x00\x22\x22\x22**6\x22\x00\x22\x22\x14\x08\x14\x22\x22\x00\x22\x22\x14\x08\x08\x08\x08\x00> \x10\x08\x04\x02>\x00>\x06\x06\x06\x06\x06>\x00\x00\x02\x04\x08\x10 \x00\x00>00000>\x00\x00\x00\x08\x14\x22\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\x00\x00\x00\x00\x00\x00\x00\x00\x08\x08\x08\x08\x08\x00\x08\x00\x14\x14\x14\x00\x00\x00\x00\x00\x14\x14>\x14>\x14\x14\x00\x08<\n\x1c(\x1e\x08\x00\x06&\x10\x08\x0420\x00\x04\n\n\x04*\x12,\x00\x08\x08\x08\x00\x00\x00\x00\x00\x08\x04\x02\x02\x02\x04\x08\x00\x08\x10   \x10\x08\x00\x08*\x1c\x08\x1c*\x08\x00\x00\x08\x08>\x08\x08\x00\x00\x00\x00\x00\x00\x08\x08\x04\x00\x00\x00\x00>\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00 \x10\x08\x04\x02\x00\x00\x1c\x222*&\x22\x1c\x00\x08\x0c\x08\x08\x08\x08\x1c\x00\x1c\x22 \x18\x04\x02>\x00> \x10\x18 \x22\x1c\x00\x10\x18\x14\x12>\x10\x10\x00>\x02\x1e  \x22\x1c\x008\x04\x02\x1e\x22\x22\x1c\x00> \x10\x08\x04\x04\x04\x00\x1c\x22\x22\x1c\x22\x22\x1c\x00\x1c\x22\x22< \x10\x0e\x00\x00\x00\x08\x00\x08\x00\x00\x00\x00\x00\x08\x00\x08\x08\x04\x00\x10\x08\x04\x02\x04\x08\x10\x00\x00\x00>\x00>\x00\x00\x00\x04\x08\x10 \x10\x08\x04\x00\x1c\x22\x10\x08\x08\x00\x08\x00\x1c\x22*:\x1a\x02<\x00\x08\x14\x22\x22>\x22\x22\x00\x1e\x22\x22\x1e\x22\x22\x1e\x00\x1c\x22\x02\x02\x02\x22\x1c\x00\x1e\x22\x22\x22\x22\x22\x1e\x00>\x02\x02\x1e\x02\x02>\x00>\x02\x02\x1e\x02\x02\x02\x00<\x02\x02\x022\x22<\x00\x22\x22\x22>\x22\x22\x22\x00\x1c\x08\x08\x08\x08\x08\x1c\x00     \x22\x1c\x00\x22\x12\n\x06\n\x12\x22\x00\x02\x02\x02\x02\x02\x02>\x00\x226**\x22\x22\x22\x00\x22\x22&*2\x22\x22\x00\x1c\x22\x22\x22\x22\x22\x1c\x00\x1e\x22\x22\x1e\x02\x02\x02\x00\x1c\x22\x22\x22*\x12,\x00\x1e\x22\x22\x1e\n\x12\x22\x00\x1c\x22\x02\x1c \x22\x1c\x00>\x08\x08\x08\x08\x08\x08\x00\x22\x22\x22\x22\x22\x22\x1c\x00\x22\x22\x22\x22\x22\x14\x08\x00\x22\x22\x22**6\x22\x00\x22\x22\x14\x08\x14\x22\x22\x00\x22\x22\x14\x08\x08\x08\x08\x00> \x10\x08\x04\x02>\x00>\x06\x06\x06\x06\x06>\x00\x00\x02\x04\x08\x10 \x00\x00>00000>\x00\x00\x00\x08\x14\x22\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\x04\x08\x10\x00\x00\x00\x00\x00\x00\x00\x1c <\x22<\x00\x02\x02\x1e\x22\x22\x22\x1e\x00\x00\x00<\x02\x02\x02<\x00  <\x22\x22\x22<\x00\x00\x00\x1c\x22>\x02<\x00\x18$\x04\x1e\x04\x04\x04\x00\x00\x00\x1c\x22\x22< \x1c\x02\x02\x1e\x22\x22\x22\x22\x00\x08\x00\x0c\x08\x08\x08\x1c\x00\x10\x00\x18\x10\x10\x10\x12\x0c\x02\x02\x22\x12\x0e\x12\x22\x00\x0c\x08\x08\x08\x08\x08\x1c\x00\x00\x006***\x22\x00\x00\x00\x1e\x22\x22\x22\x22\x00\x00\x00\x1c\x22\x22\x22\x1c\x00\x00\x00\x1e\x22\x22\x1e\x02\x02\x00\x00<\x22\x22<  \x00\x00:\x06\x02\x02\x02\x00\x00\x00<\x02\x1c \x1e\x00\x04\x04\x1e\x04\x04$\x18\x00\x00\x00\x22\x22\x222,\x00\x00\x00\x22\x22\x22\x14\x08\x00\x00\x00\x22\x22**6\x00\x00\x00\x22\x14\x08\x14\x22\x00\x00\x00\x22\x22\x22< \x1c\x00\x00>\x10\x08\x04>\x008\x0c\x0c\x06\x0c\x0c8\x00\x08\x08\x08\x08\x08\x08\x08\x08\x0e\x18\x180\x18\x18\x0e\x00,\x1a\x00\x00\x00\x00\x00\x00\x00*\x14*\x14*\x00\x00",
    'name': "7x8 Apple ][ Font w/Mouse Text",
    'char_w': 7,
    'char_h': 8,
    'uuid': '921db38b-f80a-c055-d1e5-bcff2477aa14',
    }


builtin_font_data = {f['uuid']:f for f in [A8DefaultFont, A8ComputerFont, A2DefaultFont, A2MouseTextFont]}


class AnticFont(object):
    def __init__(self, segment_viewer, font_data, font_renderer, playfield_colors, reverse=False):
        self.use_blinking = font_data.get('blink', False)
        self.char_w = font_renderer.char_bit_width
        self.char_h = font_renderer.char_bit_height
        self.scale_w = font_renderer.scale_width
        self.scale_h = font_renderer.scale_height
        self.uuid = font_data['uuid']

        self.set_colors(segment_viewer, playfield_colors)
        self.set_fonts(segment_viewer, font_data, font_renderer, reverse)

    def set_colors(self, segment_viewer, playfield_colors):
        fg, bg = colors.gr0_colors(playfield_colors)
        conv = segment_viewer.machine.get_color_converter()
        fg = conv(fg)
        bg = conv(bg)
        self.normal_gr0_colors = [fg, bg]
        prefs = segment_viewer.preferences
        self.highlight_gr0_colors = colors.get_blended_color_registers(self.normal_gr0_colors, prefs.highlight_background_color)
        self.match_gr0_colors = colors.get_blended_color_registers(self.normal_gr0_colors, prefs.match_background_color)
        self.comment_gr0_colors = colors.get_blended_color_registers(self.normal_gr0_colors, prefs.comment_background_color)
        self.data_gr0_colors = colors.get_dimmed_color_registers(self.normal_gr0_colors, prefs.background_color, prefs.data_background_color)

    def set_fonts(self, segment_viewer, font_data, font_renderer, reverse):
        if 'np_data' in font_data:
            data = font_data['np_data']
        else:
            data = np.fromstring(font_data['data'], dtype=np.uint8)
        self.font_data = font_data

        m = segment_viewer.machine
        self.normal_font = font_renderer.get_font(data, m.color_registers, self.normal_gr0_colors, reverse)

        prefs = segment_viewer.preferences
        h_colors = colors.get_blended_color_registers(m.color_registers, prefs.highlight_background_color)
        self.highlight_font = font_renderer.get_font(data, h_colors, self.highlight_gr0_colors, reverse)

        d_colors = colors.get_dimmed_color_registers(m.color_registers, prefs.background_color, prefs.data_background_color)
        self.data_font = font_renderer.get_font(data, d_colors, self.data_gr0_colors, reverse)

        m_colors = colors.get_blended_color_registers(m.color_registers, prefs.match_background_color)
        self.match_font = font_renderer.get_font(data, m_colors, self.match_gr0_colors, reverse)

        c_colors = colors.get_blended_color_registers(m.color_registers, prefs.comment_background_color)
        self.comment_font = font_renderer.get_font(data, c_colors, self.comment_gr0_colors, reverse)

    def get_height(self, zoom):
        return self.char_h * self.scale_h * zoom

    def get_image(self, char_index, zoom, highlight=False):
        f = self.highlight_font if highlight else self.normal_font
        array = f[char_index]
        w = self.char_w
        h = self.char_h
        image = wx.Image(w, h)
        image.SetData(array.tobytes())
        w *= self.scale_w * zoom
        h *= self.scale_h * zoom
        image.Rescale(w, h)
        bmp = wx.Bitmap(image)
        return bmp
