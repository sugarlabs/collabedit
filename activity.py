#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collabedit
from gettext import gettext as _

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

from sugar3.activity import activity
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import EditToolbar
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.graphics.toggletoolbutton import ToggleToolButton


class CollabEditActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.toolbarbox = ToolbarBox()
        self.toolbar = self.toolbarbox.toolbar
        self.set_toolbar_box(self.toolbarbox)

        self.edit = collabedit.CollabEdit(self)
        self.edit.connect("cursor-position-changed", self._cursor_positon_changed_cb)
        self.set_canvas(self.edit)

        self.setup_toolbar()

        self.show_all()

    def _cursor_positon_changed_cb(self, edit, pos):
        self.button_bold.props.active = self.edit.check_tag_at_offset("bold", pos)
        self.button_italic.props.active = self.edit.check_tag_at_offset("italic", pos)
        self.button_underline.props.active = self.edit.check_tag_at_offset("underline", pos)

    def setup_toolbar(self):
        activity_button = ActivityToolbarButton(self)
        self.toolbar.insert(activity_button, -1)

        self.toolbar.insert(Gtk.SeparatorToolItem(), -1)

        edit_toolbar = EditToolbar()
        self.toolbar.insert(ToolbarButton(page=edit_toolbar, icon_name="toolbar-edit"), -1)

        edit_toolbar.insert(Gtk.SeparatorToolItem(), -1)

        self.button_bold = ToggleToolButton("format-text-bold")
        self.button_bold.set_tooltip(_("Bold"))
        self.button_bold.props.accelerator = "<Ctrl>B"
        self.button_bold.connect("toggled", lambda button: self.edit.toggle_bold())
        edit_toolbar.insert(self.button_bold, -1)

        self.button_italic = ToggleToolButton("format-text-italic")
        self.button_italic.set_tooltip(_("Italic"))
        self.button_italic.props.accelerator = "<Ctrl>I"
        self.button_italic.connect("toggled", lambda button: self.edit.toggle_italic())
        edit_toolbar.insert(self.button_italic, -1)

        self.button_underline = ToggleToolButton("format-text-underline")
        self.button_underline.set_tooltip(_("Underline"))
        self.button_underline.props.accelerator = "<Ctrl>B"
        self.button_underline.connect("toggled", lambda button: self.edit.toggle_underline())
        edit_toolbar.insert(self.button_underline, -1)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        self.toolbar.insert(separator, -1)

        stop_button = StopButton(self)
        self.toolbar.insert(stop_button, -1)

        self.toolbarbox.show_all()
        edit_toolbar.show_all()
