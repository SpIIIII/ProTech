import requests
import tkinter
import re

class Versions:
    def __init__ (self):
        self.urls_of_remote_version = ["http://68.183.208.74/", "http://68.183.208.74/file_storage/ProTech/"]
        with open('.version', 'r') as f:
            self.local_version_txt = f.read()
        self.local_version = self.version_to_int(self.local_version_txt)
        self.link_to_download = str()
    
    def get_remote_version_txt(self) -> str:
        """   Get version of program from remote server 68.183.208.74 """
        try:
            for i in self.urls_of_remote_version:
                responce = requests.get(i, timeout=1)
                if responce.status_code == 200:
                    remote_version_txt = self.find_version(responce)
                    return remote_version_txt
        except: 
            tkinter.messagebox.showinfo('Connection lost','Не возможно устанвоить соединение с сервером.\n Проверьте наличие подключения \
                                        и повторите попытку')

    def find_version(self, responce):
        pattern = r'<h2>\s?(.+)\s?</h2>' 
        return re.findall(pattern,responce.content.decode())[0]

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
        