# Jacques TELLIER 20200858 #


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import streamlit as st
import time

st.title("This is Jack's app")
st.subheader('Welcome !')

# DATA IMPORTATION

df = pd.read_csv("uber-raw-data-apr14.csv")
df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%m/%d/%Y %H:%M:%S")


# DATA TRANSFORMATION

def get_dom(dt): 
    return dt.day

def get_weekday(dt): 
    return dt.weekday()

def count_rows(rows):
    return len(rows)

df['dom'] = df['Date/Time'].map(get_dom)

df['weekday']= df['Date/Time'].map(get_weekday)

df['hour']= df['Date/Time'].dt.hour

# DATA VISUALISATION

fig, ax = plt.subplots()
ax.hist(x=df["dom"], bins=30, rwidth=0.8, range=(0.5, 30.5))
st.pyplot(fig)

fig, ax = plt.subplots()
ax.hist(x=df["dom"], bins=30, rwidth=0.8, range=(0.5, 30.5))
ax.set_xlabel("Date of the month")
ax.set_ylabel("Frequency")
st.pyplot(fig)


grpby = df.groupby(df['dom']).apply(count_rows)
st.bar_chart(grpby)

st.bar_chart(grpby.sort_values())

plt.hist(df["Date/Time"].dt.hour, bins=24, range=(0.5, 24))

plt.hist(df["weekday"], bins=7, rwidth=0.8, range=(-0.5, 6.5))

grpby2 = df.groupby(['weekday', 'hour']).apply(count_rows).unstack()
sb.heatmap(grpby2)

plt.hist(x=df.weekday, bins=7, range=(0,6))
plt.xticks(np.arange(7), 'Mon Tue Wed Thu Fri Sat Sun'.split())

# DATA CROSS ANALYSIS

fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12, 5))
ax1.hist(df["Lat"], range=(40.5, 41))
fig.suptitle("")
ax1.set_xlabel("Latitude")
ax1.set_ylabel("Frequency")

ax2.hist(df["Lon"], range=(-74.3, -73.6))
ax2.set_xlabel("Longitude")
ax2.set_ylabel("Frequency")



fig, ax1 = plt.subplots()
ax2 = ax1.twiny()

ax1.hist(df["Lat"], range=(40.5, 41))
fig.suptitle("")
ax1.set_xlabel("Latitude")
ax1.set_ylabel("Frequency")

ax2.hist(df["Lon"], range=(-74.3, -73.6))
ax2.set_xlabel("Longitude")
ax2.set_ylabel("Frequency")


ax3 = sb.scatterplot(data=df["Lat"])
