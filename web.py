#encoding:utf-8
import sys  
from PyQt4.QtGui import *  
from PyQt4.QtCore import *  
from PyQt4.QtWebKit import * 
import pandas as pd 
import StringIO
import re
  
url = r'http://www.jisilu.cn/data/sfnew/#tlink_3'

class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()  

if __name__ == '__main__':
    r = Render(url)  
    # html = str.decode( str(r.frame.toPlainText()),'utf-8')
    html = str(r.frame.toPlainText())
    
    col_start = html.find('代码')
    col_end   = html.find('定期折算')
    end   = html.find('数据说明')
    
    cols = html[col_start:col_end + 12]
    cols = cols.replace('\n','')
    cols = map(lambda x: str.decode(x,'utf-8'),cols.split())
    body = html[col_end + 13:end]
    body = body.replace(',', '、')
    ###regex
    pattern = re.compile('[^\S\n ]')
    body = pattern.sub(',',body)
    ###norml
    # body = body.replace('\t', ',')
    with open('e:\\tmp.csv','w') as fout:
        fout.write(body)
        
    df = pd.read_csv('e:\\tmp.csv',header = None)
    df.columns = cols
    print df.head()
    