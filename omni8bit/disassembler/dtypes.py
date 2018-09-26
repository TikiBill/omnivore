# Debugger breakpoint definition
import numpy as np


HISTORY_ENTRY_DTYPE = np.dtype([
    ("pc", np.uint16),
    ("target_addr", np.uint16),
    ("num_bytes", np.uint8),
    ("flag", np.uint8),
    ("disassembler_type", np.uint8),
    ("unused", np.uint8),
    ("instruction", np.uint8, 16),
])

HISTORY_6502_DTYPE = np.dtype([
    ("pc", np.uint16),
    ("target_addr", np.uint16),
    ("num_bytes", np.uint8),
    ("flag", np.uint8),
    ("disassembler_type", np.uint8),
    ("unused", np.uint8),
    ("instruction", np.uint8, 4),
    ("a", np.uint8),
    ("x", np.uint8),
    ("y", np.uint8),
    ("sp", np.uint8),
    ("sr", np.uint8),
    ("before1", np.uint8),
    ("after1", np.uint8),
    ("before2", np.uint8),
    ("after2", np.uint8),
    ("before3", np.uint8),
    ("after3", np.uint8),
    ("extra", np.uint8),
])

EMULATOR_HISTORY_HEADER_DTYPE = np.dtype([
    ("num_allocated_entries", np.int32),
    ("num_entries", np.int32),
    ("first_entry_index", np.int32),
    ("latest_entry_index", np.int32),
    ("unused1", np.int32),
    ("unused2", np.int32),
])
