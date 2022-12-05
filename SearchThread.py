from PyQt5.QtCore import QThread, pyqtSignal
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class SearchThread(QThread):
    callback = pyqtSignal(object)
    def __init__(self, browser , song):
        super().__init__(None)
        self.browser = browser
        self.song = song
    def run(self):
        self.browser.get(f"https://www.youtube.com/results?search_query={self.song}")
        links = {}
        try:
            WebDriverWait(self.browser,20,5).until(EC.presence_of_element_located((By.ID,'video-title')))
            tags = self.browser.find_elements(By.TAG_NAME,'a')
            for tag in tags:
                # print(tag.text) #測試是否成功抓到資料
                href = tag.get_attribute('href')
                # print(href) #測試是否成功抓到資料
                if 'watch' in str(href):  #在youtube裡有'watch' 才可下載
                    title = tag.get_attribute('title')
                    if title=='': #沒有title再第二次搜尋
                        try:
                            title = tag.find_element(By.ID, 'video-title').get_attribute('title')
                        except:
                            pass
                    if title!='':
                        links[href]=f'{title} url={href}'
        except Exception as e:
            print(e) #列印錯誤訊息
        # print(links) #測試是否成功抓到資料
        self.callback.emit(links)