# main.py
#
# Copyright 2019 Ken VanDine
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import os
import subprocess

class StackWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="GTK Desktop Example Snap")
        self.set_border_width(10)
        self.set_default_size(400, 800)

        settings = Gio.Settings.new("com.github.kenvandine.gtk-desktop-example")
        theme_settings = Gio.Settings.new("org.gnome.desktop.interface")


        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_halign(Gtk.Align.CENTER)
        self.add(vbox)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)

        # Info box
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        example_string = settings.get_string("example-string")
        self.info = Gtk.Label(label="Example String: " + example_string)
        info_box.pack_start(self.info, False, False, 0)
        theme = theme_settings.get_string("gtk-theme")
        self.theme_info = Gtk.Label(label="Current GTK theme: " + theme)
        info_box.pack_start(self.theme_info, False, False, 0)
        stack.add_titled(info_box, "info_box", "Session Info")

        # System Info box
        sysinfo_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        sysinfo_box.pack_end(scrolledwindow, True, True, 0)
        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("")
        scrolledwindow.add(self.textview)
        stack.add_titled(sysinfo_box, "sysinfo_box", "System Info")
        self.on_sysinfo_refresh_clicked()

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        vbox.pack_start(stack_switcher, False, True, 0)
        vbox.pack_start(stack, True, True, 0)

    def on_sysinfo_refresh_clicked(self, widget=None):
        with open(os.devnull, 'w') as devnull:
            ret = subprocess.check_output("lshw", stderr=devnull)
        self.textbuffer.set_text(ret.decode("utf-8"))

win = StackWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
