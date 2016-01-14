#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject


class Buffer(Gtk.TextBuffer):

    def __init__(self, collab):
        Gtk.TextBuffer.__init__(self)

        self.collab = collab

    def get_cursor_position(self):
        return self.props.cursor_position


class View(Gtk.ScrolledWindow):

    __gsignals__ = {
        "insert-char": (GObject.SIGNAL_RUN_FIRST, None, [int, int]),
        "cursor-position-changed": (GObject.SIGNAL_RUN_FIRST, None, [int])
    }

    def __init__(self, collab):
        Gtk.ScrolledWindow.__init__(self)

        self.buffer = Buffer(collab)
        self.buffer.connect("notify::cursor-position", self.__cursor_position_cb)

        self.view = Gtk.TextView.new_with_buffer(self.buffer)
        self.view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.view.connect("key-press-event", self.__key_press_event_cb)
        self.add(self.view)

    def __key_press_event_cb(self, widget, event):
        key = event.keyval
        if key in utils.LETTERS_KEYS or key in utils.OTHER_KEYS:
            self.emit("insert-char", key, self.buffer.get_cursor_position())

            return False

        return True;

    def __cursor_position_cb(self, buffer, *args):
        self.emit("cursor-position-changed", self.buffer.get_cursor_position())

    def insert_at_position(self, string, position):
        cursor = self.buffer.get_cursor_position()

        iter = self.buffer.get_iter_at_offset(position)
        self.buffer.insert(iter, string)

        if position < cursor:
            cursor += 1
            offset = self.buffer.get_iter_at_offset(cursor)
            self.buffer.place_cursor(offset)

