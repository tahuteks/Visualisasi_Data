# DISPLAY DATA
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.title('This is my first app!')
st.write('This is a table')
dataframe = pd.DataFrame(np.random.randn(10, 20),
  columns = ('col %d' % i
    for i in range(20)))
st.write(dataframe)

# VISUALIZATION OF THE CHART
dataframe = pd.DataFrame(np.random.randn(10, 5),
  columns = ('col %d' % i
    for i in range(5)))
dataframe
# Line Chart
st.write('This is a line_chart.')
st.line_chart(dataframe)
# Area Chart
st.write('This is a area_chart.')
st.area_chart(dataframe)
# Bar Chart
st.write('This is a bar_chart.')
st.bar_chart(dataframe)
# Map Visualisation
st.write('Map data')
data_of_map = pd.DataFrame(
  np.random.randn(1000, 2) / [60, 60] + [36.66, -121.6],
  columns = ['latitude', 'longitude'])
st.map(data_of_map)

# DISPLAY PICTURES
image = Image.open('Screenshot (1).png')
st.image(image, caption = 'This is a picture', use_column_width = True)