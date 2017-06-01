# BeybladeBurst_bot
# 蒼井霸斗

![Alt text](http://anmtv.xpg.uol.com.br/wp-content/uploads/beyblade-burst-3-600x300.jpg)

    蒼井霸斗 聊天機器人 簡介
    
戰鬥陀螺

    結晶輪盤、鋼鐵輪盤、軸心
    
 比賽資訊

    北區、中區、南區、東區
    
 賣場資訊
 
    北區、中區、南區、東區

# 如何使用戰鬥陀螺 chat bot？

  - 搜尋 @BeybladeBurst_bot (蒼井霸斗)
  - 點選 /start 開始對話
  - 有四個選項
  -     戰鬥陀螺、零件、比賽資訊、賣場資訊
  - 可以輸入相同的關鍵字來查詢
  - 或是直接以底下的按鈕點選欲查詢資訊
  - 若輸入其他非關鍵字的字，會回覆關鍵字介紹

### 戰鬥陀螺
> 點選戰鬥陀螺按鈕或輸入關鍵字 "戰鬥陀螺 "，會出現提示字串
> 輸入欲查詢品項數字 ( 1 - 85 )
> 會回傳日本官方網站的相對應商品圖及名稱
> 利用 database 獲取相對應資料
> 若想要更詳細的各部位零件，可按底下按鈕或輸入關鍵字
> 會回傳選擇的零件部位的名稱及圖片
> 按下取消，會回到開始的選擇畫面

### 零件
> 點選零件按鈕或輸入關鍵字 "零件 "，會出現提示字串
> 點選欲查詢的項目 ( 結晶輪盤、鋼鐵輪盤、軸心 ) 或輸入關鍵字
> 會回傳該種類中所有的品項圖片
> 圖片上有標示攻擊力、防禦力......等

### 賣場資訊
> 點選賣場資訊按鈕或輸入關鍵字 "賣場資訊 "，會出現提示字串
> 點選欲查詢的區域 ( 北區、中區、南區、東區 ) 或輸入關鍵字
> 利用網路爬蟲回傳該區域中所有的專櫃店家
> 詳細資訊包含店名、店家地址及電話

### 比賽資訊
> 點選比賽資訊按鈕或輸入關鍵字 "比賽資訊 "，會出現提示字串
> 點選欲查詢的區域 ( 北區、中區、南區、東區 ) 或輸入關鍵字
> 回傳該區域中所有比賽場次的照片
> 詳細資訊包含日期、時間及地點

# How to run your code？
     ./ngrok http 5000
     
把網址複製下來放進 app.py

    python3 app.py

# Finite State Machine
![Alt text](http://i.imgur.com/e6vccXk.png)

# State
-   user ： 初始 state，傳入 input 後，根據判斷到其餘五個 state (state1 , state2, hello, beyblade, parts)
-   hello ： 為初始 state 輸入皆不符合關鍵字時所到的 state，會回覆提示字串，再回到 user state
-   state1 ：為初始 state 輸入比賽資訊時進入，輸入取消會回到 user state
-   pic：為 state1 輸入地區關鍵字後進入，輸入取消會回到 user state，未輸入取消則能繼續選擇地區
-   state2 ：為初始 state 輸入賣場資訊時進入，輸入取消會回到 user state
-   taiwan ：為 state2 輸入地區關鍵字後進入，輸入取消會回到 user state，未輸入取消則能繼續選擇地區
-   beyblade ：為初始 state 輸入戰鬥陀螺時進入
-   product ：為 beyblade state 輸入各品項數字後進入，並回傳相對應的商品資訊
-   detail ：為 product state 輸入各零件關鍵字後進入，回傳上個 state 收到的品項數字對應的零件部位
-   parts ：為初始 state 輸入零件時進入，輸入取消會回到 user state
-   part ：為 parts state 輸入各零件關鍵字後進入，回傳所有零件資訊圖片


