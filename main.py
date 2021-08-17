import schedule
import time

from Binance import checks
from Telegram import telegramBot

def job():
    telegramBot.announceDip()

def main():
    schedule.every().day.at("00:00").do(job)
    schedule.every().day.at("03:00").do(job)
    schedule.every().day.at("06:00").do(job)
    schedule.every().day.at("09:00").do(job)
    schedule.every().day.at("12:00").do(job)
    schedule.every().day.at("15:00").do(job)
    schedule.every().day.at("18:00").do(job)
    schedule.every().day.at("21:00").do(job)
    telegramBot.botStart()

if __name__ == '__main__':
    main()