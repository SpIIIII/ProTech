
import requests
import platform
import re
import os


class Update:
    def __init__ (self):
        self.url_of_sutup =   "http://68.183.208.74/mysetup.exe"
        self.cwd = os.getcwd()

        if platform.system() == 'Windows':
            self.desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/')
        else:
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/')
        self.versions = Versions() 


    def start(self):
        # if self.versions.remote_version > self.versions.local_version:
        print("it's New NEWER version")
   

    def download (self):
        response = requests.get(self.url_of_sutup)
        with open(self.cwd+'/tmp/ProTech setup.exe','wb') as f:
            f.write(response.content)




class Versions:
    def __init__(self):
        self.ulr_of_version = "http://68.183.208.74"
        self.local_version = self.get_local_version()
        self.remote_version = self.get_remote_version()


    def get_remote_version(self) -> str:
        """   Get version of program from remote server 68.183.208.74
        """
        responce = requests.get(self.ulr_of_version)
        pattern = '<h2>\s?(.+)\s?</h2>'
        version = re.findall(pattern,responce.content.decode())[0]
        remote_version = self.version_to_int(version)  
        return remote_version


    def get_local_version(self) -> str:
        """   Get local version of program from version file
        """
        return 'v1.0.0'


    def version_to_int (self, version_str:str) -> int:
        version_int = sum(int(j)*10**i for i,j in enumerate(version_str[-1::-2]))
        return version_int