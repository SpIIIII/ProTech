import requests
import tkinter
import config
import re

class Versions:
    def __init__ (self):
        self.urls_of_remote_version = config.remmotes
        with open('.version', 'r') as f:
            self.local_version_txt = f.read()
        self.local_version = self.version_to_int(self.local_version_txt)
        config.version = self.local_version_txt
        
    def get_responce(self):
        """ function to get remote version and link to update """
        try:
            for i in self.urls_of_remote_version:
                responce = requests.get(i, timeout=1)
                if responce.status_code == 200:
                    return responce
        except: 
            tkinter.messagebox.showinfo('Connection lost','Не возможно устанвоить соединение с сервером.\n Проверьте наличие подключения \
                                        и повторите попытку')
    
    def get_remote_version_txt(self)-> str:
        """  Get version of program from remote server 68.183.208.74  """
        responce = self.get_responce()
        remote_version_txt = self.pars_version(responce)
        return remote_version_txt

    def get_download_link(self)-> str:
        responce = self.get_responce()
        return self.pars_link(responce)

    def pars_link(self, responce):
        return responce.url
        
    def pars_version(self, responce):
        pattern = r'<h2>\s?(.+)\s?</h2>' 
        return re.findall(pattern, responce.content.decode())[0]

    @property
    def download_link(self):
        return self.get_download_link()

    @property
    def remote_version(self):
        return self.version_to_int(self.remote_version_txt)

    @property
    def remote_version_txt(self):
        return self.get_remote_version_txt()

    def version_to_int (self, version_str:str) -> int:
        """   Calculate int form of version to comparison. """
        # it just assumes that every number separapted by dot in text version is a corespond rank
        # i.e. big number in previous niche can outnumber that in next while compare in int form
        version_int = sum(int(j)*10**i for i,j in enumerate(version_str[-1::-2]))
        return version_int
        