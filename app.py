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

def caribuku(id_buku):
    URL = "http://www.aditmasih.tk/api-tyo/show.php?id_buku=" + id_buku
    r = requests.get(URL)
    data = r.json()
    err = "data tidak ditemukan"
    
    flag = data['flag']
    if(flag == "1"):
        id_buku = data['data_buku'][0]['id_buku']
        judul_buku = data['data_buku'][0]['judul_buku']
        pengarang = data['data_buku'][0]['pengarang']
        tahun = data['data_buku'][0]['tahun']
        data= "Judul buku : "+judul_buku+"\nid buku : "+id_buku+"\nPengarang : "+pengarang+"\nTahun : "+tahun
        return data
        # return all_data

    elif(flag == "0"):
        return err

def allbuku():
    r = requests.post("http://www.aditmasih.tk/api-tyo/all.php")
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        hasil = ""
        for i in range(0,len(data['data_buku'])):
            id_buku = data['data_buku'][int(i)][0]
            judul_buku = data['data_buku'][int(i)][2]
            pengarang = data['data_buku'][int(i)][4]
            tahun = data['data_buku'][int(i)][6]
            hasil=hasil+str(i+1)
            hasil=hasil+".\nID buku : "
            hasil=hasil+id_buku
            hasil=hasil+"\nJudul buku : "
            hasil=hasil+judul_buku
            hasil=hasil+"\nPengarang : "
            hasil=hasil+pengarang
            hasil=hasil+"\n"
            hasil=hasil+tahun
            hasil=hasil+"\n"
        return hasil
    elif(flag == "0"):
        return 'Perpustakaan kosong\n'

def hapusbuku(id_buku):
    r = requests.post("http://www.aditmasih.tk/api-tyo/delete.php", data={'id_buku': id_buku})
    data = r.json()

    flag = data['flag']
   
    if(flag == "1"):
        return 'Data '+id_buku+' berhasil dihapus\n'
    elif(flag == "0"):
        return 'Data gagal dihapus\n'

def updatebuku(idLama,id_buku,judul_buku,pengarang,tahun):
    URL = "http://www.aditmasih.tk/api-tyo/show.php?id_buku=" + idLama
    r = requests.get(URL)
    data = r.json()
    err = "data tidak ditemukan"
    id_lama=idLama
    flag = data['flag']
    if(flag == "1"):
        r = requests.post("http://www.aditmasih.tk/api-tyo/update.php", data={'id_lama':id_lama, 'id_buku': id_buku, 'judul_buku': judul_buku,
         'pengarang': pengarang, 'tahun': tahun})
        data = r.json()
        flag = data['flag']

        if(flag == "1"):
            return 'Data '+id_lama+' berhasil diupdate\n'
        elif(flag == "0"):
            return 'Data gagal diupdate\n'

    elif(flag == "0"):
        return err


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
    data=text.split('')
    if(data[0]=='lihat'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=caribuku(data[0])))
    elif(data[0]=='tambah'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=inputbuku(data[1],data[2],data[3],data[4])))
    elif(data[0]=='hapus'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hapusbuku(data[1])))
    elif(data[0]=='ganti'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=updatebuku(data[1],data[2],data[3],data[4],data[5])))
    elif(data[0]=='semua'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=allbuku()))
    elif(data[0]=='ganti buku'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ketikkan ganti-[id lama]-[id baru]-[judul_buku baru]-[pengarang baru]-[tahun baru]"))
    elif(data[0]=='hapus buku'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ketikkan hapus-[id_buku]"))
    elif(data[0]=='tambah buku'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ketikkan tambah-[id_buku]"))
    elif(data[0]=='lihat buku'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ketikkan lihat-[id_buku]"))
    elif(data[0]=='menu'):
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://asset.kompas.com/crop/65x65:865x599/750x500/data/photo/2017/06/28/1265845835.jpg',
            title='Menu',
            text='Please select',
            actions=[
                MessageAction(
                    label='lihat buku',
                    text='lihat buku'
                ),
                MessageAction(
                    label='tambah buku',
                    text='tambah buku'
                ),
                MessageAction(
                    label='hapus',
                    text='hapus'
                ),
                MessageAction(
                    label='ganti buku',
                    text='ganti buku'
                ),
                MessageAction(
                    label='lihat',
                    text='lihat'
                )
            ]
          )
        )
      )
        #menu = "1. lihat-[id_buku]\n2. tambah-[id_buku]-[judul_buku]-[pengarang]-[tahun]\n3. hapus-[id_buku]\n4. ganti-[id lama]-[id baru]-[judul_buku baru]-[pengarang baru]-[tahun baru]\n5. semua"
        #line_bot_api.reply_message(event.reply_token, TextSendMessage(text=menu))
    else :
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Ketik menu dong ! '))


    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)