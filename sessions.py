import os

class Session:
    def __init__(self, sessionfile):
        self._sessionfile = sessionfile
        try:
            with open(self._sessionfile) as f:
                self.string = f.read()
        except:
            self.string = ''
    
    def save(self, session):
        self.string = session
        try:
            with open(self._sessionfile, 'w') as f:
                f.write(self.string)
        except:
            pass
