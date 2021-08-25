import schedule
import time
import threading

from Binance import checks
from Telegram import telegramBot

def job():
    print("Time for announce dips")
    telegramBot.announceDip()

def anounceLoop():
    schedule.every().day.at("00:00").do(job)
    schedule.every().day.at("03:00").do(job)
    schedule.every().day.at("06:00").do(job)
    schedule.every().day.at("09:00").do(job)
    schedule.every().day.at("12:55").do(job)
    schedule.every().day.at("15:00").do(job)
    schedule.every().day.at("18:00").do(job)
    schedule.every().day.at("21:00").do(job)    

    while True:
        schedule.run_pending()                
        time.sleep(1)

def main():
    threading.Thread(target=anounceLoop).start()
    threading.Thread(target=telegramBot.botStart()).start()
    

if __name__ == '__main__':
    main()