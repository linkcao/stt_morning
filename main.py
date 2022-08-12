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
# template_id = "PTRE1OhKxncrSs_N6NNQ43JnkI6oMgLpoB0H14GzE78"

# city = "临海"

# birthday = "8-5"
# start_date = "2022-6-7"


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  print(weather)
  low_temp = weather['low']
  high_temp = weather['high']
  return weather['weather'], math.floor(weather['temp']), low_temp, high_temp

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

print(app_id)
print(app_secret)

client = WeChatClient(app_id, app_secret)


week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
week = week_list[date.today().weekday()]
print(week)

wm = WeChatMessage(client)
wea, temperature ,low_temp ,high_temp= get_weather()
print(high_temp)
data = {
  "week":{"value": week },"weather":{"value":wea},"low_temp":{"value": int(low_temp) },"high_temp": {"value": int(high_temp)},"temperature":{"value":temperature},"love_days":{"value":get_count()+1},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
# data = {"weather":{"value":wea}}

res = wm.send_template(user_id, template_id, data)
print(res)
