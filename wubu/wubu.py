#-*- coding: utf-8 -*-
import sys
sys.path.append('../config')
sys.path.append('../telegram')
from configGather import configGather
import wubot

class WUBU():
    # CONFIG OPTION
    # 1. RUN SLACK BOT
    # 2. RUN CREON
    # 3. DB 서버 계정 정보
    # 4. ETC....
    def __init__(self):
        """ """
        self.config = configGather('../config/config.ini')
        self.TELEGRAM = int(self.config.getValue('SERVICE', 'TELEGRAM'))
        self.CREON = int(self.config.getValue('SERVICE', 'CREON'))

    # TELEGRAM? UI? CREON? 
    def start(self):
       """ """
       #if telegram on
       print (self.TELEGRAM)
       if self.TELEGRAM == 1:
           self.wubot = wubot.WuBot()
           self.wubot.start()
           self.wubot.join()

if __name__ == "__main__":
    wubu = WUBU()
    wubu.start()
