

import requests

import json

from time import sleep

from random import randint

import pymongo


from lxml import etree

client = pymongo.MongoClient(host="localhost",port=27017)
db = client['stocks']
table_basic = db['basic']
table_quotes = db['quotes']


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Referer': 'http://quotes.money.163.com/trade/lsjysj_600030.html',
}


def get_table_basic():
    response = requests.get(url='http://quote.eastmoney.com/stock_list.html', headers=headers)

    html = etree.HTML(response.text.encode(response.encoding).decode('gbk'))

    location = '上海'

    print(len(html.xpath('//div[@id="quotesearch"]/ul/li/a/text()')))

    for stock in html.xpath('//div[@id="quotesearch"]/ul/li/a/text()'):
        left = stock.index('(')
        name = stock[0:left]
        code = stock[left + 1:-1]
        # 凌云B股 后面都是深圳的
        if name == '凌云B股':
            location = '深圳'
            print(name, code)
        data = {
            'location': location,
            'name': name,
            'code': code
        }
        # 上海和深圳可能有两个同名的股票
        # 上海股市也可能有同名股票，但是code不一样
        res = table_basic.update_one({'code': code}, {'$set': data}, True)
        # if res.modified_count>0:
        #     print(name,code)
def parsefloat(s):
    s = s.replace(',','')
    return float(s)

def list_reversed(l):
    return list(reversed(l))

def get_selected_data(code):
    year, season = 2020, 1
    base_url = 'http://quotes.money.163.com/trade/lsjysj_{code}.html'
    params = {
        'year': year,
        'season': season
    }

    dates = []
    opens = []
    closes = []
    highs = []
    lows = []

    response = requests.get(url=base_url.format(code=code), headers=headers, params=params)

    html = etree.HTML(response.text)
    for index, tr in enumerate(html.xpath('//table[@class="table_bg001 border_box limit_sale"]/tr')):
        tds = tr.xpath('.//td/text()')
        date = tds[0].replace('-', '')
        open, high, low, close = tds[1], tds[2], tds[3], tds[4]

        dates.append(date)
        opens.append(open)
        highs.append(high)
        lows.append(low)
        closes.append(close)

    return list_reversed(dates),list_reversed(opens),  list_reversed(closes),list_reversed(highs), list_reversed(lows),

def get_lastweekday_data():
    year, season = 2020, 2
    base_url = 'http://quotes.money.163.com/trade/lsjysj_{code}.html'
    params = {
        'year':year,
        'season':season
    }

    query_res = table_basic.find()
    for i,row in enumerate(query_res):
        if i%50==0:
            sleep(randint(4, 6))
        code, location, name = row['code'], row['location'], row['name']

        print(code, location, name)


        response = requests.get(url=base_url.format(code=code), headers=headers, params=params)

        html = etree.HTML(response.text)
        for index,tr in enumerate(html.xpath('//table[@class="table_bg001 border_box limit_sale"]/tr')):
            if index==0:
                tds = tr.xpath('.//td/text()')
                date = tds[0].replace('-', '')
                open, high, low, close = tds[1], tds[2], tds[3], tds[4]
                change, change_pencentage = tds[5], tds[6]
                deal_amount, deal_money, deal_percentage = tds[7].replace(',', ''), tds[8].replace(',', ''), tds[
                    10].replace(',', '')  # 成交量，成交金额（万元）
                print(date, open, high, low, close, change, change_pencentage, deal_amount, deal_money)
                data = {
                    'code': code,
                    'location': location,
                    'name': name,
                    'date': int(date),
                    'open': parsefloat(open),
                    'high': parsefloat(high),
                    'low': parsefloat(low),
                    'close': parsefloat(close),
                    'change': parsefloat(change),
                    'change_pencentage': parsefloat(change_pencentage),
                    'deal_amount': parsefloat(deal_amount),
                    'deal_money': parsefloat(deal_money),
                    'deal_percentage': parsefloat(deal_percentage),
                }
                print(response.status_code, data)
                # 上海和深圳可能有两个同名的股票
                # 上海股市也可能有同名股票，但是code不一样
                table_quotes.update_one({'date': int(date), 'code': code}, {'$set': data}, True)
                break
def get_kc():
    response = requests.get(url='http://api.money.126.net/data/feed/RANK_AUP,RANK_ADOWN,RANK_KCBUP,RANK_KCBDOWN,RANK_ZXBUP,RANK_ZXBDOWN,RANK_CYBUP,RANK_CYBDOWN,RANK_BUP,RANK_BDOWN?callback=ne_1585711036137&[object%20Object]',
                            headers = headers)
    data = json.loads(response.text[17:-2])
    UP,DOWN = [],[]
    cols = ['symbol', 'name', 'issue_price', 'price', 'updown', 'percent','fiveminute', 'hs']
    for i in data['RANK_KCBUP']['list']:
        t1, t2 = [],[]
        t1.append(i['name'])
        t1.append(i['symbol'])
#        t1.append(round(i['issue_price'], 2))
        t1.append(round(i['price'], 2))
        t1.append(round(i['updown'], 2))
        t1.append(round(i['percent'], 4))
        t1.append(round(float(i['fiveminute']), 6))
        t1.append(round(i['hs'], 4))
        UP.append(t1)

    for j in data['RANK_KCBDOWN']['list']:
        t2 = []
        t2.append(j['name'])
        t2.append(j['symbol'])
        t2.append(round(j['issue_price'], 2))
        t2.append(round(j['price'], 2))
        t2.append(round(j['updown'], 2))
        t2.append(round(j['percent'], 4))
        t2.append(round(float(j['fiveminute']), 6))
        t2.append(round(j['hs'], 4))
        DOWN.append(t2)

    return UP, DOWN

from datetime import *
def get_last_WeekDay(day):
    now=day
    print(now.weekday())
    if now.weekday()==0:
      dayStep=3
    elif now.weekday()==6:
        dayStep=2
    else:
      dayStep=1
    lastWorkDay = now - timedelta(days=dayStep)

    return lastWorkDay.strftime("%Y%m%d")

def get_data():
    if table_basic.count() == 0:
        get_table_basic()

    last_weekday = get_last_WeekDay(datetime.now())
    last_weekday = int(last_weekday)
    if table_quotes.find({'date': last_weekday}).count() == 0:
        print('正在抓取上一个交易日数据')
        get_lastweekday_data()

    print('正在加载上一个交易日数据')
    KCB_UP, KCB_DOWN = get_kc()

    # 涨幅前 10
    zf_res = table_quotes.find({'date': last_weekday}).sort([('change_pencentage', -1)]).limit(10)
    # 跌幅前 10
    df_res = table_quotes.find({'date': last_weekday}).sort([('change_pencentage', 1)]).limit(10)
    # 换手率前 10
    hs_res = table_quotes.find({'date': last_weekday}).sort([('deal_percentage', -1)]).limit(10)
    ZF, DF, HS = [], [], []
    cols = ['name', 'code', 'change_pencentage','open', 'close', 'high', 'low', 'deal_percentage']
    for i, j, k in zip(zf_res, df_res, hs_res):
        l1, l2, l3 = [], [], []
        for col in cols:
            l1.append(i[col])
            l2.append(j[col])
            l3.append(k[col])
        ZF.append(l1)
        DF.append(l2)
        HS.append(l3)
    return [ZF, DF,HS,KCB_UP,KCB_DOWN,]


if __name__ == '__main__':

    # get_data()
    # get_kc()
    get_data()