import requests
import platform
import tempfile
import re
import os


class Updater:
    def __init__ (self, versions:object):
        self.url_of_sutup =   "http://68.183.208.74/ProTech_32.exe"
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

    def start(self):
        if self.need_update():
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
        os.startfile(f'{self.folder_with_installer}/ProTech_setup_32.exe')

    def close_curetn(self):
        os._exit(0)

