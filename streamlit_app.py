import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My mother\'s new healthy diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#list picker here
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#table as before
streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

#NEW SECTION PER WORKSHOP
streamlit.header('Fruityvice Fruit Advice!')
try: 
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
    else:
      fruityvice_response=requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.stop()

#streamlit.header('Fruityvice Fruit Advice!')
#fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
#streamlit.write('The uwer entered', fruit_choice)

#new section for fruityvice api

#fruityvice_response=requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())#just writes data to screen

#normalise json
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it to screen
#streamlit.dataframe(fruityvice_normalized)
#troubleshoot
streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
#try 2

fruit_choice2 = streamlit.text_input('What fruit would you like information about?')
streamlit.write("thanks for adding ", fruit_choice2)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
