import os

import snapcraft
from snapcraft.plugins import autotools

class FakeAutotoolsPlugin(autotools.AutotoolsPlugin):
    def build(self):

        print(self.installdir)
        assert self.installdir

        ## skip over parent class
        snapcraft.BasePlugin.build(self)

        configure_command = ['./configure']
        make_install_command = ['make', 'install']

        if self.install_via_destdir:
            # Use an empty prefix since we'll install via DESTDIR
            configure_command.append('--prefix=')
            make_install_command.append('DESTDIR=' + self.installdir)
        else:
            configure_command.append('--prefix=' + self.installdir)

        self.run(configure_command + self.options.configflags)
        self.run(['make', '-j{}'.format(self.project.parallel_build_count)])
        self.run(make_install_command)
