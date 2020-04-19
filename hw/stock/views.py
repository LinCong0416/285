from django.shortcuts import render
from alpha_vantage.timeseries import TimeSeries
import requests
from datetime import datetime, timezone
import pytz
import requests
import socket


# Create your views here.
def index(request):
     return render(request,'index.html')

def calPage(request):
    value_A = request.POST['symbol']
    value_B = request.POST['allotment']
    value_C = request.POST['sPrice']
    value_D = request.POST['cPrice1']
    value_E = request.POST['iPrice']
    value_F = request.POST['cPrice2']
    value_G = request.POST['rate']

    resA = float(value_B) * float(value_C)
    resBB = float(value_B) * float(value_C) - float(value_B)*float(value_E) - float(value_D) - float(value_F)
    resB = float(value_B) * float(value_E) + float(value_F) + float(value_D) + resBB * float(value_G) / 100
    resC = resBB * (1 - float(value_G) / 100)
    resD = round(resC / resB * 100, 2)
    resE = (float(value_E) * float(value_B) + float(value_D) + float(value_F)) / float(value_B)

    return render(request,'index.html',context={'data1':resA,'data2':resB,'data3':resC,
                                                'data4':resD,'data5':resE})


def search(request):
    return render(request, 'search.html')

def searchPage(request):
    try:
        api_key = 'EADU97JO5Z1TCYPV'

        input_symbol = request.POST['s']
        ts = TimeSeries(key=api_key, output_format='pandas')

        tz_NY = pytz.timezone('US/Pacific')
        datetime_NY = datetime.now(tz_NY)
        current_time = datetime_NY.strftime("%a %b %d %H:%M:%S %Z %Y")

        # r = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+value_A & 'apikey='+api_key)
        r = ts.get_symbol_search(keywords=input_symbol)
        data, meta_data1 = ts.get_daily(symbol=input_symbol, outputsize='full')

        # result = r.json()
        # full_name = result['bestMatches'][0]['2. name']
        full_name = r[0]['2. name'][0]

        close_data = data['4. close']
        num_change = round(close_data[0] - close_data[1], 2)
        percentage_change = round(num_change / close_data[1] * 100, 2)

        if num_change > 0:
            num_change = '+' + str(num_change)
        else:
            num_change = '-' + str(num_change)

        if percentage_change > 0:
            percentage_change = '+' + str(percentage_change) + '%'
        else:
            percentage_change = '-' + str(percentage_change) + '%'

        return render(request, 'search.html', context={'data1': current_time, 'data2': full_name, 'data3': close_data[0],
                                                   'data4': num_change, 'data5': percentage_change})

    except Exception:
        return render(request, 'err.html')