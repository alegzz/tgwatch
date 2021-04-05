
#from dynaconf import Dynaconf

#settings = Dynaconf(
#    envvar_prefix="DYNACONF",
#    settings_files=['settings.toml', '.secrets.toml'],
#)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load this files in the order.

import toml
from os import path

class Settings:
    def __init__(self, configfile):
        self.admins = []
        self.pattern = []
        self.channel = []
        self.session = ''
        self.api_id = ''
        self.api_hash = ''
        sessionpath = path.dirname(configfile)

        with open(configfile) as f:
            self._config = toml.loads(f.read())
        for k, v in self._config.items():
            setattr(self, k, v)

        if self.session:
            self.sessionfile = '{}/{}.session'.format(sessionpath, self.session)
