#啟動錯誤訊息log : 工具列:Run /Edit configuration/Emulate terminal in output console
import sys, os
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QCheckBox, QListWidgetItem, QFileDialog
from BrowserThread import BrowserThread
from DownloadThread import DownloadThread
from SearchThread import SearchThread
from ui.ui_mainwindow import Ui_MainWindow

class Mainwindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.resize(960,720)
        self.path = "d:\\mp3_tmp" #一定要用 "\\"
        self.lbl_path.setText(self.path)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.disabledGui()
        #開啟瀏覽器:
        #1.新員工
        self.browserThread = BrowserThread(self.path)
        #2.callback打電話給老闆
        self.browserThread.callback.connect(self.browserThreadCallback)
        #3.叫新員工開始工作
        self.browserThread.start()
        self.btn_search.clicked.connect(self.btnSearch_click)

        self.btn_download.clicked.connect(self.btnDownload_click)

        self.btn_path.clicked.connect(self.btnPath_click)

        #按下鍵盤"Enter"鍵開始下載
        self.txtSong.installEventFilter(self)
    def btnPath_click(self):
        #path 為區域變數，再此區塊執行後就沒有其他地方使用，故可以設定區域變數
        path = QFileDialog.getExistingDirectory()
        if path !='':
            self.path = path.replace("/","\\")
            self.lbl_path.setText(self.path)
            self.disabledGui() #停止按鈕干擾
            #將原本的瀏覽器關掉
            # self.browser.close()
            self.browser.quit() #用 quit 速度會快點
            #重新設定路徑
            self.browserThread = BrowserThread(self.path)

            self.browserThread.callback.connect(self.browserThreadCallback)
            self.browserThread.start()

    #鍵盤按下Enter鍵，執行搜尋
    def eventFilter(self, source, event):
        if(event.type()==QEvent.KeyPress and source is self.txtSong):
            if event.text()=='\r':
                self.btnSearch_click()
        return super(Mainwindow, self).eventFilter(source,event) #這段系統內定一定要加

    def btnDownload_click(self):
        # print('Download被按了')
        count = self.lst_widgt.count()
        # 抓取所有的方塊
        boxes = [self.lst_widgt.itemWidget(self.lst_widgt.item(i)) for i in range(count)]
        #
        chks =[]
        for box in boxes:
            if box.isChecked():
                chks.append(box.text())
        # print(chks)
        self.disabledGui()
        self.downloadThread = DownloadThread(self.browser ,chks ,self.path)
        #每下載一首回報
        self.downloadThread.callback.connect(self.downloadThreadCallback) #第一支電話
        #所有下載完回報
        self.downloadThread.finished.connect(self.downloadThreadFinished) #第二支電話
        self.downloadThread.start()
    def downloadThreadCallback(self,msg):
        self.lbl_status.setText(msg)
    def downloadThreadFinished(self):
        self.lbl_status.setText('下載完成')
        self.enabledGui()

    def btnSearch_click(self):
        self.lst_widgt.clear()
        self.song = self.txtSong.text()
        if self.song =="":
            dialong = QMessageBox()
            dialong.setWindowTitle("錯誤訊息")
            dialong.setText("請輸入歌手/歌曲")
            dialong.exec()
            return
        self.lbl_status.setText("搜尋中...")
        #先鎖住按鈕
        self.disabledGui()
        #找一個新員工來查詢
        self.searchThread = SearchThread(self.browser,self.song)
        self.searchThread.callback.connect(self.searchThreadCallback)
        self.searchThread.start()
    def searchThreadCallback(self, links): #不要命名object ，因為它是物件非變數
        self.enabledGui()
        self.lbl_status.setText('')
        for key in links.keys():
            item = QListWidgetItem()
            self.lst_widgt.addItem(item)
            box = QCheckBox(links[key])
            self.lst_widgt.setItemWidget(item ,box)



    def browserThreadCallback(self, browser):
        self.browser = browser
        self.enabledGui()


    def disabledGui(self):
        self.txtSong.setEnabled(False)
        self.btn_path.setEnabled(False)
        self.btn_download.setEnabled(False)
        self.btn_search.setEnabled(False)
    def enabledGui(self):
        self.txtSong.setEnabled(True)
        self.btn_path.setEnabled(True)
        self.btn_download.setEnabled(True)
        self.btn_search.setEnabled(True)



if __name__=='__main__':
    app = QApplication(sys.argv)
    mp3 = Mainwindow()
    mp3.show()
    app.exec()#等待迴圈，監控滑鼠鍵盤，更新視窗

