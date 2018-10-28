#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
#import urllib.request as get
import urllib2 as get
import json
import time
import re

url = 'https://api.coinmarketcap.com/v2/listings/'
html = get.urlopen(url)
jsondata = json.load(html)
listing = jsondata['data']
dic_by_symbol = {}
dic_by_name = {}
dic = {}
for item in listing:
    dic_by_symbol[item['symbol']]=str(item['id'])
    dic_by_name[item['name']]=str(item['id'])
dic['symbol']=dic_by_symbol
dic['name']=dic_by_name

# This requires data source from http://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz
with open('price_coinbase_minute_sort.json','r') as f:
    priceDict  = json.load(f) 

#messages
welcome_message = 'Hi! Welcome to xxxx. I\'m XX Bot. I\'ll help to answer any questions than you may have. Send /cancel to stop talking to me. \n\n You can also try /crypto and /deal to explore more !\n\n'
final_message = 'if you need anything else, please /start here and I\'m here to help. \n\n You can also try /crypto and /deal to explore more ! '
intro_message = 'The decentralized structure of blockchain technology provides a vast array of powerful and simple solutions which were never before thought possible.\n We empower and launch new blockchain ventures and equip established businesses with the competitive advantages of blockchain. Blockchain is an emerging technology that possesses many competitive advantages for both small startups and large corporations. We are accelerating the blockchain industry by making it accessible, applicable, and understandable.\n\n'
message_3 = 'This is message_3 for xxxx \n\n'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Assign each state with an integer
OPTIONS, CRYPTO, PRICE, DEAL, PROJECT, CONTACT, NAME, EMAIL, CONTENT, BTCPRICE, CHECKPRICE= range(11)
#.          start 
#           Options
# Crypto    Deal     Contact
# Price     Project  Name
#                    Email
#                    Content
#            END 

def getTicker(query_type, query_input):
    ticker_api = 'https://api.coinmarketcap.com/v2/ticker/'+ dic[query_type][query_input]
    html_ticker = json.load(get.urlopen(ticker_api))['data']
    name = html_ticker['name']
    symbol = html_ticker['symbol']
    market_cap_in_USD = html_ticker['quotes']['USD']['market_cap']
    current_price_in_USD = html_ticker['quotes']['USD']['price']
    percent_change_1h = html_ticker['quotes']['USD']['percent_change_1h']
    percent_change_24h = html_ticker['quotes']['USD']['percent_change_24h']
    percent_change_7d = html_ticker['quotes']['USD']['percent_change_7d']
    
    return [name, symbol, market_cap_in_USD, current_price_in_USD, percent_change_1h, percent_change_24h, percent_change_7d]

def unixTimeConversion(t):
    if type(t) == int and len(str(t))>10:
        t = int(str(t)[0:10])
    elif type(t) == str and len(t)>10:
        t = int(t[0:10])
    else:
        t = int(t)
    return timeConversion(time.ctime(t))

def timeConversion(t):
    tmp = re.split('\s+', t)
    if len(tmp[2])==1:
        tmp[2]='0'+tmp[2]
    hms = tmp[3].split(':') 
    month = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04',
             'May':'05','Jun':'06','Jul':'07','Aug':'08',
            'Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    return tmp[4]+month[tmp[1]]+tmp[2]+hms[0]+hms[1]#+hms[2]
 
def getBTCprice(t):
    if int(timeConversion(time.ctime()))-t<10000:
        print('data from recent 24 hours not available, retrieving current pricing... ')
        return float(json.load(get.urlopen('https://api.coinbase.com/v2/prices/spot?currency=USD'))['data']['amount'])
    else:
        d=priceDict.get(str(t))
        if d != None:
            print(t)
            return d
        else:
            print('not found')
            return getBTCprice(t-1)

def start(bot, update):
    user = update.message.from_user
    reply_keyboard = [['Token Info', 'Token Deal'], ['BTC Historical Price','Contact Us']]
    logger.info("User %s is talking to us", user.first_name)
    update.message.reply_text(intro_message+ welcome_message +'Please select from the options below \n', reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return OPTIONS

def btcprice(bot, update):
    #user = update.message.from_user
    update.message.reply_text('Input date and time in the format YYYYMMDDHHMM ? ')
    return CHECKPRICE

def checkprice(bot, update):
    #user = update.message.from_user
    update.message.reply_text(str(getBTCprice(int(update.message.text))))
    return ConversationHandler.END

def crypto(bot, update):
    user = update.message.from_user
    #reply_keyboard = [['BTC', 'ETH', 'LTC']]
    #if update.message.text == 'Go Ahead!':
    logger.info("%s, User %s wants to know more about cryptocurrency", update.message.text, user.first_name)
    update.message.reply_text('What cryptocurrency do you want to know about?')
    return PRICE

def price(bot, update):
    user = update.message.from_user
    logger.info("User %s asks for token information", user.first_name)
    if update.message.text[0].lower()==update.message.text[0]:
        query_name = update.message.text[0].upper()+update.message.text[1:]
        query_symbol = update.message.text.upper()
    else:  
        query_name = update.message.text
        query_symbol = update.message.text.upper()
    if query_name in dic['name'].keys():
        result = getTicker('name',query_name)
        update.message.reply_text('The name of this cryptocurrency is '+result[0]+'\n'+
         'The symbol of it is '+result[1]+'\n'+
         'The total market cap is '+str(result[2])+' USD'+'\n'+
         'The current price is '+str(result[3])+' USD'+'\n'+
         '1-hour price change is '+str(result[4])+'%'+'\n'+
         '24-hour price change is '+str(result[5])+'%'+'\n'+
         '7-day price change is '+str(result[6])+'%\n'+final_message)
    elif query_symbol in dic['symbol'].keys():
        result = getTicker('symbol',query_symbol)
        update.message.reply_text('The name of this cryptocurrency is '+result[0]+'\n'+
         'The symbol of it is '+result[1]+'\n'+
         'The total market cap is '+str(result[2])+' USD'+'\n'+
         'The current price is '+str(result[3])+' USD'+'\n'+
         '1-hour price change is '+str(result[4])+'%'+'\n'+
         '24-hour price change is '+str(result[5])+'%'+'\n'+
         '7-day price change is '+str(result[6])+'%\n'+final_message)
    else:
        update.message.reply_text('Sorry, I didn\'t find the symbol or name in my knowledge base, please check the spell and try again later, '+final_message, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
    
def deal(bot, update):
    user = update.message.from_user
    deals_keyboard = [['Envilope Project'],['Other deals']]
    #if update.message.text == 'I like deals!':
    update.message.reply_text('Currently, I have the following deals for you, check it out!\n', reply_markup = ReplyKeyboardMarkup(deals_keyboard, one_time_keyboard=True))
    logger.info("User %s is interested in token deals", user.first_name)
    return PROJECT
    
def envilope(bot, update):
    user = update.message.from_user
    update.message.reply_text(message_3+final_message, reply_markup=ReplyKeyboardRemove())
    logger.info("User %s is checking out envilope project", user.first_name)
    return ConversationHandler.END
    
def otherproject(bot, update):
    user = update.message.from_user
    update.message.reply_text('Sorry, we don\'t have more deals\n'+final_message, reply_markup=ReplyKeyboardRemove())
    logger.info("User %s is checking out other projects", user.first_name)
    return ConversationHandler.END

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])
    
def contact(bot, update):
    user = update.message.from_user
    logger.info("User %s is being asked for name information .", user.first_name)
    update.message.reply_text('What name do you like to be called? \n')
    return NAME

def name(bot, update, user_data):
    user = update.message.from_user
    logger.info("User %s is being asked for email information .", user.first_name)
    name = update.message.text
    user_data['name']=name
    update.message.reply_text('What\'s your email address?\n')
    return EMAIL
    
def email(bot, update, user_data):
    user = update.message.from_user
    logger.info("User %s is being asked for content information .", user.first_name)
    email = update.message.text
    user_data['email']=email
    update.message.reply_text('What do you want to ask me about?\n')
    return CONTENT

def content(bot, update, user_data):
    user = update.message.from_user
    logger.info("User %s has submitted all information .", user.first_name)
    content = update.message.text
    user_data['content']=content
    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}".format(facts_to_str(user_data)))
    with open('userData.json','r') as fp:
        tmp = json.load(fp)
        tmp.append(user_data)
    with open('userData.json','w') as gp:
        json.dump(tmp, gp)
    user_data.clear()
    return ConversationHandler.END
     
def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! '+final_message, reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("BOT TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('crypto', crypto), CommandHandler('deal', deal), CommandHandler('btcprice', btcprice)],
  
        states={
            #INTRO: [RegexHandler('^(Yes|No)$', intro)],
            
            OPTIONS: [RegexHandler('^(Token Info)$', crypto),
                      RegexHandler('^(Token Deal)$', deal),
                      RegexHandler('^(BTC Historical Price)$', btcprice),
                      RegexHandler('^(Contact Us)$', contact)],

            CRYPTO: [MessageHandler(Filters.text, crypto)],
            
            PRICE: [MessageHandler(Filters.text, price)],
            
            DEAL: [MessageHandler(Filters.text, deal)],
            
            PROJECT: [RegexHandler('^(Envilope Project)$', envilope),
                      RegexHandler('^(Other deals)$', otherproject)],
            
            BTCPRICE: [MessageHandler(Filters.text, btcprice)], 
            
            CHECKPRICE: [MessageHandler(Filters.text, checkprice)],
            
            CONTACT: [MessageHandler(Filters.text, contact)],
        
            NAME: [MessageHandler(Filters.text, name, pass_user_data=True)],
            
            EMAIL: [MessageHandler(Filters.text, email, pass_user_data=True)],
            
            CONTENT: [MessageHandler(Filters.text, content, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
