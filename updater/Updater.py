import requests
import platform
import tempfile
import re
import os


class Updater:
    def __init__ (self, versions:object)-> None:
        self.curent_folder = os.getcwd()
        self.temp_folder = tempfile.gettempdir()
        self.versions = versions
        self.update_needed = False
        
        if platform.system() == 'Windows':
            self.desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/')
        else:
            self.desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/')         

    def need_update(self) ->bool:
        return self.versions.local_version < self.versions.remote_version

    def start(self)-> None:
        if self.need_update():
            self.download()
            self.run_setup()
            self.close_curent()
               
    def download (self)-> None:
        self.url_to_download = self.versions.download_link + 'ProTech_32.exe' #"http://68.183.208.74/ProTech_32.exe"
        print(self.url_to_download)
        response = requests.get(self.url_to_download)
        self.folder_with_installer = self.temp_folder+'/protech'
        if not os.path.exists(self.folder_with_installer):
                os.makedirs(self.folder_with_installer)
                
        with open(self.folder_with_installer+'/ProTech_setup_32.exe','wb') as f:
            f.write(response.content)

    def run_setup(self)-> None:
        os.startfile(f'{self.folder_with_installer}/ProTech_setup_32.exe')

    def close_curent(self)-> None:
        os._exit(0)

