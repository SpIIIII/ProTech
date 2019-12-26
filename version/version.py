class Version:
    def __init__ (self):
        with open('version', 'r') as f:
            self.version_t = f.read()
        