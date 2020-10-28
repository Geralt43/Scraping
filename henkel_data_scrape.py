"""
Utilizes Google Analytics database to pull traffic volume of a given keyword within a given timeframe.
"""

import pandas as pd
from pytrends.request import TrendReq
from pandas.io.json._normalize import nested_to_record
from pandas import DataFrame
import matplotlib
import datetime as dt


#list of keywords, if list is too long it might return an error 400 (seems like 5 keywords or less works)
keywords = ['cbdoil','cannabis','patchouli','ylang ylang oil','lavender oil']

#requests the keyword search volume from the last three months
pytrend = TrendReq(hl='en-US', tz=360)
pytrend.build_payload(kw_list=keywords,cat=0,timeframe='today 3-m',gprop='')
data = pytrend.interest_over_time()
data = data.drop(labels=['isPartial'],axis='columns')

#creates visual plot of traffic over time, remove triple quotes to create the image file
"""
image = data.plot(title = 'Traffic from the Last 3 Months')
fig = image.get_figure()
fig.savefig('traffic.png')
"""

#outputs the search results to a csv file
data.to_csv('test.csv', sep=';', encoding='utf_8_sig', header=True)
