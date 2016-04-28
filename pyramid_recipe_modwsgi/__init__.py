import logging
import os
import stat
import zc.buildout
from zc.recipe.egg.egg import Eggs

ENV_TEMPLATE = """\
import os
"""

WSGI_TEMPLATE = """\
import sys
sys.path[0:0] = [
    %(syspath)s,
    ]

from pyramid.paster import get_app, setup_logging
configfile = "%(configfile)s"
setup_logging(configfile)
application = get_app(configfile, name=%(app_name)s)
"""


class Recipe:
    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.logger = logging.getLogger(self.name)

        if "config-file" not in options:
            self.logger.error(
                    "You need to specify either a paste configuration file")
            raise zc.buildout.UserError("No paste configuration given")

        if "target" in options:
            location = os.path.dirname(options["target"])
            if not os.path.isdir(location):
                self.logger.error(
                    "The 'target' option refers to a directory that is not "
                    "valid: %s" % location)
                raise zc.buildout.UserError("Invalid directory for target")

    def install(self):
        egg = Eggs(self.buildout, self.options["recipe"], self.options)
        reqs, ws = egg.working_set()
        path = [pkg.location for pkg in ws]
        extra_paths = self.options.get('extra-paths', '')
        extra_paths = extra_paths.split()
        path.extend(extra_paths)

        # Do not put None into 'quotes'
        # Everything else should be a string pointing to a pipeline
        app_name = self.options.get('app_name')
        if app_name is not None:
            app_name = '"%s"' % app_name

        env = self.options.get('env')
        if env:
            output = ENV_TEMPLATE
            for line in env.splitlines():
                key, value = line.split('=')
                output += "os.environ['%s'] = '%s'\n" % (key, value)
            output += '\n'
        else:
            output = ''

        output += WSGI_TEMPLATE % dict(
            configfile=self.options["config-file"],
            syspath=",\n    ".join((repr(p) for p in path)),
            app_name=app_name
            )

        target = self.options.get("target")
        if target is None:
            location = os.path.join(
                            self.buildout["buildout"]["parts-directory"],
                            self.name)
            if not os.path.exists(location):
                os.mkdir(location)
                self.options.created(location)
            target = os.path.join(location, "wsgi")
        else:
            self.options.created(target)

        f = open(target, "wt")
        f.write(output)
        f.close()

        exec_mask = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(target, os.stat(target).st_mode | exec_mask)
        self.options.created(target)

        return self.options.created()

    def update(self):
        self.install()
