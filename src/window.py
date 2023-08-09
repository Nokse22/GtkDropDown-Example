# window.py
#
# Copyright 2023 Nokse
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
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw, Gio, GObject, Gtk, GLib
import random

class ListString(GObject.Object):
    __gtype_name__ = 'ListString'

    def __init__(self, name):
        super().__init__()
        self._name = name

    @GObject.Property(type=str)
    def name(self):
        return self._name

class GtkdropdownExampleWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.countries_and_capitals = [
            ("United States", "Washington, D.C."),
            ("Canada", "Ottawa"),
            ("United Kingdom", "London"),
            ("Germany", "Berlin"),
            ("France", "Paris"),
            ("Australia", "Canberra"),
            ("Japan", "Tokyo"),
            ("China", "Beijing"),
            ("India", "New Delhi"),
            ("Brazil", "Brasília"),
            ("Mexico", "Mexico City"),
            ("South Korea", "Seoul"),
            ("Russia", "Moscow"),
            ("Italy", "Rome"),
            ("Spain", "Madrid"),
            ("Netherlands", "Amsterdam"),
            ("Turkey", "Ankara"),
            ("Saudi Arabia", "Riyadh"),
            ("Argentina", "Buenos Aires"),
            ("Egypt", "Cairo"),
            ("Canada", "Ottawa"),
            ("Brazil", "Brasília"),
            ("Mexico", "Mexico City"),
            ("South Korea", "Seoul"),
            ("Russia", "Moscow"),
            ("Italy", "Rome"),
            ("Spain", "Madrid"),
            ("Netherlands", "Amsterdam"),
            ("Turkey", "Ankara")
        ]

        countries = [country for country, capital in self.countries_and_capitals]
        capitals = [capital for country, capital in self.countries_and_capitals]
        random.shuffle(countries)
        random.shuffle(capitals)

        box = Gtk.Box(orientation=1, spacing=10)
        box.append(Adw.HeaderBar())

        box2 = Gtk.Box(spacing=6, hexpand=True, homogeneous=True, margin_start=10, margin_end=10)

        drop_down = self.new_drop_down_from_strings(countries)
        drop_down2 = self.new_drop_down_from_strings(capitals)

        box2.append(drop_down)
        box2.append(drop_down2)

        box.append(box2)
        button = Gtk.Button(label="Correct ?", margin_start=10, margin_end=10, margin_bottom=10)
        button.connect("clicked", self.check_correct, drop_down, drop_down2)
        box.append(button)

        self.set_content(box)
        self.set_resizable(False)

    def check_correct(self, btn, d1, d2):
        if self.get_capital(d1.get_model()[d1.get_selected()].name) == d2.get_model()[d2.get_selected()].name:
            btn.add_css_class("success")
        else:
            print(d1.get_model()[d1.get_selected()].name)
            print(d2.get_model()[d2.get_selected()].name)
            btn.add_css_class("error")
        GLib.timeout_add(2000, self.reset_button_color, btn)

    def get_capital(self, country_name):
        for country, capital in self.countries_and_capitals:
            if country == country_name:
                return capital
        return None

    def reset_button_color(self, btn):
        btn.remove_css_class("error")
        btn.remove_css_class("success")

    def new_drop_down_from_strings(self, strings):
        model_widget = Gio.ListStore(item_type=ListString)
        sort_model_widget  = Gtk.SortListModel(model=model_widget)
        filter_model_widget = Gtk.FilterListModel(model=sort_model_widget)
        custom_filter_model = Gtk.CustomFilter.new() #self._do_filter_widget_view, filter_model_widget
        filter_model_widget.set_filter(custom_filter_model)

        for string in strings:
            model_widget.append(ListString(string))

        factory_widget = Gtk.SignalListItemFactory()
        factory_widget.connect("setup", self._on_factory_widget_setup)
        factory_widget.connect("bind", self._on_factory_widget_bind)

        ddwdg = Gtk.DropDown(model=filter_model_widget, factory=factory_widget)
        ddwdg.set_enable_search(True)

        search_entry_widget = self._get_search_entry_widget(ddwdg)
        custom_filter_model.set_filter_func(self._do_filter_drop_down, filter_model_widget, search_entry_widget)
        search_entry_widget.connect('search-changed', self._on_search_drop_down_changed, custom_filter_model)

        return ddwdg

    def _get_search_entry_widget(self, dropdown):
        popover = dropdown.get_last_child()
        box = popover.get_child()
        box2 = box.get_first_child()
        search_entry = box2.get_first_child() # Gtk.SearchEntry
        return search_entry

    def _on_factory_widget_setup(self, factory, list_item):
        box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.HORIZONTAL)
        label = Gtk.Label()
        box.append(label)
        list_item.set_child(box)

    def _on_factory_widget_bind(self, factory, list_item):
        box = list_item.get_child()
        label = box.get_first_child()
        widget = list_item.get_item()
        label.set_text(widget.name)

    def _on_selected_widget(self, dropdown, data):
        widget = dropdown.get_selected_item()

        name = widget.name
        obj = eval(name)
        a = set(dir(obj))
        b = set(dir(Gtk.Widget))
        c = a - b
        for item in sorted(list(c)):
            self.model_method.append(Method(name=item))

    def _on_search_drop_down_changed(self, search_entry, filter_model):
        filter_model.changed(Gtk.FilterChange.DIFFERENT)

    def _do_filter_drop_down(self, item, filter_list_model, search_entry):
        return search_entry.get_text().upper() in item.name.upper()
