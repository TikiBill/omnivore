# Standard library imports.
import sys
import os

# Major package imports.
import wx
import wx.stc
import numpy as np

# Enthought library imports.
from traits.api import Any, Bool, Int, List, Event, Enum, Instance, File, Unicode, Property, provides
from pyface.key_pressed_event import KeyPressedEvent

# Local imports.
from peppy2.framework.editor import FrameworkEditor
from i_hex_editor import IHexEditor
from grid_control import HexEditControl
from peppy2.utils.wx.stcbase import PeppySTC
from peppy2.utils.wx.stcbinary import BinarySTC
from peppy2.utils.wx.bitviewscroller import EVT_BYTECLICKED
import peppy2.utils.fonts as fonts
from peppy2.utils.dis6502 import Atari800Disassembler
from peppy2.utils.binutil import known_segment_parsers, DefaultSegmentParser, XexSegmentParser, InvalidSegmentParser

@provides(IHexEditor)
class HexEditor(FrameworkEditor):
    """ The toolkit specific implementation of a HexEditor.  See the
    IHexEditor interface for the API documentation.
    """

    #### 'IPythonEditor' interface ############################################

    obj = Instance(File)

    #### traits
    
    grid_range_selected = Bool
    
    font = Any
    
    disassembler = Any
    
    segment_parser = Any(XexSegmentParser)
    
    segments = List
    
    segment_number = Int(0)
    
    segment_data = Any(None)

    #### Events ####

    changed = Event

    key_pressed = Event(KeyPressedEvent)
    
    # Class attributes (not traits)
    
    font_list = None
    
    font_mode = Enum(2, 4, 5, 6, 7, 8, 9)
    
    ##### Default traits
    
    def _disassembler_default(self):
        return Atari800Disassembler

    ###########################################################################
    # 'PythonEditor' interface.
    ###########################################################################

    def create(self, parent):
        self.control = self._create_control(parent)
        self.init_fonts(self.window.application)
        self.task.fonts_changed = self.font_list

    def load(self, guess=None):
        """ Loads the contents of the editor.
        """
        if guess is None:
            path = self.path
            text = ''
        else:
            metadata = guess.get_metadata()
            path = metadata.uri
            text = guess.get_utf8()

        self.bytestore.SetBinary(text)
        self.path = path
        self.dirty = False
        
        self.set_segment_parser(self.segment_parser)
        self.update_panes()

    def save(self, path=None):
        """ Saves the contents of the editor.
        """
        if path is None:
            path = self.path

        f = file(path, 'w')
        f.write(self.control.GetTextUTF8())
        f.close()

        self.dirty = False
    
    def undo(self):
        self.bytestore.Undo()
    
    def redo(self):
        self.bytestore.Redo()

    def update_panes(self):
        temp_stc = BinarySTC()
        temp_stc.SetBinary(self.segment_data)
        self.control.Update(temp_stc)
        self.disassembly.set_disassembler(self.disassembler)
        self.disassembly.update(self.segment_data)
        self.byte_graphics.set_data(self.segment_data)
        self.font_map.set_data(self.segment_data)
        self.set_font(self.font)
        self.memory_map.set_data(self.segment_data)
        self.segment_list.set_segments(self.segments)
        self.task.segments_changed = self.segments
    
    def redraw_panes(self):
        self.font_map.Refresh()
    
    @classmethod
    def init_fonts(cls, application):
        if cls.font_list is None:
            try:
                data = application.get_bson_data("font_list")
                cls.font_list = data['font_list']
            except IOError:
                # file not found
                cls.font_list = []
            except ValueError:
                # bad JSON format
                cls.font_list = []
    
    def remember_fonts(self):
        data = {'font_list': self.font_list}
        self.window.application.save_bson_data("font_list", data)
    
    def set_font(self, font=None, font_mode=None):
        if font is None:
            font = self.font
        self.font = font
        if font_mode is None:
            font_mode = self.font_mode
        self.font_mode = font_mode
        self.font_map.set_font(font, font_mode)
        self.redraw_panes()
    
    def load_font(self, filename):
        try:
            fh = open(filename, 'rb')
            data = fh.read() + "\0"*1024
            data = data[0:1024]
            font = {
                'name': os.path.basename(filename),
                'data': data,
                'char_w': 8,
                'char_h': 8,
                }
            self.set_font(font)
            self.font_list.append(font)
            self.remember_fonts()
            self.task.fonts_changed = self.font_list
        except:
            raise
    
    def get_font_from_selection(self):
        pass
    
    def set_disassembler(self, disassembler):
        self.disassembler = disassembler
        self.disassembly.set_disassembler(disassembler)
        self.disassembly.update(self.segment_data)
    
    def set_segment_parser(self, parser):
        self.segment_parser = parser
        try:
            s = self.segment_parser(self.bytestore.data)
        except InvalidSegmentParser:
            self.segment_parser = DefaultSegmentParser
            s = self.segment_parser(self.bytestore.data)
        self.segments = s.segments
        self.segment_list.set_segments(self.segments)
        self.segment_data = self.bytestore.data
        self.segment_number = 0
        self.task.segments_changed = self.segments
    
    def view_segment_number(self, number):
        self.segment_number = number if number < len(self.segments) else 0
        self.segment_data = self.segments[self.segment_number].data
        self.update_panes()

    ###########################################################################
    # Trait handlers.
    ###########################################################################


    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_control(self, parent):
        """ Creates the toolkit-specific control for the widget. """

        # Base-class constructor.
        self.bytestore = stc = BinarySTC()
        self.control = HexEditControl(parent, self, stc, show_records=False)

        ##########################################
        # Events.
        ##########################################

        # Get related controls
        self.disassembly = self.window.get_dock_pane('hex_edit.disasmbly_pane').control
        self.disassembly.set_disassembler(self.disassembler)
        self.byte_graphics = self.window.get_dock_pane('hex_edit.byte_graphics').control
        self.font_map = self.window.get_dock_pane('hex_edit.font_map').control
        self.memory_map = self.window.get_dock_pane('hex_edit.memory_map').control
        self.segment_list = self.window.get_dock_pane('hex_edit.segments').control
        self.segment_list.Bind(wx.EVT_LISTBOX, self.on_segment_click)

        # Load the editor's contents.
        self.load()

        return self.control

    #### wx event handlers ####################################################
    
    def byte_clicked(self, byte, bit):
        self.control.SelectPos(byte)

    def on_segment_click(self, event):
        item = event.GetSelection()
        print "Selected segment %d" % item
        self.view_segment_number(item)
        event.Skip()

    def _on_stc_changed(self, event):
        """ Called whenever a change is made to the text of the document. """

        self.dirty = self.bytestore.CanUndo()
        self.can_undo = self.bytestore.CanUndo()
        self.can_redo = self.bytestore.CanRedo()
        self.changed = True

        # Give other event handlers a chance.
        event.Skip()

        return

    def _on_char(self, event):
        """ Called whenever a change is made to the text of the document. """

        self.key_pressed = KeyPressedEvent(
            alt_down     = event.m_altDown == 1,
            control_down = event.m_controlDown == 1,
            shift_down   = event.m_shiftDown == 1,
            key_code     = event.m_keyCode,
            event        = event
        )

        # Give other event handlers a chance.
        event.Skip()

        return
