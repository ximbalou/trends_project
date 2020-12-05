#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### Instal the Pytrends Package ###

get_ipython().system('pip install pytrends')
get_ipython().system('pip install termcolor')
get_ipython().system('pip install ipywidgets')
get_ipython().system('pip install pivottablejs')


# In[1]:


### Import the needed libraries ###

from pytrends.request import TrendReq
from ipywidgets import interact, interactive, fixed, interact_manual
from pivottablejs import pivot_ui
from datetime import date
from termcolor import colored

import ipywidgets as widgets
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly
import webbrowser
import re
import datetime
import requests


# In[2]:


### Assigning the API module to a variable ###

pytrend = TrendReq()


# In[3]:


### Ask user to input keyword to be analysed ###

keyword_1 =  input("Select a keyword 1: ")

keyword_2 =  input("Select a keyword 2: ")

keyword_3 =  input("Select a keyword 3: ")

kw_list = [keyword_1, keyword_2, keyword_3]

#need bullet-proof at least one keyword
#while kw_list[0] == "":
#    country_code = str(input("Select the country code to be analysed (ex:'PT'): ")).upper()


# In[4]:


kw_list


# In[5]:


### Ask user to select number of years to be analysed ###

print(colored("Select number of years to analyse:" ,attrs=["bold",'underline']))

slider = widgets.IntSlider(
            value=1, 
            min=1, 
            max=5, 
            step=1)

slider.style.handle_color = 'orange'

slider


# In[6]:


### Manage dates to meet API requirements ###

num_days = 7
num_weeks = 52
total_time_range = num_days * num_weeks * slider.value

# Set Today Date
final_date = date.today()

# Set Today -N
init_date = final_date - datetime.timedelta(days = total_time_range)

# Define date to meet API requirements
user_timeframe = init_date.strftime('%Y-%m-%d') + ' ' + final_date.strftime('%Y-%m-%d')
user_timeframe


# In[7]:


### Web Scrapping to get Countries Codes ###

url = 'https://www.iban.com/country-codes'
web_scrappe = pd.read_html(url)

df = web_scrappe[0]

df2 = df[["Country", "Alpha-2 code"]]

#try to do the same with rewuest.get and beautiful soup


# In[8]:


### Create a drop-down widget with Country Names ###

print(colored("Please Select Country to Analyse:" ,attrs=["bold",'underline']))

country = widgets.Dropdown(
        options=df2["Country"],
        value='Portugal',
        disabled=False,
        positioning="Bottom")

country


# In[9]:


### Get the Country Code from the selected Country Name, to meet API Requirements ###

df_country = df2["Alpha-2 code"].where(df2['Country'] == country.value)

country_code = pd.DataFrame(df_country.dropna()).values.flatten()[0]
country_code


# In[10]:


r = requests.get('http://covid19.richdataservices.com/rds/api/catalog/int/jhu_country/classification/iso3166_1/codes')

url = f"https://covid19.richdataservices.com/rds/api/query/int/jhu_country/select?cols=date_stamp,cnt_confirmed,cnt_death,cnt_recovered&where=(iso3166_1={country_code})&format=amcharts&limit=50000"
r = requests.get(url)
new_df = pd.DataFrame(r.json())

covid_data = pd.DataFrame(dict(new_df['dataProvider'])).transpose()
covid_data.head()


# In[11]:


### Load the data according with the user selection ###

pytrend.build_payload(kw_list, 
                      cat = 0, 
                      timeframe = user_timeframe,
                      geo=country.value)


# In[ ]:


### First Query about historical Data ###

"""Interest Over Time: returns historical,indexed data for \n
when the keyword was searched most \n
as shown on Google Trends’ Interest Over Time section."""


df_interest = pytrend.interest_over_time()

df_interest.head(5)
#df_interest
df_interest['Date'] = df_interest.index
df_interest

covid_data["date_stamp"] =  pd.to_datetime(covid_data["date_stamp"])

output = pd.merge(left=df_interest, right=covid_data, how='left', left_on='Date', right_on='date_stamp')
output


# In[ ]:


#df_interest.to_csv("desktop/df_interest.csv", index = True)


# In[ ]:


dates_list = [init_date]

for index in range (0, num_weeks * slider.value - 1):
    dates_list.append(dates_list[index] + datetime.timedelta(days = num_days)) 


# In[ ]:


# Plot
x_axis = dates_list
plt.figure(figsize = (16,10))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(0,40 * slider.value))
plt.gcf().autofmt_xdate()
plt.plot (x_axis, df_interest.iloc[:,0], label = '{}'.format(keyword_1))
#plt.plot (x_axis, output.iloc[:,0], label = '{}'.format(keyword_1))
#plt.plot (x_axis, output.iloc[:,6], label = '{}'.format("cnt_confirmed"))
if keyword_2:
    plt.plot (x_axis, df_interest.iloc[:,1], label = '{}'.format(keyword_2))
    #plt.plot (x_axis, output.iloc[:,1], label = '{}'.format(keyword_2))
if keyword_3:
    plt.plot (x_axis, df_interest.iloc[:,2], label = '{}'.format(keyword_3))
    #plt.plot (x_axis, output.iloc[:,2], label = '{}'.format(keyword_3))
plt.xticks(rotation = 1)
plt.xlabel('\nTime\n')
plt.ylabel('\nLevel of Interest\n')
plt.title('\nInterest over the Time\n')
plt.legend()
plt.show()


# In[ ]:


# create figure and axis objects with subplots()
fig,ax = plt.subplots(figsize=(16,10))

#f, axs = plt.subplots(2,2,figsize=(15,15))

# make a plot
k_1 = ax.plot(dates_list, output.iloc[:,0], color="red", marker="o", label = '{}'.format(keyword_1))
k_2 = ax.plot(dates_list, output.iloc[:,1], color="orange", marker="o", label = '{}'.format(keyword_2))
k_3 = ax.plot(dates_list, output.iloc[:,2], color="green", marker="o", label = '{}'.format(keyword_3))

ax.set_xlabel("year",fontsize=14)
# set y-axis label
ax.set_ylabel('\nLevel of Interest\n',color="red",fontsize=14)


# twin object for two different y-axis on the sample plot
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
k_4 = ax2.plot(dates_list, output.iloc[:,6],color="blue",marker="o", label="Covid +")
ax2.set_ylabel("covid",color="blue",fontsize=14)
ax2.autoscale()
#ax.legend(loc=3)


lns = k_1+k_2+k_3+k_4
labs = [l.get_label() for l in lns]
#ax.legend(lns, labs, loc=1)

fig.legend(loc="upper right")
plt.show()


# In[ ]:


#start the analysys by keyword

#related_queries_dict = pytrend.related_queries()
#keyword_1_top_search = related_queries_dict['{}'.format(keyword_1)]['top']
#keyword_1_rising_search = related_queries_dict['{}'.format(keyword_1)]['rising']
#df_top = pd.DataFrame(keyword_1_top_search)
#df_rise= pd.DataFrame(keyword_1_rising_search)
#pd.concat([df_top, df_rise], axis=1 )
#print(df_rise)
related_queries= pytrend.related_queries()
dg=related_queries.get('bmw').get('rising')
dg


# In[ ]:


#yy = pytrends.interest_by_region(resolution='COUNTRY', inc_geo_code=False)

interest_by_region_df = pytrend.interest_by_region()
print(interest_by_region_df.sort_values(kw_list, ascending=False).head(20))


# In[ ]:


import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# In[ ]:


fig = px.bar(df1, x=df1.index, y=df1['leaseplan'])

fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}) #, text=

#fig = px.bar(df, y='pop', x='country', text='pop')
#fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
#fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
fig.show()


# In[ ]:


yy['geoName_col'] = yy.index
yy


# In[ ]:


pivot_ui(yy)


# In[ ]:


xx.tail()


# In[ ]:



print(colored("Please Insert your e-mail:" ,attrs=["bold",'underline']))

email_box = widgets.Text(
         value='example@gmail.com',
         description="",
)

email_box


# In[ ]:


import re

pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
result = re.match(pattern, email_box.value)

if len(email_box.value) - email_box.value.find(".") <3 or result == None:
    print("Check your e-mail! Confirm the '@' or .com/pt/es...")
elif email_box.value == 'example@gmail.com':
    print("Insert valid e-mail")
else:
    print("E-mail Address OK.")


# In[ ]:


email_box.value


# In[ ]:



from ipywidgets import Layout, Button, Box, FloatText, Textarea, Dropdown, Label, IntSlider

form_item_layout = Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between'
)

form_items = [
    Box([Label(value='Age of the captain'), IntSlider(min=40, max=60)], layout=form_item_layout),
    Box([Label(value='Egg style'),
         Dropdown(options=['Scrambled', 'Sunny side up', 'Over easy'])], layout=form_item_layout),
    Box([Label(value='Ship size'),
         FloatText()], layout=form_item_layout),
    Box([Label(value='Information'),
         Textarea()], layout=form_item_layout)
]

form = Box(form_items, layout=Layout(
    display='flex',
    flex_flow='column',
    border='solid 2px',
    align_items='stretch',
    width='50%'
))
form


# In[ ]:





# In[ ]:





# In[ ]:




