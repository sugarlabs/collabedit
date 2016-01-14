#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from gettext import gettext as _

import utils
from view import View

from gi.repository import Gtk
from gi.repository import Gdk

try:
    from sugar3.presence.wrapper import CollabWrapper
    logging.error('USING SUGAR COLLAB WRAPPER!')

except ImportError:
    from collabwrapper import CollabWrapper


class CollabEdit(Gtk.VBox):

    def __init__(self, activity):
        Gtk.VBox.__init__(self)

        self.collab = CollabWrapper(activity)
        self.collab.connect('message', self.__message_cb)
        self.collab.connect('joined', self.__joined_cb)

        self.view = View(self.collab)
        self.view.connect("insert-char", self.__insert_char_cb)
        self.pack_start(self.view, True, True, 0)

    def __message_cb(self, collab, buddy, msg):
        action = msg.get("action")
        if action is None:
            return

        if action == "insert":
            self.view.insert_at_position(msg.get("key"), msg.get("position"))

        #    self.add_item(*args)
        #elif action == 'delete_row':
        #    self._main_list.delete(args)
        #elif action == 'edit_item':
        #    self._main_list.edited_via_collab(msg.get('path'), args)
        #else:
        #    logging.error('Got message that is weird %r', msg)

    def __joined_cb(self, sender):
        if self.collab._leader:
            return

        self.collab.post(dict(
            action='init_request'))#,
            #res_id=self._id))

    def __insert_char_cb(self, view, key, position):
        if key in utils.LETTERS_KEYS:
            self.collab.post(dict(
                action="insert",
                key=Gdk.keyval_name(key)
                position=position))

