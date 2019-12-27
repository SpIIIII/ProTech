class Version:
    def __init__ (self):
        with open('version/version', 'r') as f:
            self.version_txt = f.read()

    def change_version (self, version:str):
        with open('version/version', 'w') as f:
            f.write(version)
        
    def get_version (self):
        return self.version_txt