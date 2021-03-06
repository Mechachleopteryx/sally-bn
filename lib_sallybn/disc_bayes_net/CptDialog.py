# ----------------------------------------------------------------------------
#
# Sally BN: An Open-Source Framework for Bayesian Networks.
#
# ----------------------------------------------------------------------------
# GNU General Public License v2
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ----------------------------------------------------------------------------

from gi.repository import Gtk

from lib_sallybn.disc_bayes_net.gwidgets import GraphicCptTable, StatesTable
from lib_sallybn.util import ugraphic
import lib_sallybn.util.resources as res

class CptDialog:
    def __init__(self):
        # Represents a Bayesian network with discrete CPD tables.
        self.var_name = None

    def show_cpt_dialog(self, window, disc_bn, selected_vetex):
        # Get widgets from dialog.
        cpt_dialog, treeview_cpt, text_var_name, button_cancel, \
        button_ok, button_rand, treeview_states, badd_state, bremove_state = \
            ugraphic.create_widget(res.DISC_VAR_DIALOG_GLADE,
                                ["dialog_cpt",
                                "treeview_cpt",
                                "text_var_name",
                                "button_cancel",
                                "button_ok",
                                "button_rand",
                                "treeview_states",
                                "badd_state",
                                "bremove_state"])


        # cpt_dialog.set_parent(window)
        cpt_dialog.set_modal(True)
        text_var_name.set_text(selected_vetex)

        #TODO clone disc_bn and assign only if accept

        # load info for CPT
        gcpt_table = GraphicCptTable(disc_bn,
                                     selected_vetex,
                                     treeview_cpt)

        def state_changed_func():
            gcpt_table.modify_treeview_for_cpt()


        gstates_table = StatesTable(disc_bn, selected_vetex,
                                    state_changed_func, treeview_states,
                                    badd_state, bremove_state)
        # Quit
        def quit(*args):
            cpt_dialog.destroy()
        cpt_dialog.connect("delete-event", quit)

        # Cancel
        def cancel_ev(widget):
            cpt_dialog.destroy()

        button_cancel.connect("clicked", cancel_ev)

        # Fill rand
        def fill_rand(widget):
            gcpt_table.fill_random()

        button_rand.connect("clicked", fill_rand)

        # OK
        def ok_ev(widget):
            # validate CPT
            if not gcpt_table.validate_cpt():
                dialog = Gtk.MessageDialog(cpt_dialog, 0, Gtk.MessageType.WARNING,
                                           Gtk.ButtonsType.OK, "Invalid CPT")
                dialog.format_secondary_text("Every row must sum 100 %")
                dialog.set_modal(True)
                dialog.run()
                dialog.destroy()

                return
            else:
                self.var_name = text_var_name.get_text()
                # Save cpt in current name
                cprob = gcpt_table.get_cprob_from_table()
                disc_bn.set_cprob(selected_vetex, cprob)

                cpt_dialog.destroy()

        button_ok.connect("clicked", ok_ev)

        cpt_dialog.run()
        # cpt_dialog.destroy()

    def get_var_name(self):
        return self.var_name
