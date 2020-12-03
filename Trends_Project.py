#!/usr/bin/env python
# coding: utf-8

# In[6]:


### Instal the Pytrends Package ###

get_ipython().system('pip install pytrends')


# In[338]:


### Import the needed libraries ###

from pytrends.request import TrendReq

import pandas as pd
import matplotlib as plt
import seaborn as sns
import plotly
import webbrowser


# In[187]:


### Assigning the API module to a variable ###

pytrend = TrendReq()


# In[341]:


### Ask user to input keyword to be analysed ###

keyword_1 =  input("select a keyword 1: ")

keyword_2 =  input("select a keyword 2: ")

keyword_3 =  input("select a keyword 3: ")

kw_list = [keyword_1, keyword_2, keyword_3]


# In[321]:


### Ask user to input number of years to be analysed ###

time = str(input("Select number of years to be analysed: "))

years = str("today "+time+"-y")


# In[349]:


### Country to be analysed ###

    # Opening help with countries codes #
    click_here = webbrowser.open_new_tab("https://www.iban.com/country-codes")

    # Ask user to input the country code #
    country_code = str(input("Select the country code to be analysed (ex:'PT'): ")).upper()
    
    # Dummy bullet proof #
    while len(country_code) != 2:
        country_code = str(input("Select the country code to be analysed (ex:'PT'): ")).upper()


# In[325]:


### Load the data according with the user selection ###

pytrend.build_payload(kw_list, 
                      cat = 0, 
                      timeframe =years, 
                      geo = country_code)


# In[351]:


### First Query about historical Data ###

"""Interest Over Time: returns historical,indexed data for \n
when the keyword was searched most \n
as shown on Google Trends’ Interest Over Time section."""


interest = pytrend.interest_over_time()


# In[327]:


yy = pytrend.interest_by_region("CITY", inc_low_vol=True)

yy


# In[193]:


import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# In[265]:


fig = px.bar(df1, x=df1.index, y=df1['leaseplan'])

fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, text=)

#fig = px.bar(df, y='pop', x='country', text='pop')
#fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
#fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig.show()


# In[175]:


yy


# In[ ]:




