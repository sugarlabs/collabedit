#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GObject


class Buffer(Gtk.TextBuffer):

    def __init__(self):
        Gtk.TextBuffer.__init__(self)

        self.__make_tags()

    def __make_tags(self):
        self.tag_bold = self.create_tag("bold", weight=Pango.Weight.BOLD)
        self.tag_italic = self.create_tag("italic", style=Pango.Style.ITALIC)
        self.tag_underline = self.create_tag("underline", underline=Pango.Underline.SINGLE)
        self.tag_curosr = self.create_tag("cursor", background="green")

    def __get_tag_by_name(self, tag):
        tags = {
            "bold": self.tag_bold,
            "italic": self.tag_italic,
            "underline": self.tag_underline
        }

        return tags[tag]

    def __toggle_tag(self, tag):
        start, end = self.get_selection_bounds()
        if start == end:
            apply_tag = not self.check_tag_at_offset(tag, start.get_offset())

        else:
            apply_tag = not self.check_tag_at_bounds(tag, start, end)

        if apply_tag:
            self.apply_tag_by_name(tag, start, end)

        else:
            self.remove_tag_by_name(tag, start, end)

    def get_cursor_position(self):
        return self.props.cursor_position

    def get_selection_bounds(self):
        bounds = Gtk.TextBuffer.get_selection_bounds(self)
        if bounds:
            return bounds

        else:
            start = end = self.get_iter_at_offset(self.get_cursor_position())
            return start, end

    def toggle_bold(self):
        self.__toggle_tag("bold")

    def toggle_italic(self):
        self.__toggle_tag("italic")

    def toggle_underline(self):
        self.__toggle_tag("underline")

    def check_tag_at_offset(self, tag, offset):
        iter = self.get_iter_at_offset(offset)
        start, end = self.get_selection_bounds()

        if start == end:  # Haven't selection
            tag = self.__get_tag_by_name(tag)
            return tag in iter.get_tags()

        else:
            return self.check_tag_at_bounds(tag, start, end)

    def check_tag_at_bounds(self, tag, start, end):
        tag = self.__get_tag_by_name(tag)
        return tag in start.get_tags() and tag in end.get_tags()


class View(Gtk.ScrolledWindow):

    __gsignals__ = {
        "insert-char": (GObject.SIGNAL_RUN_FIRST, None, [int, int]),
        "cursor-position-changed": (GObject.SIGNAL_RUN_FIRST, None, [int])
    }

    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)

        self.buffer = Buffer()
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

    def toggle_bold(self):
        self.buffer.toggle_bold()

    def toggle_italic(self):
        self.buffer.toggle_italic()

    def toggle_underline(self):
        self.buffer.toggle_underline()

    def check_tag_at_offset(self, tag, position):
        return self.buffer.check_tag_at_offset(tag, position)

