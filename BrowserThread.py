# pip install selenium beautifulsoup4 lxml packaging webdriver-manager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PyQt5.QtCore import QThread, pyqtSignal


class BrowserThread(QThread):
    #產生一支電話，打給ui 主執行緒用的
    callback = pyqtSignal(object)
    def __init__(self,path):
        super().__init__(None)
        self.browser = None
        self.path = path
    def run(self):
        #要執行的任務都要放在run 方法中
        opt = Options()
        opt.add_argument('--headless')
        opt.add_argument('--disable-gpu')
        opt.add_experimental_option('detach',True)
        #允許 Chrome 可以下載
        opt.add_experimental_option('excludeSwitches',['enable-logging'])
        #更改下載目錄
        prefs = {'profile.default_content_settings.popups':0, 'download.default_directory':self.path}
        opt.add_experimental_option('prefs',prefs)
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service = service,options=opt)
        #發射，打電話回ui主執行緒
        self.callback.emit(browser)