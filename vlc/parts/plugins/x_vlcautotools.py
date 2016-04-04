import os
import stat

import snapcraft
import snapcraft.common


class VlcAutotoolsPlugin(snapcraft.BasePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()
        schema['properties']['configflags'] = {
            'type': 'array',
            'minitems': 1,
            'uniqueItems': True,
            'items': {
                'type': 'string',
            },
            'default': [],
        }

        schema['properties']['install-via'] = {
            'enum': ['destdir', 'prefix'],
            'default': 'destdir',
        }

        return schema

    def __init__(self, name, options):
        super().__init__(name, options)
        self.build_packages.extend([
            'autoconf',
            'automake',
            'autopoint',
            'libtool',
            'make',
        ])

        if options.install_via == 'destdir':
            self.install_via_destdir = True
        elif options.install_via == 'prefix':
            self.install_via_destdir = False
        else:
            raise RuntimeError('Unsupported installation method: "{}"'.format(
                options.install_via))

    def build(self):
        super().build()
        
        print('About ro run bootstrap')
        self.run(['./bootstrap'])
        
        if not os.path.exists(os.path.join(self.builddir, "configure")):
            autogen_path = os.path.join(self.builddir, "autogen.sh")
            if os.path.exists(autogen_path):
                # Make sure it's executable
                if not os.access(autogen_path, os.X_OK):
                    os.chmod(autogen_path,
                             stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
                             stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP |
                             stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH)

                self.run(['env', 'NOCONFIGURE=1', './autogen.sh'])
            else:
                self.run(['autoreconf', '-i'])

        configure_command = ['./configure']
        make_install_command = ['make', 'install']

        if self.install_via_destdir:
            # Use an empty prefix since we'll install via DESTDIR
            configure_command.append('--prefix=')
            make_install_command.append('DESTDIR=' + self.installdir)
        else:
            configure_command.append('--prefix=' + self.installdir)

        self.run(configure_command + self.options.configflags)
        self.run(['make', '-j{}'.format(
            snapcraft.common.get_parallel_build_count())])
        self.run(make_install_command)
