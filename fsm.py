from transitions.extensions import GraphMachine
from bs4 import BeautifulSoup
import requests
from PIL import Image
import io 
import urllib.request
import telegram
import pymysql


class TocMachine(GraphMachine):

    B=0

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_hello(self, update):
        text = update.message.text
        return (text !='比賽資訊' and text != '賣場資訊' and text !='戰鬥陀螺' and text !='零件')

    def is_going_to_state1(self, update):
        text = update.message.text
        return text == '比賽資訊' or text == '/比賽資訊'

    def is_going_to_pic(self, update):
        text = update.message.text
        return text == '北部' or text == '中部' or text == '南部' or text == '東部' or text == '取消'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text == '賣場資訊' or text == '/賣場資訊'

    def is_going_to_taiwan(self, update):
        text = update.message.text
        return text == '台灣' or text == '北部' or text == '中部' or text == '南部' or text == '東部' or text == '取消'

    def is_going_to_beyblade(self, update):
        text = update.message.text
        return text == '戰鬥陀螺' or text == '/戰鬥陀螺'

    def is_going_to_product(self, update):
        text = update.message.text
        if text.isnumeric():
            return int(text) > 0 and int(text) < 100 

    def is_going_to_detail(self, update):
        text = update.message.text
        return text == '結晶輪盤' or text == '鋼鐵輪盤（鐵）' or text == '鋼鐵輪盤' or text == '鐵' or text == '軸心' or text.lower() == 'frame' or text == '取消'

    def is_going_to_parts(self, update):
        text = update.message.text
        return text == '零件' or text == '/零件'

    def is_going_to_part(self, update):
        text = update.message.text
        return text == '結晶輪盤' or text == '鋼鐵輪盤（鐵）' or text == '鋼鐵輪盤' or text == '鐵' or text == '軸心' or text.lower() == 'frame' or text == '取消'

#HELLO -------------------------------------------------------------------
    def on_enter_hello(self, update):
        custom_keyboard=[['戰鬥陀螺','零件'],['賣場資訊','比賽資訊']]
        reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text("我要成為陀螺鬥士！！\n可以輸入以下關鍵字：\n  戰鬥陀螺\n  零件\n  賣場資訊\n  比賽資訊",reply_markup=reply_markup)
        self.go_back(update)

    def on_exit_hello(self, update):
        print('Leaving hello')

#比賽資訊 -----------------------------------------------------------------
    def on_enter_state1(self, update):
        custom_keyboard=[['北部','中部','南部','東部'],['取消']]
        reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text("比賽資訊\n請輸入地區：\n  北部\n  中部\n  南部\n  東部\n  取消",reply_markup=reply_markup)
        self.advance(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_pic(self,update):
        if update.message.text == "北部":
            #URL = "http://www.funbox.com.tw/Uploads/News/8173027630.png"
            #with urllib.request.urlopen(URL) as url:
            #    f = io.BytesIO(url.read())
            #img = Image.open(f)
            #img.show()
            #reply(img = urllib2.urlopen(URL).read())
            update.message.reply_photo(photo='http://www.funbox.com.tw/Uploads/News/8173027630.png')
            update.message.text = "11111"
            self.advance(update)
        elif update.message.text == "中部" or update.message.text == "南部" or update.message.text == "東部":
            update.message.reply_photo(photo='http://www.funbox.com.tw/Uploads/News/86474.png')
            update.message.text = "11111"
            self.advance(update)
        elif update.message.text == "取消":
            custom_keyboard=[['戰鬥陀螺','零件'],['賣場資訊','比賽資訊']]
            reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
            update.message.reply_text("我要成為陀螺鬥士！！\n可以輸入以下關鍵字：\n  戰鬥陀螺\n  零件\n  賣場資訊\n  比賽資訊",reply_markup=reply_markup)
            self.go_back(update)


    def on_exit_pic(self, update):
        print('Leaving pic')

#賣場資訊 ------------------------------------------------------------------

    def on_enter_state2(self, update):
        custom_keyboard=[['北部','中部','南部','東部'],['取消']]
        reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text("賣場資訊\n請輸入地區：\n  北部\n  中部\n  南部\n  東部\n  取消",reply_markup=reply_markup)
        self.advance(update)

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_taiwan(self, update):
        res = requests.get("http://www.funbox.com.tw/stores.aspx")
        soup = BeautifulSoup(res.text,'html.parser')
        #print(soup.prettify())
        #store = soup.select('#')
        stores = soup.find_all('div',attrs={'id':'tab1'})
        for x in stores:
            storeArea = x.find_all('ul')
        #print(storeArea[0].text)
        #print(storeArea[1].text)
        #print(storeArea[2].text)
        #print(storeArea[3].text)
        #storeName = store.contents[0]
        #print(stores)
        #print(soup.find('h3'))
        #print(soup.find_all('a',attrs={'rel':'fancybox-thumb'}))

        if update.message.text == "北部":
            print(storeArea[0].text)
            s = storeArea[0].text.replace("\n","\n\n")
            s = s.replace("地址：","\n地址：")
            s = s.replace("電話：","\n電話：")
            update.message.reply_text("北部專櫃")
            update.message.reply_text(s)
            update.message.text = "11111"
            self.advance(update)
        elif update.message.text == "中部":
            print(storeArea[1].text)
            s = storeArea[1].text.replace("\n","\n\n")
            s = s.replace("地址：","\n地址：")
            s = s.replace("電話：","\n電話：")
            update.message.reply_text("中部專櫃")
            update.message.reply_text(s)
            update.message.text = "11111"
            self.advance(update)
        elif update.message.text == "南部":
            print(storeArea[2].text)
            s = storeArea[2].text.replace("\n","\n\n")
            s = s.replace("地址：","\n地址：")
            s = s.replace("電話：","\n電話：")
            update.message.reply_text("南部專櫃")
            update.message.reply_text(s)
            update.message.text = "11111"
            self.advance(update)
        elif update.message.text == "東部":
            print(storeArea[3].text)
            s = storeArea[3].text.replace("\n","\n\n")
            s = s.replace("地址：","\n地址：")
            s = s.replace("電話：","\n電話：")
            update.message.reply_text("東部專櫃")
            update.message.reply_text(s)
            update.message.text = "111111"
            self.advance(update)
        elif update.message.text == "取消":
            custom_keyboard=[['戰鬥陀螺','零件'],['賣場資訊','比賽資訊']]
            reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
            update.message.reply_text("我要成為陀螺鬥士！！\n可以輸入以下關鍵字：\n  戰鬥陀螺\n  零件\n  賣場資訊\n  比賽資訊",reply_markup=reply_markup)
            self.go_back(update)
        #update.message.reply_text(stores)

    def on_exit_taiwan(self, update):
        print('Leaving taiwan')

#戰鬥陀螺 ------------------------------------------------------------------
    def on_enter_beyblade(self, update):
        update.message.reply_text("戰鬥陀螺\n請輸入陀螺代號：\n（ex:b-79 即輸入79）")
        self.advance(update)

    def on_exit_beyblade(self, update):
        print('Leaving beyblade')

    def on_enter_product(self, update):
        db = pymysql.connect(host="140.116.247.183",user="iir_college",password="iir_5757",database="cosme",charset="GBK")
        cursor = db.cursor()
        sql = "SELECT * FROM burst WHERE id=" + (update.message.text)
        if int(update.message.text) < 10:
            update.message.reply_photo(photo='https://beyblade.takaratomy.co.jp/category/img/products/B_0'+update.message.text+'.png')
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    no=row[2]
                    eng=row[3]
                    cn=row[4]
                    jp=row[5]
                    disk=row[6]
                    driver=row[7]
                    update.message.reply_text(cn+"\t"+eng+"\t"+jp)
                    update.message.reply_text("鋼鐵輪盤："+disk+"\t\t\t\t軸心："+driver)
            except:
                print ("Error")
        else:
            update.message.reply_photo(photo='https://beyblade.takaratomy.co.jp/category/img/products/B_'+update.message.text+'.png')
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    no=row[2]
                    eng=row[3]
                    cn=row[4]
                    jp=row[5]
                    disk=row[6]
                    driver=row[7]
                    update.message.reply_text(cn+"\t"+eng+"\t"+jp)
                    update.message.reply_text("鋼鐵輪盤："+disk+"\t\t\t\t軸心："+driver)
            except:
                print ("Error")       
        db.close()
        global B
        B = int(update.message.text)
        update.message.text = "111111"
        custom_keyboard=[['結晶輪盤','鋼鐵輪盤','軸心'],['取消']]
        reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text("零件（若非陀螺請按取消）\n請輸入零件總類：\n  結晶輪盤\n  鋼鐵輪盤（鐵）\n  軸心\n  取消\n（備註：結晶輪盤圖片只有原色版,\n\t\t\t\t無其他色版本）",reply_markup=reply_markup)
        self.advance(update)

    def on_exit_product(self, update):
        print('Leaving product')

    def on_enter_detail(self, update):
        db = pymysql.connect(host="140.116.247.183",user="iir_college",password="iir_5757",database="cosme",charset="GBK")
        cursor = db.cursor()
        global B
        sql = "SELECT * FROM burst WHERE id=" + str(B)
        if update.message.text == "結晶輪盤":
            try:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for row in results:
                        eng=row[3]
                        cn=row[4]
                        jp=row[5]
                        pic=row[8]
                        update.message.reply_text(cn+"\t"+eng+"\t"+jp)
                        update.message.reply_photo(photo=pic)
            except:
                print ("Error")
            update.message.text = "111111"
            self.advance(update)
        elif update.message.text == "鋼鐵輪盤" or update.message.text == "鐵" or update.message.text == "鋼鐵輪盤（鐵）":
            try:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for row in results:
                        disk=row[6]
                        pic=row[9]
                        frame=row[11]
                        update.message.reply_text("鋼鐵輪盤："+disk)
                        update.message.reply_photo(photo=pic)
                        update.message.reply_photo(photo=frame)
            except:
                print ("Error")
            update.message.text = "111111"
            self.advance(update)
        elif update.message.text == "軸心":
            try:
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    for row in results:
                        driver=row[7]
                        pic=row[10]
                        update.message.reply_text("軸心："+driver)
                        update.message.reply_photo(photo=pic)
            except:
                print ("Error")
            update.message.text = "111111"
            self.advance(update)
        elif update.message.text == "取消":
            custom_keyboard=[['戰鬥陀螺','零件'],['賣場資訊','比賽資訊']]
            reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
            update.message.reply_text("我要成為陀螺鬥士！！\n可以輸入以下關鍵字：\n  戰鬥陀螺\n  零件\n  賣場資訊\n  比賽資訊",reply_markup=reply_markup)
            update.message.text = "111111"
            self.go_back(update)

    def on_exit_detail(self, update):
        print('Leaving detail')

#零件 ------------------------------------------------------------------
    def on_enter_parts(self, update):
        custom_keyboard=[['結晶輪盤','鋼鐵輪盤（鐵）'],['軸心', 'frame'],['取消']]
        reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
        update.message.reply_text("零件\n請輸入零件總類：\n  結晶輪盤\n  鋼鐵輪盤（鐵）\n  軸心\n  frame\n  取消",reply_markup=reply_markup)
        self.advance(update)

    def on_exit_parts(self, update):
        print('Leaving parts')

    def on_enter_part(self, update):
        res = requests.get("https://beyblade.takaratomy.co.jp/parts")
        soup = BeautifulSoup(res.text,'html.parser')
        
        if update.message.text == "結晶輪盤":
            update.message.reply_text("結晶輪盤")
            update.message.reply_photo(photo='http://beyblade.vocarevoproject.com/catalog/Layer%201.jpg')
            update.message.reply_photo(photo='http://beyblade.vocarevoproject.com/catalog/Layer%202.jpg')
            update.message.reply_photo(photo='http://beyblade.vocarevoproject.com/catalog/Layer%203.jpg')
            update.message.text = "111111"
            self.advance(update)
        elif update.message.text == "鋼鐵輪盤" or update.message.text == "鐵" or update.message.text == "鋼鐵輪盤（鐵）":
            update.message.reply_text("鋼鐵輪盤")
            update.message.reply_photo(photo='http://beyblade.vocarevoproject.com/catalog/Disk.jpg')
            update.message.reply_photo(photo='http://beyblade.vocarevoproject.com/catalog/Core%20Disk.jpg')
            update.message.text = "11111"
            self.advance(update)
        elif update.message.text == "軸心":
            update.message.reply_text("軸心")
            update.message.reply_photo(photo='http://beyblade.vocarevoproject.com/catalog/Driver%201.jpg')
            update.message.reply_photo(photo='http://beyblade.vocarevoproject.com/catalog/Driver%202.jpg')
            update.message.text = "11111"
            self.advance(update)
        elif update.message.text.lower() == "frame":
            update.message.reply_text("frame")
            update.message.reply_photo(photo='http://beyblade.vocarevoproject.com/catalog/Frame.jpg')
            update.message.text = "11111"
            self.advance(update)
        elif update.message.text == "取消":
            custom_keyboard=[['戰鬥陀螺','零件'],['賣場資訊','比賽資訊']]
            reply_markup=telegram.ReplyKeyboardMarkup(custom_keyboard)
            update.message.reply_text("我要成為陀螺鬥士！！\n可以輸入以下關鍵字：\n  戰鬥陀螺\n  零件\n  賣場資訊\n  比賽資訊",reply_markup=reply_markup)
            self.go_back(update)
        
    def on_exit_part(self, update):
        print('Leaving part')
