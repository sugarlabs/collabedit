#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import utils
from view import View
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject

try:
    from sugar3.presence.wrapper import CollabWrapper
    logging.error('USING SUGAR COLLAB WRAPPER!')

except ImportError:
    from collabwrapper import CollabWrapper


class CollabEdit(Gtk.VBox):

    __gsignals__ = {
        "insert-char": (GObject.SIGNAL_RUN_FIRST, None, [int, int]),
        "cursor-position-changed": (GObject.SIGNAL_RUN_FIRST, None, [int])
    }

    def __init__(self, activity):
        Gtk.VBox.__init__(self)

        self.collab = CollabWrapper(activity)
        self.collab.connect('message', self.__message_cb)
        self.collab.connect('joined', self.__joined_cb)

        self.view = View()
        self.view.connect("insert-char", self.__insert_char_cb)
        self.view.connect("cursor-position-changed",
                          self.__cursor_position_changed_cb)
        self.view.connect("tag-applied", self.__tag_applied_cb)
        self.view.connect("tag-removed", self.__tag_removed_cb)
        self.pack_start(self.view, True, True, 0)

    def __message_cb(self, collab, buddy, msg):
        action = msg.get("action")
        if action is None:
            return

        elif action == "insert":
            self.view.insert_at_position(msg.get("key"), msg.get("position"))

        elif action == "curosr_moved":
            self.view.draw_other_cursor(msg.get("id"), msg.get("position"))

        elif action == "insert_tag":
            self.view.insert_tag(msg.get("tag"),
                                 msg.get("start"),
                                 msg.get("end"))

        elif action == "remove_tag":
            self.view.remove_tag(msg.get("tag"),
                                 msg.get("start"),
                                 msg.get("end"))

    def __joined_cb(self, sender):
        if self.collab._leader:
            return

        self.collab.post(dict(action='init_request',
                              res_id=10))  # How get an unique id?

    def __insert_char_cb(self, view, key, position):
        if key in utils.LETTERS_KEYS:
            self.collab.post(dict(action="insert",
                                  key=Gdk.keyval_name(key),
                                  position=position))

    def __cursor_position_changed_cb(self, view, position):
        self.collab.post(dict(action="cursor_moved",
                              id=10,  # How get an unique id?
                              position=position))

        self.emit("cursor-position-changed", position)

    def __tag_applied_cb(self, buffer, tag, start, end):
        self.collab.post(dict(action="insert_tag",
                              tag=tag,
                              start=start,
                              end=end))

    def __tag_removed_cb(self, buffer, tag, start, end):
        self.collab.post(dict(action="remove_tag",
                              tag=tag,
                              start=start,
                              end=end))

    def toggle_bold(self):
        self.view.toggle_bold()

    def toggle_italic(self):
        self.view.toggle_italic()

    def toggle_underline(self):
        self.view.toggle_underline()

    def check_tag_at_offset(self, tag, position):
        return self.view.check_tag_at_offset(tag, position)
