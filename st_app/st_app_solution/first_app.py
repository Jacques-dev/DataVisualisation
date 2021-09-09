

# ------   PART 0

import streamlit as st
import numpy as np
import pandas as pd

# st.title("My first app")



# ------   PART 1

import os
import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import time

st.title('My first app')

st.text('Cam + Mrn = <3')

df = pd.DataFrame({
'first column': [1, 2, 3, 4],
'second column': [10, 20, 30, 40]
})
st.write(df)

st.latex(r'''a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =\sum_{k=0}^{n-1} ar^k =a \left(\frac{1-r^{n}}{1-r}\right)''')

chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
st.line_chart(chart_data)

map_data = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
st.map(map_data)

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
chart_data

option = st.selectbox('Which number do you like best?',df['first column'])
'You selected: ', option

option2 = st.sidebar.selectbox('Which number do you like best?',df['second column'])
'You selected:', option2

left_column, right_column = st.columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")
expander = st.expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")

latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    # Update the progress bar with each iteration.
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)
'...and now we\'re done!'