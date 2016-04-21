# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2016 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): David Planella <david.planella@ubuntu.com>

import os

import snapcraft
from snapcraft.plugins import make
import sysconfig

class QmakePlugin(make.MakePlugin):

    def __init__(self, name, options, project):
        super().__init__(name, options, project)

    def build(self):
        """Build the source code as retrieved from the pull phase.

        Being based on qmake, the project needs the `qmake` command to be run
        before doing the build. The `qmake` command generates a Makefile that
        can then be processed with standard `make`.

        The project does not have an install target, so we are not using the
        parent class' build method and we install the built binary
        programmatically.
        """

        # Skip over parent class to copy the source dir
        # to the build dir
        snapcraft.BasePlugin.build(self)

        qmake_command = ['qmake']
        make_all_command = ['make', 'all']

        # Run qmake to generate a Makefile
        self.run(qmake_command)
        # Run make to build the sources only (no installation)
        self.run(make_all_command)

        # The upstream build does not have an install target, but it puts
        # the one single binary (Notes) to ../bin relative to the build dir.
        # We then do the installation of that file programmatically
        binary_file = 'Notes'
        binary_dir = 'bin'

        os.makedirs(os.path.join(self.installdir, binary_dir))

        os.link(
            os.path.join(os.path.dirname(self.builddir), binary_dir,
                                         binary_file),
            os.path.join(self.installdir, binary_dir, binary_file))
