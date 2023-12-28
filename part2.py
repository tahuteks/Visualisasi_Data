# STREAMLIT.TEXT_INPUT/STREAMLIT.NUMBER_INPUT
import streamlit as st
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

st.text_input("Your name", key = "name")
st.write("Welcome to you,", st.session_state.name)

# STREAMLIT.BUTTON
if st.button('Submit'):
  st.write('You have submitted!')
else:
  st.write('Please submit!')

# STREAMLIT.CHECKBOX
agree = st.checkbox('I agree')
disagree = st.checkbox('I disagree')
if agree:
  st.write('Great!')

# STREAMLIT.SELECTBOX
skill_option = st.selectbox(
  'Which skill do you most want to learn?',
  ('Java', 'Python', 'C', 'PHP', 'C++', 'Javascript', 'HTML', 'Other'))
st.write('You selected:', skill_option)

# STREAMLIT.SLIDER
score = st.slider('What is your score?', 0.0, 100.0, (80.0))
st.write('Score:', score)

# ADD WIDGETS TO SIDEBAR
df = pd.DataFrame(np.random.randn(10, 3),
  columns = ('column %d' % col
    for col in range(3)))
column_left, column_right = st.columns(2)
with column_left:
  st.line_chart(data = df)
with column_right:
  df

# CACHING
@st.cache
def fetch_and_clean_data(url):
    # Fetch data from URL here, and then clean it up.
    return data