#!/usr/bin/env python

import sys
import traceback
import wx


class UndoHistoryPanel(wx.Panel):
    def __init__(self, parent, task, **kwargs):
        self.task = task
        wx.Panel.__init__(self, parent, wx.ID_ANY, **kwargs)

        # Mac/Win needs this, otherwise background color is black
        attr = self.GetDefaultAttributes()
        self.SetBackgroundColour(attr.colBg)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.history = wx.ListBox(self, size=(100, -1))

        self.sizer.Add(self.history, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.sizer.Layout()
        self.Fit()

    def DoGetBestSize(self):
        """ Base class virtual method for sizer use to get the best size
        """
        width = 300
        height = -1
        best = wx.Size(width, height)

        # Cache the best size so it doesn't need to be calculated again,
        # at least until some properties of the window change
        self.CacheBestSize(best)

        return best

    def set_task(self, task):
        self.task = task

    def recalc_view(self):
        e = self.task.active_editor
        self.editor = e
        if e is not None:
            self.update_history()

    def refresh_view(self):
        editor = self.task.active_editor
        if editor is not None:
            if self.editor != editor:
                self.recalc_view()
            else:
                self.Refresh()

    def update_history(self):
        project = self.task.active_editor
        summary = project.document.undo_stack.history_list()
        self.history.Set(summary)
        index = project.document.undo_stack.insert_index
        if index > 0:
            self.history.SetSelection(index - 1)

    def activate_spring_tab(self):
        self.recalc_view()

    def get_notification_count(self):
        return 0
