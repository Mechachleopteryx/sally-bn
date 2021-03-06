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
import os

# current path
current = os.getcwd()

# resources path
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
os.chdir('../../')
root_path = os.getcwd()

# Go back
os.chdir(current)
current = os.getcwd()


# Glade Files
MAIN_WINDOW_GLADE = root_path + '/resources/gui/main_window.glade'
DISC_VAR_DIALOG_GLADE = root_path + '/resources/gui/discrete_var_dialog.glade'
TAB_DISC_BAYES_NET_GLADE = root_path + '/resources/gui/tab_disc_bayes_net.glade'
DIALOG_ABOUT = root_path + '/resources/gui/about.glade'
SPLASH_IMG = root_path + '/resources/image/splash.gif'