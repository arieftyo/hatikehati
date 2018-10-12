from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from random import randint
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile
import requests, json
import re

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('NoRQIuX60A9qC+O7cTR9jAgBus1B8nfci4ri7c8o9PJyB6VkeSHk3nFVQGKBMcoYwpTQHu3qpfwHGlqusokO+V947DnZbcOcJt/B+E7ZyP1/AAvB0TUFjM6q79pBEPAIqqlGTJjMkys5cMaN8FOvggdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('30458b4e6d4f12e05791ec3948d0c18f')
#===========[ NOTE SAVER ]=======================
notes = {}

#INPUT DATA MHS buat di app.py
def inputbuku(id_buku, judul_buku, pengarang, tahun):
    r = requests.post("http://www.aditmasih.tk/api-tyo/insert.php", data={'id_buku': id_buku, 'judul_buku': judul_buku, 
        'pengarang': pengarang, 'tahun': tahun})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+' berhasil dimasukkan\n'
    elif(flag == "0"):
        return 'Data gagal dimasukkan\n'

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get usesenderr_id
    gid = event.source.sender_id #get group_id
    profile = line_bot_api.get_profile(sender)
    
    data=text.split('-')
    if(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputbuku(data[1],data[2],data[3],data[4])))

    #line_bot_api.reply_message(event.reply_token,TextSendMessage(text='Halo '+profile.display_name+'\n'+event.message.text))


    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)