#-*- coding: utf-8 -*-
from telegram.ext import Updater
from telegram.ext import CommandHandler
#import ebest  creon 변경
import threading
from queue import Queue
import time
#import pythoncom
import requests
from bs4 import BeautifulSoup
from enum import Enum, auto
import sys
sys.path.append('../config')
sys.path.append('../data')
from configGather import configGather
from crawling import Crawling

class WorkList(Enum):
    LOGIN = auto()
    PRICE = auto()
    USER = auto()
    AUTOTEST = auto()

class Worker(threading.Thread):
    def __init__(self, workList, workerQueue, config):
        super().__init__()
        self.workList = workList
        self.workerQueue = workerQueue
        self.crawling = Crawling()
        #self.__finance = ebest.Finance() creon

    def run(self):
        while True:
            #lock?
            time.sleep(3)
            if self.workerQueue.empty():
                continue

            work = self.workerQueue.get()

            if work[1] == self.workList.LOGIN:
                work[2].bot.send_message(work[0], "로그인 성공")

                """
                if self.__finance.login() == self.__finance.SUCCESS:
                    self.__finance.kospiLoad()
                    self.__finance.kosdaqLoad()
                    work[2].bot.send_message(work[0], "로그인 성공")
                else:
                    work[2].bot.send_message(work[0], "로그인 실패")
                    """
                continue
            elif work[1] == self.workList.PRICE:
                result = self.crawling.getPrice(work[3])
                if result == None:
                    work[2].bot.send_message(work[0], "현재 종목명으로 검색은 미지원합니다. 코드값을 입력해주세요." )
                else :
                    work[2].bot.send_message(work[0], work[3] + " 가격은 " + result + "원 입니다." )
                continue



class WuBot(threading.Thread):
    def __init__(self):
        super().__init__()

        self.config = configGather('../config/config.ini') #TODO main 에서 변경
        self.token = self.config.getValue('TELEGRAM', 'TOKEN')
        self.user = int(self.config.getValue('TELEGRAM', 'TELEGRAM_USERS'))

        self.__updater = Updater(token=self.token, use_context=True)
        self.__dispatcher = self.__updater.dispatcher

        start_handler = CommandHandler('start', self.startWUBU)
        self.__dispatcher.add_handler(start_handler)

        help_handler = CommandHandler('help', self.helpWUBU)
        self.__dispatcher.add_handler(help_handler)

        login_handler = CommandHandler('login', self.loginCreon)
        self.__dispatcher.add_handler(login_handler)

        price_handler = CommandHandler('price', self.getPrice)
        self.__dispatcher.add_handler(price_handler)

        user_handler = CommandHandler('admin', self.checkUser)
        self.__dispatcher.add_handler(user_handler)

        self.workList = WorkList
        self.workerQueue = Queue()
        self.admin = False

    def startWUBU(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="hello world!")


    def helpWUBU(self, update, context):
        id = update.effective_chat.id
        text = "안녕하세요. WUBUBOT 입니다.\n"
        context.bot.send_message(id, text)

    def loginCreon(self, update, context):
        id = update.effective_chat.id
        if self.admin == False:
            context.bot.send_message(id, "Admin 권한 확인이 필요합니다.")
            return None
        self.workerQueue.put((id, self.workList.LOGIN, context))
        context.bot.send_message(id, "로그인 시도 중")

    def getPrice(self, update, context):
        id = update.effective_chat.id
        text = update.effective_message.text
        priceCode = text.split(' ')
        self.workerQueue.put((id, self.workList.PRICE, context, priceCode[1]), context)
        context.bot.send_message(id, priceCode[1] + " 가격 조회 중")

    def checkUser(self, update, context):
        user_id = update.effective_user.id
        id = update.effective_chat.id
        if user_id == self.user:
            self.admin = True
            context.bot.send_message(id, "admin 전환 성공")


    def run(self):
        worker = Worker(self.workList, self.workerQueue, self.config)
        worker.start()
        self.__updater.start_polling()


if __name__ == "__main__":
    wubot = WuBot()
    wubot.start()
