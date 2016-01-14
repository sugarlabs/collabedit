#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")

import collabedit

from gi.repository import Gtk

from sugar3.activity import activity
from sugar3.activity.widgets import StopButton
from sugar3.activity.widgets import EditToolbar
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.toolbarbox import ToolbarButton


class CollabEditActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        self.toolbarbox = ToolbarBox()
        self.toolbar = self.toolbarbox.toolbar
        self.set_toolbar_box(self.toolbarbox)

        self.edit = collabedit.CollabEdit(self)
        self.set_canvas(self.edit)

        self.setup_toolbar()

        self.show_all()

    def setup_toolbar(self):
        activity_button = ActivityToolbarButton(self)
        self.toolbar.insert(activity_button, -1)

        self.toolbar.insert(Gtk.SeparatorToolItem(), -1)

        edit_toolbar = EditToolbar()
        self.toolbar.insert(ToolbarButton(page=edit_toolbar, icon_name="toolbar-edit"), -1)

        edit_toolbar.insert(Gtk.SeparatorToolItem(), -1)

        ## FIXME: arreglar iconos, estos no se ven
        button_bold = ToolButton(stock_id="format-text-bold")
        edit_toolbar.insert(button_bold, -1)

        button_italic = ToolButton(stock_id="format-text-italic")
        edit_toolbar.insert(button_italic, -1)

        button_underline = Gtk.ToolButton(stock_id="format-text-underline")
        edit_toolbar.insert(button_underline, -1)

        #button_bold.connect("clicked", self.on_button_clicked, self.tag_bold)
        #button_italic.connect("clicked", self.on_button_clicked,
        #    self.tag_italic)
        #button_underline.connect("clicked", self.on_button_clicked,
        #    self.tag_underline)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        self.toolbar.insert(separator, -1)

        stop_button = StopButton(self)
        self.toolbar.insert(stop_button, -1)

        self.toolbarbox.show_all()
        edit_toolbar.show_all()

