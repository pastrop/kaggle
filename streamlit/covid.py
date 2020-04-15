import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#import datetime
#from dateutil.parser import parse

st.title('COVID19 Data Analysis')


data_load_state = st.text('Loading data...')
df = pd.read_csv('covid_19_data.csv')
data_load_state.text('Loading data... done!')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df.head(10))

st.subheader('Comparison of the "Confirmed" and "Death" Curves for Hubei Province, Italy, New York, Spain')
#start = df.loc[df['Province/State'] == 'Hubei', 'ObservationDate'].iloc[0]
#finish = df.loc[df['Province/State'] == 'Hubei', 'ObservationDate'].iloc[-1]
#dt = parse(start).date()
#end = parse(finish).date()
len_max = len(list(df.loc[df['Province/State'] == 'Hubei', 'ObservationDate'].values))
len_Italy = len(list(df.loc[df['Country/Region'] == 'Italy', 'Deaths'].values))
len_NY = len(list(df.loc[df['Province/State'] == 'New York', 'Deaths'].values))
len_Spain = len(list(df.loc[df['Country/Region'] == 'Spain', 'Deaths'].values))

Italy = [0]*(len_max-len_Italy)+list(df.loc[df['Country/Region'] == 'Italy', 'Deaths'].values)
NY = [0]*(len_max-len_NY)+list(df.loc[df['Province/State'] == 'New York', 'Deaths'].values)
Spain = [0]*(len_max-len_Spain)+list(df.loc[df['Country/Region'] == 'Spain', 'Deaths'].values)

st.write(len_max,len(NY),len(Spain))
dat = st.slider('date selector', 0, len_max)


test = pd.DataFrame({
  'date': list(df.loc[df['Province/State'] == 'Hubei', 'ObservationDate'].values)[dat:],
  'Hubei - Deaths': list(df.loc[df['Province/State'] == 'Hubei', 'Deaths'].values)[dat:],
  'Italy - Deaths': Italy[dat:],
  'NY - Deaths': NY[dat:],
  'Spain - Deaths': Spain[dat:]
})

test = test.rename(columns={'date':'index'}).set_index('index')
st.line_chart(test, use_container_width=True)

fig_test, ax = plt.subplots(figsize=(20, 8)) 
# Add x-axis and y-axis

ax.plot(df.loc[df['Province/State'] == 'Hubei', 'ObservationDate'],
          df.loc[df['Province/State'] == 'Hubei', 'Confirmed'],label = 'Hubei - Confirmed',
          color='purple')

ax.plot(df.loc[df['Country/Region'] == 'Italy', 'ObservationDate'],
          df.loc[df['Country/Region'] == 'Italy', 'Confirmed'], label = 'Italy - Confirmed',
          color='orange')

ax.plot(df.loc[df['Province/State'] == 'New York', 'ObservationDate'],
          df.loc[df['Province/State'] == 'New York', 'Confirmed'],label = 'New York - Confirmed',
          color='red')

ax.plot(df.loc[df['Country/Region'] == 'Spain', 'ObservationDate'],
          df.loc[df['Country/Region'] == 'Spain', 'Confirmed'], label = 'Spain - Confirmed',
          color='green')



# Set title and labels for axes
ax.set(xlabel="Date",
       ylabel="ConfirmedCases",
       title="Hubei vs Italy vs Spain vs New York")
plt.xticks(rotation=90, fontsize = 5)
plt.legend(loc='upper left')

st.pyplot(fig_test)

# interactive charts - US Major Metro Areas:

st.subheader('Major Metro Areas: Confirmed Cases Normalized by Population Density (in days starting on 01/22/2020)')
df_us = pd.read_csv('time_series_covid_19_confirmed_US.csv')
if st.checkbox('Show raw data - US Cities'):
    st.subheader('Raw data - US Cities')
    st.write(df_us.head(10))

# Data for 10 largest US Metro Areas:
cols = [0,1,2,3,4,5,6,7,8,9,10]
df_nyc = df_us.loc[df_us['Admin2'] =='New York'].drop(df_us.columns[cols],axis=1)
df_la = df_us.loc[df_us['Admin2'] =='Los Angeles'].drop(df_us.columns[cols],axis=1)
df_houston = df_us.loc[(df_us['Admin2'] =='Harris') & (df_us['Province_State']=='Texas')].drop(df_us.columns[cols],axis=1)
df_chicago = df_us.loc[(df_us['Admin2'] =='Cook') & (df_us['Province_State']=='Illinois')].drop(df_us.columns[cols],axis=1)
df_phoenix = df_us.loc[df_us['Admin2'] =='Maricopa'].drop(df_us.columns[cols],axis=1) 
df_philly = df_us.loc[df_us['Admin2'] =='Philadelphia'].drop(df_us.columns[cols],axis=1)
df_sanant = df_us.loc[(df_us['Admin2'] =='Bexar') & (df_us['Province_State']=='Texas')].drop(df_us.columns[cols],axis=1)
df_dallas = df_us.loc[(df_us['Admin2'] =='Dallas') & (df_us['Province_State']=='Texas')].drop(df_us.columns[cols],axis=1)
df_sanjose = df_us.loc[(df_us['Admin2'] =='Santa Clara') & (df_us['Province_State']=='California')].drop(df_us.columns[cols],axis=1)
df_sandiego = df_us.loc[(df_us['Admin2'] =='San Diego') & (df_us['Province_State']=='California')].drop(df_us.columns[cols],axis=1)
# Normilizing by the Population
NYC_norm = [item//38 for item in list(df_nyc.values.flatten())]
LA_norm = [round(item/7.5) for item in list(df_la.values.flatten())]
Houston_norm = [round(item/3.6) for item in list(df_houston.values.flatten())]
Chicago_norm = [item//12 for item in list(df_chicago.values.flatten())]
Phoenix_norm = [round(item/1.55) for item in list(df_phoenix.values.flatten())]
Philly_norm = [round(item/4.9) for item in list(df_philly.values.flatten())]
Sanant_norm = [round(item/3.2) for item in list(df_sanant.values.flatten())]
Dallas_norm = [round(item/3.65) for item in list(df_dallas.values.flatten())]
Sanjose_norm = [round(item/1.3) for item in list(df_sanjose.values.flatten())]
Sandiego_norm = [round(item/0.8) for item in list(df_sandiego.values.flatten())]

timeline = len(NYC_norm)
val = st.slider('day', 0, timeline, (49,60))
#st.write(val)
chart_cities = pd.DataFrame({'day':list(range(val[0],val[1])),
	                          'New York': NYC_norm[val[0]:val[1]],
	                          'LA': LA_norm[val[0]:val[1]],
	                          'Houston_norm':Houston_norm[val[0]:val[1]],
	                          'Chicago_norm':Chicago_norm[val[0]:val[1]],
	                          'Phoenix_norm':Phoenix_norm[val[0]:val[1]],
	                          'Philadelphia': Philly_norm[val[0]:val[1]],
	                          'San Antonio': Sanant_norm[val[0]:val[1]],
	                          'Dallas':Dallas_norm[val[0]:val[1]],
	                          'San Jose':Sanjose_norm[val[0]:val[1]],
	                          'San Diego':Sandiego_norm[val[0]:val[1]]})

chart_cities = chart_cities.set_index('day')
st.line_chart(chart_cities, width = 1000, height = 700)


# side by side plots - Daily Infections
st.subheader('Daily Infection Rate - NYC')

frame_NY = {'ObservationDate': df.loc[df['Province/State'] == 'New York', 'ObservationDate'],
         'Confirmed':df.loc[df['Province/State'] == 'New York', 'Confirmed'],
         'Deaths':df.loc[df['Province/State'] == 'New York', 'Deaths']}
frame_NY = pd.DataFrame(frame_NY)
frame_NY_grouped_confirmed = frame_NY.groupby(['ObservationDate'])['Confirmed'].sum()
frame_NY_grouped_death = frame_NY.groupby(['ObservationDate'])['Deaths'].sum()


fig = plt.figure(figsize=(10, 6))
fig.add_subplot(1,2,1)

plot_NY = []
plot_NY_conf = []
rate_NY = frame_NY_grouped_confirmed.values
for item in zip(rate_NY[::],rate_NY[1:]):
    plot_NY.append((item[1]-item[0]))   
#print(len(plot_NY))
plt.plot(list(frame_NY['ObservationDate'])[1:],plot_NY)
plt.xticks(rotation='vertical', fontsize = 5)
plt.title('Infection Rate-NY')

fig.add_subplot(1,2,2)
plot_NY = []
rate_NY = frame_NY_grouped_confirmed.values
for item in zip(rate_NY[::],rate_NY[1:]):
    plot_NY.append((item[1]-item[0])/item[0])   
print(plot_NY)
#plot_NY_conf = copy.deepcopy(plot_NY)
count = 0
for item in reversed(plot_NY):
    if item>0.2:
        break
    count += 1
print(count)
plt.plot(plot_NY)
plt.title('Normalized Infection Rate')

st.pyplot(fig)

# NY Death Rate & Normilized Death Rate
fig = plt.figure(figsize=(10, 6))
fig.add_subplot(1,2,1)

plot_NY = []
rate_NY = frame_NY_grouped_death.values
rate_NY_filtered = list(filter(lambda x: x != 0, rate_NY))        
for item in zip(rate_NY_filtered[::],rate_NY_filtered[1:]):
    plot_NY.append((item[1]-item[0]))
plt.plot(plot_NY)
plt.title('Death Rate')

fig.add_subplot(1,2,2)
plot_NY = []
rate_NY = frame_NY_grouped_death.values
rate_NY_filtered = list(filter(lambda x: x != 0, rate_NY))        
for item in zip(rate_NY_filtered[::],rate_NY_filtered[1:]):
    plot_NY.append((item[1]-item[0])/item[0])
plt.plot(plot_NY)
plt.title('Normalized Death Rate')

st.pyplot(fig)
#future functionality

#chart_data_x = pd.DataFrame({'Date':df.loc[df['Country/Region'] == 'Italy', 'ObservationDate'].values})

#chart_data = pd.concat([chart_data_x,chart_data_y])
#chart_data = chart_data.set_index('Date')

#st.line_chart(chart_data, width = 1000, height = 700)

#f = px.histogram(df.query(f”price.between{values}”), x=”price”, nbins=15, title=”Price distribution”)
#st.line_chart(chart_data, width = 1000, height = 700)

# for the future styling
def styling():
	st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
    }}
</style>
""",
        unsafe_allow_html=True,
    )



#interactive chart
#st.subheader('Interactive Chart')
#frame_Italy = {'ObservationDate': df.loc[df['Country/Region'] == 'Italy', 'ObservationDate'],'Confirmed':df.loc[df['Country/Region'] == 'Italy', 'Confirmed']}
#frame_Italy = pd.DataFrame(frame_Italy)
#frame_Italy_grouped_confirmed = frame_Italy.groupby(['ObservationDate'])['Confirmed'].sum()

#plot_Italy = []
#rate_Italy = frame_Italy_grouped_confirmed.values
#for item in zip(rate_Italy[::],rate_Italy[1:]):
    #plot_Italy.append((item[1]-item[0]))
#plt.plot(plot_Italy)
#values = st.slider('day', 0, len(plot_Italy), (5,20))
#st.write(values)
#chart1 = pd.DataFrame({'Daily Confirmed': plot_Italy[values[0]:values[1]],'Day':list(range(values[0],values[1]))})

#st.write(chart1.head(5))
#chart1 = chart1.set_index('Day')
#st.line_chart(chart1, width = 1000, height = 700)