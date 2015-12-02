from bs4 import BeautifulSoup
import sys
import datetime
import logging
import json
import os


class ConfigError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def read_config():
    config_file_name = "{}/vervoercast_config.json".format(os.environ['HOME'])
    with open(config_file_name) as json_data_file:
        config = json.load(json_data_file)
        return config
    raise ConfigError("Cannot read configuration file")

def extract_forecast_text(soup):
    lines = []
    for d in soup.find_all('div'):
        if 'class' in d.attrs:
            if 'weather__text' in d['class']:
                for ss in d.strings:
                    lines.append(ss)
    return("\n".join(lines))

def extract_forecast_table(soup):
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


if __name__ == "__main__":
    configuration = read_config()

    today    = datetime.date.today()

    # Parse the forecast page
    soup = BeautifulSoup(open(sys.argv[1]), "lxml")

    # Extract the written forecast.
    forecast_text = extract_forecast_text(soup)

    # Extract data from the table in the forecast.
    forecast = extract_forecast_table(soup)

    tomorrows_forecast = forecast[0]
    tomorrow = today + datetime.timedelta(days=1)

    # Check if the forecast is indeed for tomorrow.
    ist_date = datetime.datetime.strptime(tomorrows_forecast[0], "%d-%m-%Y")
    if tomorrow == ist_date.date():
        datastring = " ".join(tomorrows_forecast)
    else:
        datastring = "NA"
        pass

    datastring = str(today) + ',"' + datastring + '"'
    path = os.path.join(configuration['datadir'], "KNMI/Verwachting")

    if os.path.isdir(path):
        text_forecast_filename = today.strftime("%Y-%m-%d-forecasttext.txt")
        text_forecast_path = os.path.join(path, text_forecast_filename)
        with open(text_forecast_path, "w", encoding="utf-8") as outpf:
            outpf.write(forecast_text)
        forecast_filename = today.strftime("%Y-%m-%d-forecast.csv")
        forecast_path = os.path.join(path, forecast_filename)
        with open(forecast_path, "w", encoding="utf-8") as outpf:
            outpf.write("datestamp,text\n")
            for f in forecast:
                outpf.write(",".join([f[0], '"' + " ".join(f[1:]) + '"']))
                outpf.write("\n")

    else:
        pass
        # Datadirectory does not exist

