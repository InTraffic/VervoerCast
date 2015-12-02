#!/bin/bash

cd /tmp
rm -f verwachtingen
wget http://www.knmi.nl/nederland-nu/weer/verwachtingen
python ~/bin/parse_forecast.py verwachtingen

