from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

# app_id = "wxda714829c5c006df"
# app_secret = "d9c1d57da6cfab23f24645d5d8eda963"

# user_id = "o_Umd6Vux-Pz6dQRfP5G1D6kycYE"
# template_id = "uFD__3huhMoZn0XKCn7gLDrMtxpjzhQMYteaWEEa4Ys"

city = "临海"

birthday = "8-5"
start_date = "2022-6-7"
yimaday = 16

yama_watch = ""
year = date.today().year
if (year%4==0 and year%100!=0) or (year%400==0):
  calendar={1:31,2:29,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
else:
  calendar={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

def watch_out_yima():
  cur_day = int(date.today().day)
#   cur_day = 28
  cur_month = int(date.today().month)
  left_day = 0
  pass_day = 0
  if cur_day <= yimaday:
    left_day = yimaday - cur_day
    if cur_day < yimaday:
        pass_day = cur_day
        pass_day += calendar[cur_month] - yimaday
    else:
        pass_day = 0
  else:
    left_day = calendar[cur_month] - cur_day
    left_day += yimaday
    pass_day = cur_day - yimaday
  # 计算距离来了多久
  
  return left_day,pass_day

def get_weather():
  url = "https://api.seniverse.com/v3/weather/daily.json?key=SwKq-NNswcqE7bV2C&location=hangzhou&language=zh-Hans&unit=c&start=-1&days=5"
  res = requests.get(url).json()
  weather = res['results'][0]['daily'][0]['text_day'] + '-' + res['results'][0]['daily'][0]['text_night']
  print(weather)
  low_temp = res['results'][0]['daily'][0]['low']
  high_temp = res['results'][0]['daily'][0]['high']
  return weather, math.floor(weather['temp']), low_temp, high_temp

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

    
# def get_yima_day():
print(app_id)
print(app_secret)

client = WeChatClient(app_id, app_secret)


week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
week = week_list[date.today().weekday()]
print(week)

wm = WeChatMessage(client)
wea, temperature ,low_temp ,high_temp= get_weather()

watch_out = ""

left_day,pass_day = watch_out_yima()

yama_watch
if(pass_day <= 5):
  watch_out = "姨妈期间记得注意休息呀，别吃冷的辣的，清淡饮食，注意保暖，不舒服了随时滴滴鸭鸭奥，给你去泡红糖水，按摩按摩，爱你~"
elif(left_day <= 7):
  yama_watch = "距离大姨妈拜访大概还有" + str(left_day) + "天" 
  watch_out = "快来大姨妈啦，记得别吃冷的辣的，要注意休息，来了滴我一声，我马上给你去泡红糖水，想吃啥喝啥，随时callback，爱你~"
else:
  yama_watch = "距离大姨妈拜访大概还有" + str(left_day) + "天" 

print(high_temp)
data = {
  "week":{"value": week },"weather":{"value":wea},"low_temp":{"value": int(low_temp) },"high_temp": {"value": int(high_temp)},"temperature":{"value":temperature},"love_days":{"value":get_count()+1},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()},
  "words_yima":{"value":watch_out , "color":get_random_color()}, "yima_dely": {"value": yama_watch}}
# data = {"weather":{"value":wea}}

res = wm.send_template(user_id, template_id, data)
print(res)
