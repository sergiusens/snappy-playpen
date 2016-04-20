import os

import snapcraft
from snapcraft.plugins import make
import sysconfig

class QmakePlugin(make.MakePlugin):

    def __init__(self, name, options, project):
        super().__init__(name, options, project)

    def snap_fileset(self):
        return ['*',
                'etc/xdg/qtchooser/snappy-qt5.conf',
                ]

    def _build_qt_config(self):
        arch = sysconfig.get_config_var('MULTIARCH')
        configdir = os.path.join(self.installdir, 'etc', 'xdg', 'qtchooser')
        os.makedirs(configdir, exist_ok=True)
        config = open(os.path.join(configdir, 'snappy-qt5.conf'), 'w')
        config.write('./usr/lib/{}/qt5/bin\n'.format(arch))
        config.write('./usr/lib/{}\n'.format(arch))
        config.close

    def build(self):
        print(self.installdir)
        assert self.installdir

        ## skip over parent class
        snapcraft.BasePlugin.build(self)

        qmake_command = ['qmake']
        make_all_command = ['make', 'all']

        self._build_qt_config()
        self.run(qmake_command)
        self.run(make_all_command)
