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

st.caption("DATA VISUALISATION")
# DATA VISUALISATION

option = st.selectbox('Select the column you like',["Lat", "Lon", "dom"])
'You selected: ', option

if option == "dom":
    fig, ax = plt.subplots()
    ax.hist(x=df["dom"], bins=30, rwidth=0.8, range=(0.5, 30.5))
    ax.set_xlabel("Date of the month")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
if option == "Lat":
    fig, ax = plt.subplots()
    ax.hist(x=df["Lat"], range=(40.5, 41))
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
if option == "Lon":
    fig, ax = plt.subplots()
    ax.hist(x=df["Lon"], range=(-74.3, -73.6))
    ax.set_xlabel("Latitude")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

"-----------------------------------------------------------------------"


if st.checkbox('Show dataframe'):
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12, 5))
    ax1.hist(df["Lat"], range=(40.5, 41))
    ax1.set_xlabel("Latitude")
    ax1.set_ylabel("Frequency")

    ax2.hist(df["Lon"], range=(-74.3, -73.6))
    ax2.set_xlabel("Longitude")
    ax2.set_ylabel("Frequency")
    st.pyplot(fig)

"-----------------------------------------------------------------------"

fig, ax = plt.subplots()
chart = st.pyplot(fig)
for i in range(20):
    ax.hist(x=df["dom"], range=(0,i))
    ax.set_xlabel("Date of the month")
    ax.set_ylabel("Frequency")
    chart.pyplot(fig)
    time.sleep(0.1)

"-----------------------------------------------------------------------"

st.caption("DATA CROSS ANALYSIS")
# DATA CROSS ANALYSIS

fig, ax1 = plt.subplots()
ax2 = ax1.twiny()

ax1.hist(df["Lat"], range=(40.5, 41))
fig.suptitle("")
ax1.set_xlabel("Latitude")
ax1.set_ylabel("Frequency")

ax2.hist(df["Lon"], range=(-74.3, -73.6))
ax2.set_xlabel("Longitude")
ax2.set_ylabel("Frequency")
st.pyplot(fig)

"-----------------------------------------------------------------------"