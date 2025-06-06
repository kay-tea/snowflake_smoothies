# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections=5)

if ingredients_list:

    ingredients_string = ''

    for i in ingredients_list:
        ingredients_string += i + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values
        ('""" + ingredients_string + """','"""+name_on_order+ """')"""

    # st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")


import socket
import requests

st.title("Network Test")

# DNS test
try:
    ip = socket.gethostbyname("my.smoothiefroot.com")
    st.success(f"DNS Resolution Succeeded: {ip}")
except Exception as e:
    st.error(f"DNS Resolution Failed: {e}")

# HTTP test
try:
    response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon", timeout=10)
    st.success(f"Request Succeeded: {response.status_code}")
except Exception as e:
    st.error(f"Request Failed: {e}")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())

sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

