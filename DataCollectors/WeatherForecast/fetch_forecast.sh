#!/bin/bash

cd ~/.virtualenvs/vervoercast/
source ./bin/activate
cd /tmp
rm -f verwachtingen
wget http://www.knmi.nl/nederland-nu/weer/verwachtingen
python ~/bin/parse_forecast.py verwachtingen


