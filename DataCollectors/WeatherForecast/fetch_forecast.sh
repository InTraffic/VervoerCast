#!/bin/bash

rm -f verwachtingen
wget http://www.knmi.nl/nederland-nu/weer/verwachtingen
python parse_forecast.py verwachtingen

