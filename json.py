# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 17:12:56 2017

@author: weilnboeck
"""

import json
import datetime

with open('jfileNIKKEI225p1.json', 'r') as file:
    array = json.load(file)

for entry in array['Aktien']:
    print('-----------------------------')
    print(entry['name'], '  :  ', entry['URL'])
    ISIN = entry['name']
    ISIN = ISIN.split("ISIN: ")[1].split("]")[0]
    print(ISIN)
    AvgDPS = 0.0
    AvgEPSdil = 0.0
    DPSCounter = 0
    EPSdilCounter = 0
    lastEQR = 0
    payedDividend = True
    oldestDivDate = datetime.datetime.today().year
    newestEQRDate = datetime.datetime.today().year - 10
    for year in {'2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010'
                 ,'2011', '2012', '2013', '2014', '2015', '2016'}:
        dividend = 0.0
        yearProper = datetime.datetime.strptime(year, '%Y').year
        try:
            HVDataAvailable = False
            for HV in entry['HVDiv']:
                HVyear = datetime.datetime.strptime(HV['Datum'], '%d.%m.%y').year
                if HVyear == yearProper:
                    HVDataAvailable = True
                    try:
                        dividend = dividend + float(HV['Dividende'].replace(',','.'))
                    except ValueError:
                        pass
            if dividend == 0.0 and HVDataAvailable:
                payedDividend = False
            elif HVDataAvailable and payedDividend:
                if yearProper < oldestDivDate:
#                    print(oldestDivDate, ' -> ', yearProper)
                    oldestDivDate = yearProper
        except KeyError:
#            print('No Dividend Data for ', entry['name'])
            pass
#        print(year, ' Dividende: ', dividend)
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
                        try: 
                            EQR = float(GUV['equityratio'].replace(',','.'))
                            if yearProper >= newestEQRDate:
                                lastEQR = EQR
                        except ValueError:
                            pass
            except KeyError:
                print('There is a problem in GUV Data')
        except KeyError:
            print('No valid GuV for ', entry['name'])
    if payedDividend and lastEQR > 30:
        AvgDPS = AvgDPS/DPSCounter
        print('The Average DPS is ', AvgDPS, ' over ', DPSCounter, ' years')
        AvgEPSdil = AvgEPSdil/EPSdilCounter
        print('The Average diluted EPS is ', AvgEPSdil, ' over ', EPSdilCounter, ' years')
        print('Defensive Graham value is: ', AvgEPSdil*20)
        print('Dividend payed continously since at least ', oldestDivDate)
        print('Last EQR: ', lastEQR, '%')
        if lastEQR <= 50:
            print('Be carful, lastEQR only ', lastEQR, '%, is it a public utility company?')
    elif not payedDividend:
        print('Dividend not payed continuously')
    elif not lastEQR > 30:
        print('Latest Equity ratio only: ', lastEQR, '%')
        