from optparse import OptionParser
from os import path

class Options:
    def __init__(self):
        parser = OptionParser()
        parser.add_option('-c', '--config', dest='configname', type='string', help='path to config file')

        (options, args) = parser.parse_args()

        self.configname = path.abspath(options.configname)
        if not self.configname:
            self.configname = '/etc/tgwatch/settings.toml'
