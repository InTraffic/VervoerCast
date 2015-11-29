from bs4 import BeautifulSoup
import sys
import datetime


def foo(filename):
    soup = BeautifulSoup(open(filename), "lxml")
    forecast = []
    for x in soup.find_all('ul'):
        if 'class' in x.attrs:
            if 'weather-map__table' in x['class']:
                for l in x.find_all('li'):
                    parts = []
                    for s in l.find_all('span'):
                        if 'weather-map__table-cell' in s['class']:
                            for ss in s.strings:
                                ss = ss.strip()
                                if len(ss) > 0:
                                    parts.append(ss)
                    # print(parts)
                    forecast.append(parts)
    return(forecast)


tomorrow = datetime.date.today()+datetime.timedelta(days=1)

forecast = foo(sys.argv[1])
tomorrows_forecast = forecast[0]
# Check if the forecast is indeed for tomorrow.
ist_date = datetime.datetime.strptime(tomorrows_forecast[0], "%d-%m-%Y")
if tomorrow == ist_date.date():
    print(" ".join(tomorrows_forecast))
else:
    pass

