import os
import sys

import wx

from traits.api import on_trait_change, Bool, Undefined, Any

from atrcopy import comment_bit_mask, user_bit_mask, diff_bit_mask, data_style
from udis.udis_fast import TraceInfo, flag_origin

from omnivore.framework.enthought_api import EditorAction
from omnivore.utils.nputil import intscale
from omnivore.utils.wx import compactgrid as cg

from ..ui.segment_grid import SegmentGridControl, SegmentTable
from .hex2 import HexEditControl
from ..arch.disasm import iter_disasm_styles
from ..utils import searchutil

from . import SegmentViewer

import logging
log = logging.getLogger(__name__)



class UdisFastTable(cg.HexTable):
    column_labels = ["Bytes", "Disassembly", "Comment"]
    column_sizes = [11, 18, 30]

    def __init__(self, linked_base):
        s = linked_base.segment
        cg.HexTable.__init__(self, s.data, s.style, 2, s.start_addr)
        self.lines = None
        self.num_rows = 0
        self.index_to_row = []
        self.end_addr = 0
        self.chunk_size = 256
        self.set_display_format(linked_base.cached_preferences)

    def set_display_format(self, prefs):
        for i, w in enumerate(prefs.disassembly_column_widths):
            if w > 0:
                self.__class__.column_pixel_sizes[i] = w
        self.set_fmt_hex(prefs.hex_format_character)

    def set_fmt_hex(self, fmt_char):
        self.fmt_hex1 = "%" + fmt_char
        self.fmt_hex2 = "%02" + fmt_char
        self.fmt_hex4 = "%04" + fmt_char

    def update_disassembly(self, segment, disassembly, index=0, refresh=False):
        self.segment = segment
        self.data = segment.data
        self.style = segment.style
        self.last_valid_index = len(self.data)
        self.disassembly = disassembly
        # cache some values for fewer deep references
        self.index_to_row = self.disassembly.info.index_to_row
        self.lines = self.disassembly.info
        self.jump_targets = self.disassembly.info.labels
        self.start_addr = self.disassembly.start_addr
        self.end_addr = self.disassembly.end_addr
        self.num_rows = self.lines.num_instructions
        # print(self.disassembly, self.num_rows)

    def get_index_range(self, r, c):
        try:
            try:
                line = self.lines[r]
            except IndexError:
                line = self.lines[-1]
            except TypeError:
                return 0, 0
            index = line.pc - self.start_addr
            return index, index + line.num_bytes
        except IndexError:
            if r >= self.num_rows:
                index = self.last_valid_index - 1
            else:
                index = 0
            return index, index

    def is_index_valid(self, index):
        return self.num_rows > 0 and index >= 0 and index <= self.last_valid_index

    def get_index_of_row(self, row):
        line = self.lines[row]
        index = line.pc - self.start_addr
        return index

    def get_start_end_index_of_row(self, row):
        line = self.lines[row]
        index = line.pc - self.start_addr
        return index, index + line.num_bytes

    def is_pc_valid(self, pc):
        index = pc - self.start_addr
        return self.is_index_valid(index)

    def index_to_row_col(self, index, col=1):
        try:
            row = self.index_to_row[index]
        except:
            try:
                row = self.index_to_row[-1]
            except IndexError:
                return 0, 0
        return row, col

    def get_next_caret_pos(self, row, col):
        col += 1
        if col >= self._cols:
            if row < self.num_rows - 1:
                row += 1
                col = 1
            else:
                col = self._cols - 1
        return (row, col)

    def get_next_editable_pos(self, row, col):
        if col < 1:
            col = 1
        elif col == 1:
            col = 1
            row += 1
        elif col == 2:
            col = 2
            row += 1
        return (row, col)

    def get_prev_caret_pos(self, row, col):
        col -= 1
        if col < 1:
            if row > 0:
                row -= 1
                col = self._cols - 1
            else:
                col = 1
        return (row, col)

    def get_page_index(self, index, segment_page_size, dir, grid):
        r, c = self.get_row_col(index)
        vr = grid.get_num_visible_rows() - 1
        r += (dir * vr)
        if r < 0:
            r = 0
        index, _ = self.get_index_range(r, 0)
        return index

    def get_pc(self, row):
        try:
            row = self.lines[row]
            return row.pc
        except IndexError:
            return 0
        except TypeError:
            return 0

    def get_value_style(self, row, col, operand_labels_start_pc=-1, operand_labels_end_pc=-1, extra_labels={}, offset_operand_labels={}, line=None):
        if line is None:
            line = self.lines[row]
        index = line.pc - self.start_addr
        style = 0
        for i in range(line.num_bytes):
            style |= self.style[index + i]
        text = self.calc_display_text(row, col, line, index)
        return text, style

    def calc_display_text(self, row, col, line=None, index=None):
        if line is None:
            line = self.lines[row]
            index = line.pc - self.start_addr
        if col == 0:
            if self.lines[row].flag == flag_origin:
                text = ""
            else:
                text = self.disassembly.format_data_list_bytes(index, line.num_bytes)
        else:
            text = self.disassembly.format_instruction(index, line)
            comment = self.disassembly.format_comment(index, line)
            if comment:
                text += " ; " + comment
        return text

    def get_style_override(self, row, col, style):
        if self.lines[row].flag & self.disassembly.highlight_flags:
            return style|diff_bit_mask
        return style

    def get_label_at_index(self, index):
        row = self.index_to_row[index]
        return self.get_label_at_row(row)

    def get_label_at_row(self, row):
        addr = self.get_pc(row)
        return self.fmt_hex4 % addr


class DisassemblyImageCache(cg.DrawTableCellImageCache):
    def draw_item_at(self, parent, dc, rect, row, col, last_col, widths):
        for c in range(col, last_col):
            text, style = parent.table.get_value_style(row, col)
            #text = "blah"
            #style = 0
            w = widths[c]
            rect.width = w
            self.draw_text_to_dc(parent, dc, rect, rect, text, style)
            rect.x += w
            col += 1


class DisassemblyLineRenderer(cg.TableLineRenderer):
    def draw(self, parent, dc, line_num, start_cell, num_cells):
        col = self.cell_to_col[start_cell]
        last_cell = min(start_cell + num_cells, self.num_cells)
        last_col = self.cell_to_col[last_cell - 1] + 1
        rect = self.col_to_rect(line_num, col)
        self.image_cache.draw_item_at(parent, dc, rect, line_num, col, last_col, self.pixel_widths)

    def calc_column_range(self, parent,line_num, col, last_col):
        index, last_index = parent.table.get_index_range(line_num, col)
        return col, index, last_index


class DisassemblyGridControl(SegmentGridControl):
    def calc_default_table(self):
        linked_base = self.caret_handler
        return UdisFastTable(linked_base)

    def calc_line_renderer(self):
        image_cache = DisassemblyImageCache(False)
        return DisassemblyLineRenderer(self, 2, image_cache=image_cache, widths=[5,25], col_labels=['^Opcodes','^      Operand'])

    def recalc_view(self):
        self.segment_viewer.restart_disassembly()
        cg.HexGridWindow.recalc_view(self)
        if e.editor.can_trace:
            e.update_trace_in_segment()

    def get_disassembled_text(self, start=0, end=-1):
        return self.table.disassembly.get_disassembled_text(start, end)

    def encode_data(self, segment, linked_base):
        """Segment saver interface: take a segment and produce a byte
        representation to save to disk.
        """
        lines = self.table.disassembly.get_disassembled_text()
        text = os.linesep.join(lines) + os.linesep
        data = text.encode("utf-8")
        return data

    def extra_popup_actions(self, popup_data):
        actions = []
        addr_dest = self.table.disassembly.get_addr_dest(popup_data['row'], popup_data['col'])
        actions.extend(self.segment_viewer.linked_base.get_goto_actions_other_segments(addr_dest))
        actions.extend(self.segment_viewer.linked_base.get_goto_actions_same_byte(popup_data['index']))
        return actions


class CopyDisassemblyAction(EditorAction):
    """Copy the disassembly text of the current selection to the clipboard.

    """
    name = 'Copy Disassembly Text'
    enabled_name = 'can_copy'

    def perform(self, event):
        e = self.active_editor
        s = e.segment
        ranges = s.get_style_ranges(selected=True)
        lines = []
        try:
            for start, end in ranges:
                lines.extend(e.disassembly.get_disassembled_text(start, end))
        except IndexError:
            e.window.error("Disassembly tried to jump to an address outside this segment.")
            return
        text = os.linesep.join(lines) + os.linesep
        data_obj = wx.TextDataObject()
        data_obj.SetText(text)
        e.set_clipboard_object(data_obj)

    def _update_enabled(self, ui_state):
        self.enabled = self.active_editor.focused_viewer.has_cpu


class CopyCommentsAction(EditorAction):
    """Copy the text of the comments only, using the disassembly for line
    breaks. Any blank lines that appear in the disassembly are included in the
    copy.

    """
    name = 'Copy Disassembly Comments'
    enabled_name = 'can_copy'

    def perform(self, event):
        e = self.active_editor
        s = e.segment
        ranges = s.get_style_ranges(selected=True)
        lines = []
        for start, end in ranges:
            for _, _, _, comment, _ in e.disassembly.table.disassembler.iter_row_text(start, end):
                lines.append(comment)
        text = os.linesep.join(lines) + os.linesep
        data_obj = wx.TextDataObject()
        data_obj.SetText(text)
        e.set_clipboard_object(data_obj)

    def _update_enabled(self, ui_state):
        self.enabled = self.active_editor.focused_viewer.has_cpu


# Disassembly searcher uses the __call__ method to return the object because it
# needs extra info: the machine type & the disassembly list. Normal searchers
# just use the segment's raw data and returns itself in the constructor.
class DisassemblySearcher(searchutil.BaseSearcher):
    def __init__(self, viewer, panel):
        self.search_text = None
        self.matches = []
        self.panel = panel
        self.pretty_name = viewer.machine.disassembler.name

    def __call__(self, editor, search_text):
        self.search_text = self.get_search_text(search_text)
        if len(self.search_text) > 0:
            self.matches = self.get_matches(editor)
            self.set_style(editor)
        else:
            self.matches = []
        return self

    def __str__(self):
        return "disasm matches: %s" % str(self.matches)

    def get_search_text(self, text):
        return text

    def get_matches(self, editor):
        matches = self.panel.search(self.search_text, editor.last_search_settings.get('match_case', False))
        return matches


class DisassemblyViewer(SegmentViewer):
    name = "disassembly"

    pretty_name = "Disassembly"

    control_cls = DisassemblyGridControl

    has_cpu = True

    has_hex = True

    copy_special = [CopyDisassemblyAction, CopyCommentsAction]

    current_disassembly_ = Any(None)

    @property
    def window_title(self):
        return self.machine.disassembler.name + " (" + self.machine.memory_map.name + ")"

    @property
    def searchers(self):
        return [DisassemblySearcher(self, self.control)]

    @on_trait_change('machine.disassembler_change_event')
    def do_disassembler_change(self, evt):
        log.debug("do_disassembler_change for %s using %s; flags=%s" % (self.control, self.linked_base, str(evt)))
        if evt is not Undefined:
            self.clear_disassembly()
            self.restart_disassembly()
            self.linked_base.editor.update_pane_names()

    @on_trait_change('linked_base.editor.document.byte_values_changed')
    def byte_values_changed(self, index_range):
        log.debug("byte_values_changed: %s index_range=%s" % (self, str(index_range)))
        if index_range is not Undefined:
            self.restart_disassembly(index_range)

    @on_trait_change('linked_base.editor.document.byte_style_changed')
    def byte_style_changed(self, index_range):
        log.debug("byte_style_changed: %s index_range=%s" % (self, str(index_range)))
        if index_range is not Undefined:
            self.restart_disassembly(index_range)

    def recalc_data_model(self):
        self.clear_disassembly()

    ##### UdisFast interface

    def create_disassembler(self):
        prefs = self.linked_base.cached_preferences
        d = self.machine.get_disassembler(prefs.hex_grid_lower_case, prefs.assembly_lower_case, self.document.document_memory_map, self.segment.memory_map)
        for i, name in iter_disasm_styles():
            d.add_chunk_processor(name, i)
        return d

    @property
    def current_disassembly(self):
        if self.current_disassembly_ is None:
            d = self.create_disassembler()
            self.current_disassembly_ = d
        return self.current_disassembly_

    def clear_disassembly(self):
        self.current_disassembly_ = None

    def restart_disassembly(self, index=None):
        self.current_disassembly.disassemble_segment(self.segment)
        self.control.table.update_disassembly(self.segment, self.current_disassembly)

    ##### disassembly tracing

    def start_trace(self):
        self.trace_info = TraceInfo()
        self.update_trace_in_segment()

    def get_trace(self, save=False):
        if save:
            kwargs = {'user': True}
        else:
            kwargs = {'match': True}
        s = self.segment
        mask = s.get_style_mask(**kwargs)
        style = s.get_style_bits(**kwargs)
        is_data = self.trace_info.marked_as_data
        size = min(len(is_data), len(s))
        trace = is_data[s.start_addr:s.start_addr + size] * style
        if save:
            # don't change data flags for stuff that's already marked as data
            s = self.segment
            already_data = np.logical_and(s.style[0:size] & user_bit_mask > 0, trace > 0)
            indexes = np.where(already_data)[0]
            previous = s.style[indexes]
            trace[indexes] = previous
        return trace, mask

    def update_trace_in_segment(self, save=False):
        trace, mask = self.get_trace(save)
        s = self.segment
        size = len(trace)
        s.style[0:size] &= mask
        s.style[0:size] |= trace

    def trace_disassembly(self, pc):
        self.disassembler.fast.trace_disassembly(self.table.trace_info, [pc])
        self.update_trace_in_segment()
