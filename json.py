# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 17:12:56 2017

@author: weilnboeck
"""

import json
import datetime

with open('jfile.json', 'r') as file:
    array = json.load(file)

for entry in array['Aktien']:
    print('-----------------------------')
    print(entry['name'], '  :  ', entry['URL'])
    AvgDPS = 0.0
    AvgEPSdil = 0.0
    DPSCounter = 0
    EPSdilCounter = 0
    payedDividend = True
    for year in {'2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010'
                 ,'2011', '2012', '2013', '2014', '2015', '2016'}:
        dividend = 0.0
        try:
            for HV in entry['HVDiv']:
                HVyear = datetime.datetime.strptime(HV['Datum'], '%d.%m.%y').year
                if HVyear == datetime.datetime.strptime(year, '%Y').year:
                    try:
                        dividend = dividend + float(HV['Dividende'].replace(',','.'))
                    except ValueError:
                        pass
        except KeyError:
#            print('No Dividend Data for ', entry['name'])
            pass
#        print(year, ' Dividende: ', dividend)
        if dividend == 0.0:
            payedDividend = False
        try:
            try:
                for GUV in entry['Bilanzdaten']:
                    if GUV['Jahr'] == year:
                        try:
                            AvgDPS = AvgDPS + float(GUV['DPS'].replace(',','.'))
#                            print(year, ' DPS: ', GUV['DPS'].replace(',','.'))
                            DPSCounter = DPSCounter + 1
                        except ValueError:
                            pass
                        try:
                            AvgEPSdil = AvgEPSdil + float(GUV['EPSdiluted'].replace(',','.'))
#                            print(year, ' EPSdiluted: ', GUV['EPSdiluted'].replace(',','.'))
                            EPSdilCounter = EPSdilCounter + 1
                        except ValueError:
                            pass
            except KeyError:
                print('There is a problem in GUV Data')
        except KeyError:
            print('No valid GuV for ', entry['name'])
    if payedDividend:
        AvgDPS = AvgDPS/DPSCounter
        print('The Average DPS is ', AvgDPS, ' over ', DPSCounter, ' years')
        AvgEPSdil = AvgEPSdil/EPSdilCounter
        print('The Average diluted EPS is ', AvgEPSdil, ' over ', EPSdilCounter, ' years')
        print('Defensive Graham value is: ', AvgEPSdil*20)
        