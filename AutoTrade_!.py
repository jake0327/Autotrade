from pandas import Series
from pickle import NONE
import time
import pyupbit
import datetime
import numpy as np
import threading


access ="MhTx90fyhs7SPgpU8AxYF79KQj8KAgT1qI0a7MiQ"
secret = "Z5H1xO6cknDm5COXGjL7dX98no2Bgf2One2GC45z"

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("Autotrade Start")


def get_domince(ticker, term) :                       # 화폐 도미넌스
    sum_ticker_value = 0
    df_t = pyupbit.get_ohlcv(ticker, interval = term, count=3)
    for d in pyupbit.get_tickers():
        df = pyupbit.get_ohlcv(d, interval = term, count=3)
        sum_ticker_value += df['value'][0]
    get_domince = (df_t['value'][0] / sum_ticker_value) * 100
    return get_domince

def get_target_price(ticker, term):     # 매수 목표가 조회
    df = pyupbit.get_ohlcv(ticker, interval = term, count=4)
    ror = 0
    ava_ror = 1
    real_k = 0
    for k in np.arange(0.1, 1.0, 0.1):
         df['range'] = (df['high'] - df['low']) * k          
         df['target'] = df['open'] + df['range'].shift(1)
         df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'], 1)
         ror = df['ror'][0] * 0.1 + df['ror'][1] * 0.2 + df['ror'][2] * 0.3 + df['ror'][3] * 0.4
         if ror >= ava_ror :
             ava_ror = ror
             real_k = k
    target_price = df.iloc[0]['close']+(df.iloc[0]['high'] - df.iloc[0]['low']) * real_k
    return target_price

def get_balance__(ticker) :      # 잔고 조회
    balances = upbit.get_balances(ticker)
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not NONE:
                return float(b['balance'])
            else : 
                return 0 
    return 0

def get_current_price(ticker):           # 현재가 조회
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]['ask_price']

# def get_start_time(ticker, term) :                    # 시작 설정
#     df = pyupbit.get_ohlcv(ticker, interval = term, count=3)
#     start_time = df.index[0]
#     return start_time

def get_start(time):
    now = datetime.datetime.now()
    str_today = now.strftime('%Y%m%d')
    today = str_today + time
    start = datetime.datetime.strptime(today, '%Y%m%d%H%M%S')
    return start

def get_end(time) :
    now = datetime.datetime.now()
    str_today = now.strftime('%Y%m%d')
    today = str_today + time
    end = datetime.datetime.strptime(today, '%Y%m%d%H%M%S')
    return end


def time0900() :
# 자동매매(0900 ~ 1300)
    while True:
        try:
            now = datetime.datetime.now()
            start = get_start('090000')
            end = get_end('130000')
            end2 = get_end('162900')
            nowCoin = upbit.get_balance("KRW-BTC")
            if start < now < end:
                print("자동매매(0900 ~ 1300) 시작")
                target_price = get_target_price('KRW-BTC', "day")
                current_price = get_current_price("KRW-BTC")
                if target_price < current_price and nowCoin < 0.0001 :
                    print('매수 진행 중(0900 ~ 1300)')
                    krw = upbit.get_balance("KRW")
                    value = krw * 0.9995
                    if value > 5000:
                        print('매수 주문(0900 ~ 1300)')
                        buy_result = upbit.buy_market_order("KRW-BTC", value)
                        print(buy_result)
                        if buy_result == None or 'error' in buy_result:
                            print("매수 재주문(0900 ~ 1300)")
                            time.sleep(1)
                    else:
                        print("잔고부족(0900 ~ 1300)")
            elif end < now < end2 and nowCoin != 0:
                print("매도 처리 중(0900 ~ 1300)")
                BTC = upbit.get_balance("KRW-BTC")
                upbit.sell_market_order("KRW-BTC", BTC)
        except:
            print("0900 ~ 1300 종료")        
            break

def time1630() :
# 자동매매(1630 ~ 1930)
    while True:
        try:
            now = datetime.datetime.now()
            start = get_start('163000')
            end = get_end('193000')
            end2 = get_end('215900')
            nowCoin = upbit.get_balance("KRW-BTC")
            if start < now < end:
                print("자동매매(1630 ~ 1930) 시작")
                target_price = get_target_price('KRW-BTC', "minute60")
                current_price = get_current_price("KRW-BTC")
                if target_price < current_price and nowCoin < 0.0001 :
                    print('매수 진행 중(1630 ~ 1930)')
                    krw = upbit.get_balance("KRW")
                    value = krw * 0.9995
                    if value > 5000:
                        print('매수 주문(1630 ~ 1930)')
                        buy_result = upbit.buy_market_order("KRW-BTC", value)
                        print(buy_result)
                        if buy_result == None or 'error' in buy_result:
                            print("매수 재주문(1630 ~ 1930)")
                            time.sleep(1)
                    else:
                        print("잔고 부족(1630 ~ 1930)")
            elif end < now < end2 and nowCoin != 0:
                print("매도 처리 중(1630 ~ 1930)")
                BTC = upbit.get_balance("KRW-BTC")
                upbit.sell_market_order("KRW-BTC", BTC)
        except:
            print("1630 ~ 1930 종료")        
            break

def time2200() :
    # 자동매매(2200 ~ 0000)
    while True:
        try:
            now = datetime.datetime.now()
            start = get_start('220000')
            end = get_end('235930')
            nowCoin = upbit.get_balance("KRW-BTC")
            if start < now < end:
                print("자동매매(2200 ~ 0000) 시작")
                target_price = get_target_price('KRW-BTC', "minute60")
                current_price = get_current_price("KRW-BTC")
                if target_price < current_price and nowCoin < 0.0001 :
                    print('매수 진행 중(2200 ~ 0000)')
                    krw = upbit.get_balance("KRW")
                    value = krw * 0.9995
                    if value > 5000:
                        print('매수 주문(2200 ~ 0000)')
                        buy_result = upbit.buy_market_order("KRW-BTC", value)
                        print(buy_result)
                        if buy_result == None or 'error' in buy_result:
                            print("매수 재주문(2200 ~ 0000)")
                            time.sleep(1)
                    else:
                        print("잔고 부족(2200 ~ 0000)")
            elif end < now < end + datetime.timedelta(hours=8) and nowCoin != 0:
                print("매도 처리 중(2200 ~ 0000)")
                BTC = upbit.get_balance("KRW-BTC")
                upbit.sell_market_order("KRW-BTC", BTC)
        except:
            print("2200 ~ 0000 종료")        
            break


th_0900 = threading.Thread(target=time0900, args=())
th_1630 = threading.Thread(target=time1630, args=())
th_2200 = threading.Thread(target=time2200, args=())

th_0900.start()
th_1630.start()
th_2200.start()

