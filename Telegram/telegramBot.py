import logging
import telegram

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import dotenv_values

from Binance import checks
from Db import db


config = dotenv_values()
bot = telegram.Bot(config["telegram_bot_token"])

disclaimer = '_*This bot does not provide investment advice, every trade operation is at your own risk 🤓*_\.'
thankMessage = 'Found this bot useful? Please consider making some /donation 🤑'

# bot functions that are not commands

# tell everyonbe about dips
def announceDip():        
    pairs = checks.check24hDips()
    chats = db.getActiveChats()    
    for chat in chats: 
        for pair in pairs:                   
            asset = pair["symbol"].replace("USDT", "")        
            priceChangePrecent = float(pair["priceChangePercent"])
            prettyItemString = f'GET THE DIP!!! 🤑\n\nAsset: {asset}\n24h Change: {priceChangePrecent}%\n\nGo for it!!!🏃‍♂️\nhttps://www.binance.com/es/trade/{asset}_USDT'
            bot.send_message(text=prettyItemString, chat_id=chat["Chat_id"])
        bot.send_message(text=disclaimer, chat_id=chat["Chat_id"], parse_mode=telegram.ParseMode.MARKDOWN_V2)        
        bot.send_message(text=thankMessage, chat_id=chat["Chat_id"])
        
# bot commands
def start_command(update: Update, context: CallbackContext) -> None:    
    user = update.effective_user
    
    update.message.reply_markdown_v2(
        fr'Welcome {user.mention_markdown_v2()}\! here is the command list',        
    )

    commandList = f"/start - reboot the bot\n/enable - enable DIP messages\n/disable - disable DIP messages\n/status - status of messages\n/dips - try to get assets on a dip right now\n/donation - shows all donation info"
    
    update.message.reply_text(commandList)

    try:
        db.storeChat(update.message.chat.type, update.message.chat)    
    except:
        print("user already exists")


def enable_command(update: Update, context: CallbackContext):
    update.message.reply_text("this command is still under construction 🤓")


def disable_command(update: Update, context: CallbackContext):
    update.message.reply_text("this command is still under construction 🤓")


def status_command(update: Update, context: CallbackContext):
    user = update.effective_user
    status = db.getUserChatStatus(user)
    if status is not None:
            if status[0]["Active"] == 1:
                update.message.reply_text(f'Your status is ENABLE ✅\nand you will get dips messages 🤑')
                return True
            else:
                update.message.reply_text(f'Your status is DISABLE ✅\nand you will NOT get dips messages 😪\n\n/enable again dips messages')
                return True
    

# tell to individual user about dips
def dips_command(update: Update, context: CallbackContext):
    user = update.effective_user    
    dips = checks.check24hDips()
    for pair in dips:
        asset = pair["symbol"].replace("USDT", "")        
        priceChangePrecent = float(pair["priceChangePercent"])
        prettyItemString = f'GET THE DIP!!! 🤑\n\nAsset: {asset}\n24h Change: {priceChangePrecent}%\n\nGo for it!!!🏃‍♂️\nhttps://www.binance.com/es/trade/{asset}_USDT'
        bot.send_message(text=prettyItemString, chat_id=user.id)
    bot.send_message(text=disclaimer, chat_id=user.id,parse_mode=telegram.ParseMode.MARKDOWN_V2)
    bot.send_message(text=thankMessage, chat_id=user.id)


def donateinfo_command(update: Update, context: CallbackContext):
    donateInfo = f'You can make donations on BTC and DOGE to this wallet addresses: 👇\n\nBTC: someAddress\nDOGE: someAddress'
    update.message.reply_text(donateInfo)    

def botStart() -> None:    
    # Create the Updater and pass it your bot's token.
    updater = Updater(config["telegram_bot_token"])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("enable", enable_command))
    dispatcher.add_handler(CommandHandler("disable", disable_command))
    dispatcher.add_handler(CommandHandler("status", status_command))
    dispatcher.add_handler(CommandHandler("dips", dips_command))
    dispatcher.add_handler(CommandHandler("donation", donateinfo_command))

    # Start the Bot
    updater.start_polling()    
    updater.idle()