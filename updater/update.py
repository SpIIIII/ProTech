
import requests
import platform
import tempfile
import re
import os


class Update:
    def __init__ (self):
        self.url_of_sutup =   "http://68.183.208.74/ProTech_32.exe"
        self.curent_folder = os.getcwd()
        self.temp_folder = tempfile.gettempdir()

        if platform.system() == 'Windows':
            self.desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/')
        else:
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/')
        self.versions = Versions()


    def start(self):
        if self.versions.remote_version > self.versions.local_version:
            self.download()
            self.run_setup()
            self.close_curetn()
               

    def download (self):
        response = requests.get(self.url_of_sutup)
        self.folder_with_installer = self.temp_folder+'/protech'
        if not os.path.exists(self.folder_with_installer):
                os.makedirs(self.folder_with_installer)
                
        with open(self.folder_with_installer+'/ProTech_setup_32.exe','wb') as f:
            f.write(response.content)

    def run_setup(self):
        os.system(f'{self.folder_with_installer}/ProTech_setup_32.exe')

    def close_curetn(self):
        os._exit(0)



class Versions:
    def __init__(self):
        self.ulr_of_version = "http://68.183.208.74"
        self.local_version = self.get_local_version()

    @property
    def remote_version(self) -> int:
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
        local_version = 'v1.0.0'
        return self.version_to_int(local_version)


    def version_to_int (self, version_str:str) -> int:
        version_int = sum(int(j)*10**i for i,j in enumerate(version_str[-1::-2]))
        return version_int